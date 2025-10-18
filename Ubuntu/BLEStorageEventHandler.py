from EventsHanlder import Event

class BLEStorageEventHandler(Event):
    def execute(self):
        print("Perform action on receiving this StorageEvent from android")