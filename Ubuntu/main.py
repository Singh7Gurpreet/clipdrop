import asyncio
from ClipboardEventListener import ClassBoardEvent

async def func():
    ev = ClassBoardEvent(0.5)
    ev.subscribe(lambda text: print("Clipboard changed:", text))
    await ev.start()

if __name__ == "__main__":
    asyncio.run(func())
