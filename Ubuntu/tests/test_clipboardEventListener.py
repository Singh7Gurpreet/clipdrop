import Ubuntu.ClipboardEventListener as ClipboardEventListener
import os
import pytest

#Difficult to test
# would proceed with main file testing

async def test_get_key(apiObject):
  clipEventHandler = ClipboardEventListener() 
  clipEventHandler.subscribe(lambda str: print(str))
  