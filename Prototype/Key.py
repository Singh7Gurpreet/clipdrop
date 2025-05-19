import uuid
import os
import webbrowser
import asyncio
import aiohttp
import json
from dotenv import load_dotenv
load_dotenv()

class Key:
    def __init__(self):
        self.__path = "jwt.txt"
        self.__keyValue = None

    async def __pollForKey(self, session):
        param = {"uuid": str(session)}
        async with aiohttp.ClientSession() as http_session:
            for _ in range(1,31):
                await asyncio.sleep(3)
                async with http_session.get(os.getenv("BACKEND_URL_GETKEY"), params=param) as resp:
                    if(resp.status == 200):
                      data = await resp.text()
                      data = json.loads(data)
                      print(data)
                      with open(self.__path, "w") as file:
                          file.write(data["token"])
                      self.__keyValue = data["token"]
                      break

    async def __login(self):
        session = uuid.uuid4()
        webbrowser.open(f"{os.getenv('BACKEND_URL_AUTHENTICATION')}?uuid={session}")
        await self.__pollForKey(session)

    def __readTokenFromFile(self):
        content = ""
        with open(self.__path, "r") as file:
            content = file.read()
        return content

    async def initialize(self):
        if not os.path.exists(self.__path):
            await self.__login()
        else:
            self.__keyValue = self.__readTokenFromFile()

    def getKeyValue(self):
        return self.__keyValue


# --- Driver code ---
async def main():
    l1 = Key()
    await l1.initialize()

asyncio.run(main())
