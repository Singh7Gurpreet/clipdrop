import pyperclip
import time

'''
In this python script I m going to write the code logic in this way

First there would be main async main function which will be executed
in that we will first create object key which will handle everything
related to authentication and then it will use that for sending it with cookie
now 

clipboard main loop would be just work on polling system it first checks clipboard
action that is there any change in that content if yes then store that time and content
and it will also send GET /api/file request.

Now we have three cases as following:

Case 1:
We have GET request result as 404 not found and we proceed with clipboard actions
which will send text file containg content of that clipboard in POST /api/file

Case 2:
We have got that there is no change in clipboard but we got 200 in GET /api/file
so we will fetch all content into a string and store in a clip board

'''

class Clipboard:
  def __init__(self):
    pass
  
  def copy(self,content):
    pyperclip.copy(content)
  
  def getClipboardContent(self):
    return pyperclip.paste()
  
  def saveToFile(self,content):
    with open("temp.txt","w") as file:
      file.write(content)
  
  def readFromFile(self,content):
    content = ""
    with open("temp.txt","r") as file:
        content += file.read()
    return content
  

# while True:
#     current_clipboard = pyperclip.paste()
#     if current_clipboard != last_clipboard:
#         print(f"📋 New Clipboard Content: {current_clipboard}")
#         last_clipboard = current_clipboard
#     time.sleep(1)  # check every 1 second
