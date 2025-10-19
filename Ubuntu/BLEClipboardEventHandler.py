from EventsHandler import EventHandler
from Key import Key
from PersonalBinApi import PersonalBinApi

class BLEClipboardEventHandler(EventHandler):
    async def execute(self):
        jwtToken = Key().getKeyValue()
        api = PersonalBinApi()
        api.set_cookie(jwtToken)
        response = await api.get_upload_link_clipboard()
        print("Clipboard Event Respond:", response,sep=", ",end="\n")