from fastapi import Depends, HTTPException, APIRouter
from app.common.conf import conf
from app.database.proxy import DatabaseProxy
from app.model.character import  CharacterAvatarResponse, CharacterDeleteRequests, CharacterDeleteResponse, CharacterSelectRequests, CharacterSelectResponse,  CharacterUpdateReceive, CharacterUpdateResponse, CreateCharacterrResponse
from app.models import Character, CharacterWhere, ChatRecord, CharacterV2, CharacterCreate, CharacterUpdate
from typing import Annotated, Union, List
from app.dependencies import database_proxy, get_current_uid
from typing import Any
import app.common.glm as glm
import app.database.pgsql as pg
from app.common.error import ErrorV2, character_already_exists, character_not_found, ok, unknown
from zhipuai import ZhipuAI

router = APIRouter()


# # 获取机器人名称列表
# @router.get(path="/names/query")
# async def get_bot_names(
#     db: Annotated[DatabaseProxy, Depends(dependency=database_proxy)]
# ) -> dict[str, list[str]]:
#     error, characters = db.get_all_characters()
#     # if not error.ok() or characters is None:
#     #     # TODO: do some logging
#     #     pass
#     return {"bot_names": [character.bot_name for character in characters]}


# # 根据机器人名称查询机器人信息
# @router.get(path="/character/query")
# async def query_character_info(
#     bot_name: str,
#     db: Annotated[DatabaseProxy, Depends(dependency=database_proxy)],
# ) -> dict[str, str]:
#     error, character = db.get_character_by_botname(botname=bot_name)
#     if not error.ok() or character is None:
#         raise HTTPException(status_code=404, detail=f"'{bot_name}' not found")
#     return character.dump_character_info_without_chat_history()


# 删除机器人 接口1.2 删除角色 /character/delete
@router.post(path="/character/delete")
async def delete_character(
    cids: CharacterDeleteRequests, db: Annotated[DatabaseProxy, Depends(dependency=database_proxy)]
) -> CharacterDeleteResponse:
    for cid in cids.cids:
        cw =CharacterWhere(cid=cid)
    #         err = pg.delete_chat(where=ChatWhere(cid=cid))
    # assert err.is_ok()
    # err = pg.delete_user_character(where=UserCharacterWhere(cid=cid))
    # assert err.is_ok()
    # err = pg.delete_character(where=CharacterWhere(cid=cid))
    # assert err.is_ok()
        res = pg.select_character(cw)
        if res == []:
            err = character_not_found()
            return CharacterDeleteResponse(
                code=err.code,message=err.message,data=[]
                            )
        res = pg.delete_chat(cw)
        if res.code != 0:
            return CharacterDeleteResponse(
                code=res.code,message=res.message,data=[]
            )
        res = pg.delete_user_character(cw)
        if res.code != 0:
            return CharacterDeleteResponse(
                code=res.code,message=res.message,data=[]
            )
        res = pg.delete_character(cw)   #(where: CharacterWhere) -> ErrorV2:
        if res.code != 0:
            return CharacterDeleteResponse(
                code=res.code,message=res.message,data=[]
            )
    return CharacterDeleteResponse(
                code=res.code,message=res.message,data=[]
            )
    if res.ErrorCode == 1:
        res.unknown()
        return {'code':res.code, 'message':res.message , 'data':[]}
    #err = db.delete_character_by_botname(cid=cid)
    return CharacterDeleteResponse(
        code=res.code, message=res.message, data=[]
    )
    # return {"code": res.code, "message": res.message, "data": []}
    # return {"code": 0, "message": "ok", "data": [{"cid": cid}]}

#接口1.3 修改角色 /character/update  功能描述：对已创建的角色进行修改，用户只能修改自己创建的角色，不能修改管理员创建的角色，管理员可以修改任意角色。
@router.post(path="/character/update")
async def update_character_info(
    character: CharacterUpdateReceive,
    db: Annotated[DatabaseProxy, Depends(dependency=database_proxy)],
) -> CharacterUpdateResponse:
 #def update_character(update: CharacterUpdate, where: CharacterWhere) -> ErrorV2:
