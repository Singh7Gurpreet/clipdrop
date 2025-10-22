from EventsHandler import EventHandler
from Key import Key
from PersonalBinApi import PersonalBinApi
from ClipMonitor import Clipboard
from HttpRequestFileHandler import HttpRequestFileHandler
from FileHandler import FileHandler

class BLEClipboardEventHandler(EventHandler):
    async def execute(self):
        #Can be moved to EventHandler to prevent code duplication
        #BEGIN
        jwtToken = Key()
        await jwtToken.initialize()
        api = PersonalBinApi()
        api.set_cookie(jwtToken.getKeyValue())
        #END
        response = await api.get_download_link_clipboard()
        httpRequestFileHandler = HttpRequestFileHandler()
        await httpRequestFileHandler.download(response['link'],response['fileName'])
        fileHandler = FileHandler(response['fileName'])
        content = fileHandler.read_from_file()
        Clipboard().copy(content)