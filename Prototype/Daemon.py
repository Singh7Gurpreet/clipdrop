'''
=============
|  Driver   |
|   Code    | 
=============
'''

from ClipMonitor import Clipboard
from Key import Key
import asyncio
import os
import aiohttp
from dotenv import load_dotenv
load_dotenv()

class Daemon:
    def __init__(self):
        self.clipboard = Clipboard()
        self.key = Key()
    
    async def initalize(self):
        await self.key.initialize()
        self.payload = {
         "fileName":"temp.txt"
        }
        self.cookie = {
         "token":f"{self.key.getKeyValue()}"
        }

    async def poll(self):
      try:
          async with aiohttp.ClientSession() as session:
              async with session.get(os.getenv("BACKEND_URL"), cookies=self.cookie) as response:
                  if response.status == 200:
                      data = await response.json()
                      print("Success:", data)
                  else:
                      print(f"Error {response.status}: {await response.text()}")
                      pass
      except aiohttp.ClientError as e:
          print(f"Request failed: {e}")

    async def uploadContent(self):
      async with aiohttp.ClientSession() as http_session:
        link = ""
        data = ""
        async with http_session.post(os.getenv("BACKEND_URL"),json=self.payload, cookies=self.cookie) as response:
           link = await response.json()
           link = link["link"]
        with open("temp.txt","r") as file:
           data += file.read()
        async with http_session.put(link,data=data) as response:
           pass

    async def mainLoop(self):
      while True:
          await asyncio.sleep(3)
          if(self.clipboard.isChanged()):
            self.clipboard.saveToFile()
            await self.uploadContent()
          else:
             self.poll()
          


async def main():
    daeomon = Daemon()
    await daeomon.initalize()
    await daeomon.mainLoop()

asyncio.run(main())