#    class UserCharacterWhere(BaseModel):
#     uid: int | None = None
#     cid: int | None = None
#     status: str | None = None    
#  class CharacterUpdate(BaseModel):
#     character_name: str | None = None
#     character_info: str | None = None
#     character_class: str | None = None
#     avatar_url: str | None = None
#     status: str | None = None
#     attr: str | None = None   
    # class CharacterUpdatReceive(BaseModel):
    # cid: int = Field(default=..., description="角色id")
    # character_name :str =None
    # character_info : str= None
    # avatar: str = None
    # character_class : str = None
    err = pg.select_character(where=CharacterWhere(cid=character.cid))
    if err == []:
        err = character_not_found()
        return  CharacterSelectResponse(
            code=err.code,message=err.message,data=[]
        )
    #def update_character(update: CharacterUpdate, where: CharacterWhere) -> ErrorV2:
    err = pg.update_character(update=CharacterUpdate(character_name=character.character_name,
                                                     character_info=character.character_info,
                                                     avatar_url=character.avatar,
                                                     character_class=character.character_class),
                            where=CharacterWhere(cid=character.cid))
    return CharacterUpdateResponse(code=err.code,message=err.message,data=[])


#接口1.6 角色头像生成 /character/avatar  接口1.4 1.5废弃
@router.post(path="/character/avatar")
async def generate_avatar(
    db: Annotated[DatabaseProxy, Depends(dependency=database_proxy)],
    avatar_describe: str,
) -> CharacterAvatarResponse:

    # zhipu = ZhipuAIConf(api_key ="755df9e04db5af2413e62d31ac7f0cf8.gxnvQ2oNCTYPJDQh")
    client = ZhipuAI(api_key="755df9e04db5af2413e62d31ac7f0cf8.gxnvQ2oNCTYPJDQh")  # 请填写您自已的APIKey

    response = client.images.generations(
        model="cogview-3",
        prompt=avatar_describe, )
    
    if response.data[0].url != None:
        err = ok()
        return CharacterAvatarResponse(
        code=err.code, message= err.message, data=[response.data[0].url]
    )
    else:
        err = unknown()
        return CharacterAvatarResponse(
        code=err.code, message= err.message, data=[]
    )
    


#接口1.7 查询角色信息 /character/select
#select_character(where: CharacterWhere) -> list[CharacterV2]:
@router.post(path="/character/select")
async def character_select(
    db: Annotated[DatabaseProxy, Depends(dependency=database_proxy)],
    character: CharacterSelectRequests
) -> CharacterSelectResponse:#这里有问题  一个和多个
    #characterwhere = CharacterWhere(cid=character.cids)
# class CharacterSelectRequests(BaseModel):
#     cids : list[int]  =None
#     offset : int  = 0
#     limit : int  =1
#     ascend : bool =True
    
# class CharacterWhere(BaseModel):
#     cid: int | None = None
#     character_name: str | None = None
#     character_class: str | None = None
#     status: str | None = None
#     attr: str | None = None

    # pg.select_character()
    # err, character = db.character_select1(cids,offset,limit,acsend)
    # return {"code": err.code, "message": err.message, "data": []}
    cv2=[]
    if character.cids is None or not character.cids:
        characterwhere = CharacterWhere()
        print('11111111111111111111')
        characterv2 = pg.select_character(characterwhere)
        cv2=characterv2
    else:
        for cid in character.cids:
            characterwhere = CharacterWhere(cid=cid)
            characterv2 = pg.select_character(characterwhere)
            for item in characterv2:
                cv2.append(item)
    print(character.ascend)
    cv2.sort(key=lambda x: x.cid,reverse=character.ascend)
    #cv2.sort(key=character.cids , reverse=character.ascend)
    res = cv2[character.offset:character.offset+character.limit]
    return  CharacterSelectResponse(
        code=0, message='ok', data=res
    )



    #     class CharacterV2(BaseModel):
    # cid: int = Field(default=..., description="机器人id")
    # character_name: str = Field(default=..., description="机器人名称")
    # character_info: str = Field(default=..., description="机器人信息")
    # character_class: str = Field(default=..., description="机器人类型")
    # avatar_url: str = Field(default=..., description="头像url")
    # create_time: datetime = Field(default=..., description="创建时间")
    # update_time: datetime = Field(default=..., description="更新时间")
    # status: str = Field(default=..., description="状态")
    # attr: str = Field(default=..., description="属性")



