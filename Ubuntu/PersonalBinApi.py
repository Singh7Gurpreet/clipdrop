import httpx
from dotenv import load_dotenv
import os
import json

# Load the .env file
load_dotenv()

class PersonalBinApi:
  def __init__(self):
    self.key = None
    self.cookie = None
    self.payLoadForClipBoard = {
      "fileName":"text.txt"
    }
  
  def set_cookie(self,key):
    self.cookie = {
         "token":f"{key}"
        }
  
  async def get_key(self,param: dict):
      url = os.getenv("BACKEND_URL_GETKEY")
      async with httpx.AsyncClient() as client:
          response = await client.get(url, params=param)
          if(response.status_code == 200):
            data = json.loads(response.text)
            return data['token']
          else:
            return None
  
  async def get_upload_link_clipboard(self):
      url = os.getenv("BACKEND_URL")
      async with httpx.AsyncClient() as client:
        response = await client.post(url,json = self.payLoadForClipBoard, cookies = self.cookies)
        return response

  async def is_jwt_verified(self):
     url = os.getenv("BACKEND_VERIFY_JWT_URL")
     async with httpx.AsyncClient() as client:
       response = await client.get(url,cookies=self.cookie)
       return response.status_code == 200
    