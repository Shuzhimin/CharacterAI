
from pydantic import BaseModel, Field
from app.model.common import TokenData
from app.model.common import CommonResponse


class CreateCharacterrResponse(CommonResponse):
    data: list = []

class CharacterDeleteResponse(CommonResponse):
    data: list = []

class CharacterDeleteRequests(BaseModel):
    cids: list[int] = Field(..., description="角色id")

class CharacterUpdateResponse(CommonResponse):
    data:list= []

class CharacterAvatarResponse(CommonResponse):
    data: list=[]

class CharacterSelectRequests(BaseModel):
    cids : list[int]  =None
    offset : int  = 0
    limit : int  =1
    ascend : bool =True

class CharacterSelectResponse(CommonResponse):
    data:list = None
     #return: [{ character_name, character_info, avatar, character_class }]
    
class CharacterUpdateReceive(BaseModel):
    cid: int = Field(default=..., description="角色id")
    character_name :str =None
    character_info : str= None
    avatar: str = None
    character_class : str = None

class CharacterUpdateResponse(CommonResponse):
    data:list=[]