#文档写的是根据机器人id来更新，这里占用了路径  注释掉
# 根据机器人名称更新机器人信息
# @router.post(path="/character/update")
# async def update_character_info(
#     character: Character,
#     db: Annotated[DatabaseProxy, Depends(dependency=database_proxy)],
# ) -> dict[str, bool]:
#     return {"success": db.update_character(character=character).ok()}


# 创建机器人信息 接口1.1 创建角色 /character/create  自己完成，等给他们看看
@router.post(path="/character/create")
async def create_character(
    character: CharacterCreate,
    db: Annotated[DatabaseProxy, Depends(dependency=database_proxy)],
) -> CreateCharacterrResponse:
    #err = db.create_character(character=character)
    #select_character(where: CharacterWhere) -> list[CharacterV2]
# class CharacterWhere(BaseModel):
#     cid: int | None = None
#     character_name: str | None = None
#     character_class: str | None = None
#     status: str | None = None
#     attr: str | None = None
    # class CharacterV2(BaseModel):
    # cid: int = Field(default=..., description="机器人id")
    # character_name: str = Field(default=..., description="机器人名称")
    # character_info: str = Field(default=..., description="机器人信息")
    # character_class: str = Field(default=..., description="机器人类型")
    # avatar_url: str = Field(default=..., description="头像url")
    # create_time: datetime = Field(default=..., description="创建时间")
    # update_time: datetime = Field(default=..., description="更新时间")
    # status: str = Field(default=..., description="状态")
    # attr: str = Field(default=..., description="属性")

# class CharacterCreate(BaseModel):
#     character_name: str = Field(default=..., description="机器人名称")
#     character_info: str = Field(default=..., description="机器人信息")
#     character_class: str = Field(default=..., description="机器人类型")
#     avatar_url: str = Field(default=..., description="头像url")
#     status: str = Field(default="active", description="状态")
#     attr: str = Field(default="normal", description="属性")
    
    
    characterwhere = CharacterWhere()
    characterwhere.character_name = character.character_name
    res = pg.select_character(characterwhere)
    print(characterwhere)
    print(res)
    if res != []:
        print('11111111111111111111111')
        err = character_already_exists()
        return CreateCharacterrResponse(
            code=err.code , message=err.message , data=[]
        )



    uid = get_current_uid()
    if uid == "管理员uid":
        character.attr = character.attr
    else:
        character.attr = "Normal"
    err = pg.create_character(character)
    return CreateCharacterrResponse(
        code=err.code, message=err.message, data=[]
    )


# # 聊天
# @router.post(path="/character/chat")
# async def chat(
#     bot_name: str,
#     content: str,
#     db: Annotated[DatabaseProxy, Depends(dependency=database_proxy)],
# ) -> dict[str, Any]:
#     error, character = db.get_character_by_botname(botname=bot_name)
#     if not error.ok() or character is None:
#         return {
#             "success": "fail",
#             "content": "character not found",
#             "chat_history": [],
#         }
#
#     character.chat_history.append(ChatRecord(who="user", message=content))
#     response = glm.invoke_character_glm_api(character=character)
#     content = glm.get_content_from_response(response=response)
#     character.chat_history.append(ChatRecord(who="assistant", message=content))
#     db.update_character(character=character)
#     return {
#         "success": response["success"],
#         "content": response["data"]["choices"][0]["content"],
#         "chat_history": character.dump_chat_history(),
#     }
