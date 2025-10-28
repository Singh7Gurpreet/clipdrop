from AppKit import NSPasteboard
from Foundation import NSURL
from abc import ABC, abstractmethod

# it is a abstract parent class that is inherited by 
# required os for 
class ClipboardFileFetcher(ABC):
  def __get_clipboard_files(self)->list[str]:
    pass
  
  def isFile(self, filePath: str) -> tuple[bool, str]:
    pass

class ClipboardFilesFetcherMacOs(ClipboardFileFetcher):
  def __get_clipboard_files(self) -> list[str]:
      pb = NSPasteboard.generalPasteboard()
      urls = pb.readObjectsForClasses_options_([NSURL], None)
      if urls:
          return [str(url.path()) for url in urls]
      return []
  
  # Return Value : [isFile:boolean, AbsolutefilePath: string]
  def isFile(self, filePath: str) -> tuple[bool, str]:
    files = self.__get_clipboard_files()
    if len(files) != 1:
        return (False, "")
    print(files[0])
    if filePath in files[0]:
        return (True, files[0])
    else:
        return (False, "")