'''
=============
|  Driver   |
|   Code    | 
=============
'''

# import asyncio
# from bleak import BleakScanner, BleakClient

# SERVICE_UUID = "0ce78b36-0c84-43eb-8244-000000000000"
# UUID_NOTIFY = "0ce78b36-0c84-43eb-8244-000000000001"
# UUID_WRITE  = "0ce78b36-0c84-43eb-8244-000000000002"

from ClipMonitor import Clipboard
from Key import Key
import asyncio
import os
import aiohttp
import aiofiles
from dotenv import load_dotenv
import requests
load_dotenv()

class Daemon:
    def __init__(self):
        self.clipboard = Clipboard()
        self.key = Key()

    async def handleFile(self, resp):
        if resp.status == 200:
            filename = "text.txt"

            async with aiofiles.open(filename, 'wb') as f:
                while True:
                    chunk = await resp.content.read(1024)
                    if not chunk:
                        break
                    await f.write(chunk)

            async with aiofiles.open(filename, 'r') as f:
                content = await f.read()

            self.clipboard.copy(await self.clipboard.readFromFile())


    async def initalize(self):
        await self.key.initialize()
        self.payload = {
         "fileName":"text.txt"
        }
        self.cookie = {
         "token":f"{self.key.getKeyValue()}"
        }

    async def poll(self):

      link = None
      
      try:
          async with aiohttp.ClientSession() as session:
              async with session.get(os.getenv("BACKEND_URL"), cookies=self.cookie) as response:
                  if response.status == 200:
                      data = await response.json()
                      link = data["link"]
                  else:
                      print(f"Error {response.status}: {await response.text()}")
                  
                  if(link != None):
                    async with session.get(link) as resp:
                       await self.handleFile(resp)
      except aiohttp.ClientError as e:
          print(f"Request failed: {e}")

    async def uploadContent(self):
      async with aiohttp.ClientSession() as http_session:
        link = ""
        data = ""
        async with http_session.post(os.getenv("BACKEND_URL"),json=self.payload, cookies=self.cookie) as response:
           if(response.status != 404):
                link = await response.json( )
                link = link["link"]
                with open("text.txt","r") as file:
                    data += file.read()
                async with http_session.put(link,data=data) as response:
                    print(response.status)
           else:
               print("Link is not valid")
    async def mainLoop(self):
      while True:
          await asyncio.sleep(3)
          if(self.clipboard.isChanged()):
            # requests.delete(os.getenv("BACKEND_URL"))
            self.clipboard.saveToFile()
            await self.uploadContent()
          else:
            await self.poll()
          

async def main():
    daeomon = Daemon()
    await daeomon.initalize()
    await daeomon.mainLoop()

asyncio.run(main())
