import asyncio
from PersonalBinApi import PersonalBinApi
from HttpRequestFileHandler import HttpRequestFileHandler
from FileHandler import FileHandler
from ClipboardEventListener import ClipboardEvent
from Key import Key
from BLEClipboardEventHandler import BLEClipboardEventHandler

CLIPBOARD_CONTENT_FILE_NAME = "text.txt"

#   Now I am left with the storage-api part and android part then 
#  I am finally done with this he heheheheh :)
async def func1():
    api = PersonalBinApi()
    key  = Key()
    await key.initialize()
    api.set_cookie(key.getKeyValue())
    filePath = "BLE.py"
    response = await api.get_upload_link_storage(fileName=filePath)
    httpFileHandler = HttpRequestFileHandler()
    filePath = "./BLE.py"
    response = await httpFileHandler.upload(response['link'],filePath)
    print(response)
    # path = await httpFileHandler.download(response['link'],response['fileName'])
    # fileHandler = FileHandler()
    # fileHandler.moveFileFromSourceToClipBoard(path)ENT_FILE_NAME)

async def func2():
    c = ClipboardEvent(1)
    key = Key()
    await key.initialize()
    api = PersonalBinApi()
    api.set_cookie(key.getKeyValue())
    async def saveClipBoardContentAndUpload(clipboardValue):
        if(clipboardValue == "POP"):
            await BLEClipboardEventHandler().execute()
            return
        fileHandler = FileHandler(CLIPBOARD_CONTENT_FILE_NAME)
        fileHandler.write_to_file(clipboardValue)
        response = await api.get_upload_link_clipboard()
        print(response)
        httpFileHandler = HttpRequestFileHandler()
        await httpFileHandler.upload(response['link'],CLIPBOARD_CONTENT_FILE_NAME)
    c.subscribe(saveClipBoardContentAndUpload)
    await c.start()


async def func3():
    await BLEClipboardEventHandler().execute()

if __name__ == "__main__":
    asyncio.run(func2())
