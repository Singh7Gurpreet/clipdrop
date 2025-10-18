from EventsHanlder import Event

class BLEClipboardEventHandler(Event):
    def execute(self):
        print("Perform action on receiving this clipbaordEvent from android")