'''
=============
|  Driver   |
|   Code    | 
=============
'''

# import asyncio
# from bleak import BleakScanner, BleakClient

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
  
  #To focus on for a while 2
  async def connectBleDevice(self):
    await self.bleClient.connect()
    asyncio.create_task(self.bleClient.start_notifications())
  
  def setupBleCallbacks(self):
    def fromAndroidToLaptop(event):
      print("Android to laptop")
      handler = eventFactory(event)
      asyncio.create_task(handler.execute())
    self.bleClient.on_receive(UUID_NOTIFY,fromAndroidToLaptop)
  
  async def saveClipBoardContentAndUpload(self,clipboardValue):
        fileHandler = FileHandler(CLIPBOARD_CONTENT_FILE_NAME)
        fileHandler.write_to_file(clipboardValue)
        response = await self.api.get_upload_link_clipboard()
        print(response)
        httpFileHandler = HttpRequestFileHandler()
        await httpFileHandler.upload(response['link'],CLIPBOARD_CONTENT_FILE_NAME)
    

  def setupOnChangeClipboard(self):
    def clipboardChanged(clipboardValue):
      print("🖥️ Clipboard changed, sending event to Android...")
      self.__saveClipBoardContentAndUpload(clipboardValue)
      print(clipboardValue)
      #sending event through BLE to android
      asyncio.create_task(self.bleClient.emit(UUID_WRITE, "CLIPBOARD"))
    self.clipboardEventListener.subscribe(clipboardChanged)

async def intMain():
  daemon = Daemon2()
  await daemon.initalize()

asyncio.run(intMain())
  
    
  
  