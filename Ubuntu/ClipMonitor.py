import pyperclip
import asyncio
import threading

class Clipboard:
    _instance = None
    _instance_lock = threading.Lock()   # lock for singleton creation

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._instance_lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # prevent reinitialization if instance already exists
        if hasattr(self, "_initialized") and self._initialized:
            return

        self.content = None
        self._lock = threading.Lock()
        self._suppress_next = False
        self._initialized = True  

    def isChanged(self):
        """Return True if clipboard content changed since last check."""
        with self._lock:
            if self._suppress_next:
                self._suppress_next = False
                return False

            current = pyperclip.paste()
            changed = (self.content != current and current != "")
            self.content = current
            return changed

    def copy(self, content):
        with self._lock:
            self._suppress_next = True
            self.content = content
            pyperclip.copy(content)

    def getClipboardContent(self):
        with self._lock:
            return pyperclip.paste()

    def saveToFile(self, filename="text.txt"):
        with self._lock, open(filename, "w", encoding="utf-8") as file:
            file.write(self.getClipboardContent())

    async def readFromFile(self, filename="text.txt"):
        async with asyncio.Lock():  # minor protection for async context
            with open(filename, "r", encoding="utf-8") as file:
                content = file.read()
            return content
