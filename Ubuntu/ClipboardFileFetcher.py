from AppKit import NSPasteboard
from Foundation import NSURL
import abc

# it is a abstract parent class that is inherited by 
# required os for 
class ClipboardFileFetcher(abc):
  def get_clipboard_files()->list[str]:
    pass


class ClipboardFilesFetcherMacOs(ClipboardFileFetcher):
  def get_clipboard_files() -> list[str]:
      pb = NSPasteboard.generalPasteboard()
      urls = pb.readObjectsForClasses_options_([NSURL], None)
      if urls:
          return [str(url.path()) for url in urls]
      return []
