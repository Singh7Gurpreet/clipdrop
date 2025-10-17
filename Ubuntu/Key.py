import uuid
import os
import webbrowser
import asyncio
import json
from PersonalBinApi import PersonalBinApi
from FileHandler import FileHandler

'''
Dev note:

Future refrence will be adding images too
and also need to add function verify() related to verification of user authentication
or i could some how work around it like would be checking with get /api/file
if I get 403 (unauthorized) simply call login agin
'''

class Key:
    def __init__(self):
        self.__path = "jwt.txt"
        self.__keyValue = None

    async def __pollForKey(self, session):
        param = {"uuid": str(session)}
        api = PersonalBinApi()
        for _ in range(1,16):
            await asyncio.sleep(3)
            token = await api.get_key(param)
            if(token != None):
                fileOperations = FileHandler(self.__path)
                fileOperations.write_to_file(token)
                break
                 

    async def __login(self):
        session = uuid.uuid4()
        webbrowser.open(f"{os.getenv('BACKEND_URL_AUTHENTICATION')}?uuid={session}")
        await self.__pollForKey(session)

    # verify is it valid or not 
    def __readTokenFromFile(self):
        file = FileHandler(self.__path)
        content = file.read_from_file()
        return content

    async def initialize(self):
        if not os.path.exists(self.__path):
            await self.__login()
        else:
            temporaryKey = self.__readTokenFromFile()
            api = PersonalBinApi()
            api.set_cookie(temporaryKey)
            response = await api.is_jwt_verified()
            if(response == False):
                await self.__login()
            else:
                self.__keyValue = temporaryKey

    def getKeyValue(self):
        return self.__keyValue
