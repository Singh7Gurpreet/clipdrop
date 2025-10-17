from ClipMonitor import *
from typing import Callable
import asyncio

##Usage example 
'''
ev = ClipboardEvent(0.5)
    ev.subscribe(lambda text: print("Clipboard changed:", text))
    await ev.start()
'''

class ClipboardEvent:
    def __init__(self, interv: float):
        self.clipMonitor = Clipboard()
        self.subscribers: list[Callable[[str], None]] = []
        self.interval = interv

    def subscribe(self, callback: Callable[[str], None]):
        self.subscribers.append(callback)

    async def check_once(self):
        if self.clipMonitor.isChanged():
            value: str = self.clipMonitor.getClipboardContent()
            for subs in self.subscribers:
                subs(value)

    async def start(self):
        while True:
            await self.check_once()
            await asyncio.sleep(self.interval)
