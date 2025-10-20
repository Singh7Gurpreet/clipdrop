import httpx
from dotenv import load_dotenv
from CustomExceptions import JWTKeyNotFound
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
  
  async def initializeKey(self):
    self.key = Key()
    await self.key.initialize()
  
  async def get_key(self,param: dict):
      url = os.getenv("BACKEND_URL_GETKEY")
      async with httpx.AsyncClient() as client:
          response = await client.get(url, params=param)
          if(response.status_code == 200):
            data = json.loads(response.text)
            return data['token']
          else:
            return None
  async def _request(self, url_env: str, method: str, payload: dict | None = None):
    if self.cookie is None:
        raise JWTKeyNotFound()

    url = os.getenv(url_env)
    async with httpx.AsyncClient() as client:
        if method.lower() == "post":
            response = await client.post(url, json=payload, cookies=self.cookie)
        elif method.lower() == "get":
            response = await client.get(url, cookies=self.cookie)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        return response.json()
  
  async def get_upload_link_clipboard(self):
    return await self._request("BACKEND_URL_CLIPBOARD", "post", self.payLoadForClipBoard)

  async def get_download_link_clipboard(self):
      return await self._request("BACKEND_URL_CLIPBOARD", "get")

  async def get_upload_link_storage(self, fileName):
      payLoadForStorage = {
        "fileName":f"{fileName}"
      }
      return await self._request("BACKEND_URL_STORAGE", "post", payLoadForStorage)

  async def get_download_link_storage(self):
      return await self._request("BACKEND_URL_STORAGE", "get")


  async def is_jwt_verified(self):
     url = os.getenv("BACKEND_VERIFY_JWT_URL")
     async with httpx.AsyncClient() as client:
       response = await client.get(url,cookies=self.cookie)
       return response.status_code == 200
    