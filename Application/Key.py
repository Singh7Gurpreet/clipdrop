import uuid
import os
import webbrowser
import asyncio
from PersonalBinApi import PersonalBinApi
from FileHandler import FileHandler

class Key:
    __instance = None  # Holds the single instance

    """Ensure only one instance is ever created."""
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(Key, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        # Prevent re-initialization if instance already exists
        if hasattr(self, "_initialized") and self._initialized:
            return

        self.__path = "jwt.txt"
        self.__keyValue = None
        self._initialized = True  # mark initialized

    async def __pollForKey(self, session):
        param = {"uuid": str(session)}
        api = PersonalBinApi()
        for _ in range(1, 16):
            await asyncio.sleep(3)
            token = await api.get_key(param)
            if token is not None:
                fileOperations = FileHandler(self.__path)
                fileOperations.write_to_file(token)
                self.__keyValue = token  # store directly
                break

    async def __login(self):
        session = uuid.uuid4()
        webbrowser.open(f"{os.getenv('BACKEND_URL_AUTHENTICATION')}?uuid={session}")
        await self.__pollForKey(session)

    def __readTokenFromFile(self):
        file = FileHandler(self.__path)
        return file.read_from_file()

    async def initialize(self):
        if not os.path.exists(self.__path):
            await self.__login()
        else:
            temporaryKey = self.__readTokenFromFile()
            api = PersonalBinApi()
            api.set_cookie(temporaryKey)
            response = await api.is_jwt_verified()
            if not response:
                await self.__login()
            else:
                self.__keyValue = temporaryKey
    
    def getKeyValue(self):
        return self.__keyValue
