from EventsHandler import EventHandler
from Key import Key

class BLEStorageEventHandler(EventHandler):
    async def execute(self):
        jwtToken = Key().getKeyValue()
        print("Perform action on receiving this StorageEvent from android")