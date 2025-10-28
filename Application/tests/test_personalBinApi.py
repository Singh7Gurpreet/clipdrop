import Ubuntu.PersonalBinApi as PersonalBinApi
import pytest

@pytest.fixture
def apiObject():
  return PersonalBinApi()

@pytest.mark.asyncio
async def test_get_key(apiObject):
  data = await apiObject.get_key({})  
  assert(data == None)
  
@pytest.mark.asyncio
async def test_get_upload_link_clipboard(apiObject):
  data = await apiObject.get_upload_link_clipboard()
  assert(data ==None)
  
@pytest.mark.asyncio
async def test_is_jwt_verified(apiObject):
  data = await apiObject.is_jwt_verified()
  assert(data == False)
  