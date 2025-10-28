'''
=============
|  Driver   |
|   Code    | 
=============
'''

SERVICE_UUID = "0ce78b36-0c84-43eb-8244-000000000000"
UUID_NOTIFY = "0ce78b36-0c84-43eb-8244-000000000001"
UUID_WRITE  = "0ce78b36-0c84-43eb-8244-000000000002"

from Key import Key
import asyncio
from  ClipboardEventListener import ClipboardEvent
from BLE import BleClient
from EventHandlerFactory import eventFactory
from FileHandler import FileHandler
from PersonalBinApi import PersonalBinApi
from HttpRequestFileHandler import HttpRequestFileHandler
from datetime import datetime
# will change it later on to factory pattern for supporting windows
# hehehehehe :))
from ClipboardFileFetcher import ClipboardFilesFetcherMacOs
'''
self.clipboardEventListener.subscribe()
emits ble event write charactersistics which notifies android for this 

when we recieve from android we use onrecive of the ble
onrecive simply 
'''

CLIPBOARD_CONTENT_FILE_NAME = "text.txt"

class Daemon2:
  def __init__(self):
    self.clipboardEventListener = ClipboardEvent(1)
    self.key = Key()
    self.cookie = None
    self.bleClient = BleClient(SERVICE_UUID)
    self.api = None
  
  async def initalize(self):
    await self.key.initialize()
    self.api = PersonalBinApi()
    self.api.set_cookie(self.key.getKeyValue())
    await self.connectBleDevice()
    self.setupBleCallbacks()
    self.setupOnChangeClipboard()
    asyncio.create_task(self.clipboardEventListener.start())
    while True:
      if self.bleClient.isConnected() == False:
        # can retry conntection after this condition is false
        print("Connection Dropped",datetime.now().time)
      await asyncio.sleep(15)
  
  async def connectBleDevice(self):
    await self.bleClient.connect()
    asyncio.create_task(self.bleClient.start_notifications())
  
  #focus on this for watching callbacks
  def setupBleCallbacks(self):
    def fromAndroidToLaptop(event):
      print("Android to laptop")
      handler = eventFactory(event,self.api)
      asyncio.create_task(handler.execute())
    self.bleClient.on_receive(UUID_NOTIFY,fromAndroidToLaptop)
  
  async def __saveClipBoardContentAndUpload(self,clipboardValue):
        fileHandler = FileHandler(CLIPBOARD_CONTENT_FILE_NAME)
        fileHandler.write_to_file(clipboardValue)
        response = await self.api.get_upload_link_clipboard()
        httpFileHandler = HttpRequestFileHandler()
        await httpFileHandler.upload(response['link'],CLIPBOARD_CONTENT_FILE_NAME)
  
  async def __getFileLocationAndUpload(self,fileLocation,fileName):
        response = await self.api.get_upload_link_storage(fileName= fileName)
        print(response)
        httpFileHandler = HttpRequestFileHandler()
        await httpFileHandler.upload(response['link'],fileLocation)
  async def handleClipboardEvent(self,clipboardValue):
    print(clipboardValue)
    await self.__saveClipBoardContentAndUpload(clipboardValue)
    asyncio.create_task(self.bleClient.emit(UUID_WRITE, "CLIPBOARD"))

  async def handleStorageEvent(self,fileLocation, fileName):
    print(fileLocation)
    await self.__getFileLocationAndUpload(fileLocation=fileLocation,fileName=fileName)
    asyncio.create_task(self.bleClient.emit(UUID_WRITE, "STORAGE"))

  def setupOnChangeClipboard(self):
    async def clipboardChanged(clipboardValue):
      
      fileChecker = ClipboardFilesFetcherMacOs()
      isFile, filePath = fileChecker.isFile(clipboardValue)
      if isFile == True:
        await self.handleStorageEvent(filePath,clipboardValue)
      else:
        await self.handleClipboardEvent(clipboardValue)
    self.clipboardEventListener.subscribe(clipboardChanged)

async def intMain():
  daemon = Daemon2()
  await daemon.initalize()

asyncio.run(intMain())
  
    
  
  