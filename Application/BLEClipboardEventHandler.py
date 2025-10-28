from EventsHandler import EventHandler
from Key import Key
from PersonalBinApi import PersonalBinApi
from ClipMonitor import Clipboard
from HttpRequestFileHandler import HttpRequestFileHandler
from FileHandler import FileHandler
class BLEClipboardEventHandler(EventHandler):
    def __init__(self,api: PersonalBinApi):
        super().__init__(api)
    async def execute(self):
        response = await self.api.get_download_link_clipboard()
        httpRequestFileHandler = HttpRequestFileHandler()
        await httpRequestFileHandler.download(response['link'],response['fileName'])
        fileHandler = FileHandler(response['fileName'])
        content = fileHandler.read_from_file()
        Clipboard().copy(content)