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
import threading
import asyncio
from  ClipboardEventListener import ClipboardEvent
from BLE import BleClient
'''
self.clipboardEventListener.subscribe()
emits ble event write charactersistics which notifies android for this 

when we recieve from android we use onrecive of the ble
onrecive simply 
'''

class Daemon2:
  def __init__(self):
    self.clipboardEventListener = ClipboardEvent(1)
    self.key = Key()
    self.cookie = None
    self.bleClient = BleClient(SERVICE_UUID)
  
  async def initalize(self):
    await self.key.initialize()
    self.cookie = {
      "token":f"{self.key.getKeyValue()}"
    }
    await self.connectBleDevice()
    self.setupBleCallbacks()
    self.setupOnChangeClipboard()
    asyncio.create_task(self.clipboardEventListener.start())
    while True:
      if self.bleClient.isConnected() == False:
        print("Connection Dropped")
      await asyncio.sleep(1)
  
  #To focus on for a while 2
  async def connectBleDevice(self):
    await self.bleClient.connect()
    asyncio.create_task(self.bleClient.start_notifications())
  
  def setupBleCallbacks(self):
    def fromAndroidToLaptop(event):
      print("Data uploaded to server you can fetch from there",data)
    self.bleClient.on_receive(UUID_NOTIFY,fromAndroidToLaptop)
  
  def setupOnChangeClipboard(self):
    def clipboardChanged(clipboardValue):
      print("🖥️ Clipboard changed, sending event to Android...")
      print(clipboardValue)
      asyncio.create_task(self.bleClient.emit(UUID_WRITE, "CLIPBOARD"))
    self.clipboardEventListener.subscribe(clipboardChanged)

async def intMain():
  daemon = Daemon2()
  await daemon.initalize()

asyncio.run(intMain())
  
    
  
  