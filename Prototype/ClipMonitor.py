import pyperclip
import time

last_clipboard = ""

print((time.time_ns() // 1_000_000),1747632174512,sep="\n")
# while True:
#     current_clipboard = pyperclip.paste()
#     if current_clipboard != last_clipboard:
#         print(f"📋 New Clipboard Content: {current_clipboard}")
#         last_clipboard = current_clipboard
#     time.sleep(1)  # check every 1 second
