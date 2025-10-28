from abc import ABC, abstractmethod
from enum import Enum
from PersonalBinApi import PersonalBinApi

class Events(Enum):
    STORAGE_DATA = "STORAGE_DATA"
    CLIPBOARD_DATA = "CLIPBOARD_DATA"

class EventHandler(ABC):
    def __init__(self, api:PersonalBinApi):
        self.api = api
    
    @abstractmethod
    async def execute(self):
        pass
