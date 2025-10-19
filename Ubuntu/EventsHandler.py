from abc import ABC, abstractmethod
from enum import Enum

class Events(Enum):
    STORAGE_DATA = "STORAGE_DATA"
    CLIPBOARD_DATA = "CLIPBOARD_DATA"

class EventHandler(ABC):
    @abstractmethod
    async def execute(self):
        pass
