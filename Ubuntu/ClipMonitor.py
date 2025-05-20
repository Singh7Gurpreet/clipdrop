import pyperclip

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
    self.content = None
  
  def isChanged(self):
    result = self.content != self.getClipboardContent()
    self.content = self.getClipboardContent()
    print(self.content,result,self.getClipboardContent(),sep="\n")
    return result

  def copy(self,content):
    pyperclip.copy(content)
  
  def getClipboardContent(self):
    return pyperclip.paste()
  
  def saveToFile(self):
    with open("temp.txt","w") as file:
      file.write(self.getClipboardContent())
  
  def readFromFile(self):
    content = ""
    with open("temp.txt","r") as file:
        content += file.read()
    return content