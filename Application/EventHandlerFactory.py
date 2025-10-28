from BLEClipboardEventHandler import BLEClipboardEventHandler
from BLEStorageEventHandler import BLEStorageEventHandler
from EventsHandler import *

def eventFactory(event: Events, api :PersonalBinApi) -> EventHandler:
    if event == Events.CLIPBOARD_DATA.value:
        return BLEClipboardEventHandler(api)
    elif event == Events.STORAGE_DATA.value:
        return BLEStorageEventHandler(api)
    else:
        raise ValueError(f"Unknown event type: {event}")
