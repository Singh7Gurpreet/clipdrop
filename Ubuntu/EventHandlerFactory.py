from BLEClipboardEventHandler import BLEClipboardEventHandler
from BLEStorageEventHandler import BLEStorageEventHandler
from EventsHandler import *

def eventFactory(event: Events) -> EventHandler:
    if event == Events.CLIPBOARD_DATA.value:
        return BLEClipboardEventHandler()
    elif event == Events.STORAGE_DATA.value:
        return BLEStorageEventHandler()
    else:
        raise ValueError(f"Unknown event type: {event}")
