from EventsHandler import EventHandler
from HttpRequestFileHandler import HttpRequestFileHandler
from FileHandler import FileHandler
from ClipMonitor import Clipboard
import os 

class BLEStorageEventHandler(EventHandler):
    def __init__(self, api):
        super().__init__(api)
        self.clipboard = Clipboard()
    async def execute(self):
        fileHandler = HttpRequestFileHandler()
        response = await self.api.get_download_link_storage()
        await fileHandler.download(link=response['link'],fileName=response['fileName'])
        self.clipboard.saveFileToClipboard(response['fileName'])