import asyncio
from PersonalBinApi import PersonalBinApi
from HttpRequestFileHandler import HttpRequestFileHandler
from FileHandler import FileHandler
from Key import Key

async def func():
    api = PersonalBinApi()
    key  = Key()
    await key.initialize()
    print(key.getKeyValue())
    api.set_cookie(key.getKeyValue())
    response = await api.get_download_link_storage()
    httpFileHandler = HttpRequestFileHandler()
    path = await httpFileHandler.download(response['link'],response['fileName'])
    fileHandler = FileHandler()
    fileHandler.moveFileFromSourceToClipBoard(path)

if __name__ == "__main__":
    asyncio.run(func())
