import httpx
import os

class HttpRequestFileHandler:

    #For singleton design pattern we need
    # to have private instance
  __instance = None 
  
  def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(HttpRequestFileHandler, cls).__new__(cls)
        return cls.__instance

  def __init__(self):
        # Prevent re-initialization if instance already exists
        if hasattr(self, "_initialized") and self._initialized:
            return
  
  async def download(self,link,fileName):
    async with httpx.AsyncClient() as client:
        response = await client.get(link)
        response.raise_for_status()  # ✅ raises if 404, 500, etc.
        
        with open(fileName, "wb") as f:
            f.write(response.content)
        
        return os.path.abspath(fileName)
  
  async def upload(self, link, filePath):
        with open(filePath, "rb") as f:
            data = f.read()

        async with httpx.AsyncClient() as client:
            response = await client.put(link, content=data)
            response.raise_for_status()

        print(f"✅ Uploaded {os.path.basename(filePath)} successfully.")
        return response.status_code