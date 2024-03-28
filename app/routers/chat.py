from fastapi import Depends, HTTPException, APIRouter
from app.database.proxy import DatabaseProxy
from app.models import ChatRecord, Chat
from typing import Annotated
from app.dependencies import database_proxy, get_cids, get_chat_ids, get_current_uid
from typing import Any
import app.common.glm as glm
from typing import List, Union
from app.common.error import ErrorV2
import app.common.error as error
from typing import Optional
from app.model.chat import ChatCreateResponse, ChatDeleteResponse, ChatAppendResponse, ChatSelectResponse

router = APIRouter()


# /chat/create
@router.post("/chat/create")
async def create_chat(
        cid: int,
        db: Annotated[DatabaseProxy, Depends(dependency=database_proxy)],
        current_uid: int = Depends(dependency=get_current_uid)
) -> ChatCreateResponse:
    err, uids = db.get_uids_by_cid(cid)
    if uids is None or current_uid not in uids or not err.is_ok():
        err, chat_id = db.create_chat(cid, current_uid)
        if err.is_ok():
            return ChatCreateResponse(code=err.code, message=err.message, data=chat_id)
        else:
            return ChatCreateResponse(code=err.code, message=err.message, data=None)
    else:
        return ChatCreateResponse(code=err.code, message=err.message, data=None)


# /chat/delete
@router.post("/chat/delete")
async def delete_chat(
        chat_id: int,
        db: Annotated[DatabaseProxy, Depends(dependency=database_proxy)],
) -> ChatDeleteResponse:
    err = db.delete_chat_by_chat_id(chat_id)
    return ChatDeleteResponse(code=err.code, message=err.message)


# /chat/append
@router.post("/chat/append")
async def append_chat(
        character_name: str,
        character_info: str,
        chat_id: int,
        content: str,
        db: Annotated[DatabaseProxy, Depends(dependency=database_proxy)],
) -> ChatAppendResponse:
    # 这里是不是应该考虑是否这是用户第一次与该角色对话的情况？第一次对话的情况下，chat_id是不存在的
    # 创建ChatRecord对象
    err, chat = db.get_chat_by_chat_id(chat_id)
    if not err.is_ok() or chat is None:
        return ChatAppendResponse(code=err.code, message=err.message, data=None)
    # 这里的history包含当前对话的所有信息，包括user和character，是一个list[dict]
    response, history = glm.invoke_model_api(character_name, character_info, content)
    for record in history:
        who = record["role"]
        message = record["content"]
        err = db.update_chat_by_chat_id(chat_id,ChatRecord(who=who,message=message))
        if not err.is_ok():
            return ChatAppendResponse(code=err.code, message=err.message, data=None)
    return ChatAppendResponse(code=err.code,message=err.message,data=response)


# /chat/select
@router.get("/chat/select")
async def select_chat(
        db: Annotated[DatabaseProxy, Depends(dependency=database_proxy)],
        chat_ids: Optional[List[int]] = get_chat_ids(),
        cids: Optional[List[int]] = get_cids(),
        # 从第几个开始
        offset: Optional[int] = 0,
        # 一共返回多少个
        limit: Optional[int] = 1,
        chat_history_offset: Optional[int] = 0,
        chat_history_limit: Optional[int] = 1,
) -> ChatSelectResponse:
    chat_list = []
    for chat_id, cid in zip(chat_ids, cids):
        err, chat = db.get_chat_by_chat_id_cid(chat_id, cid)
        if err.is_ok():
            chat_list.append(chat)
        else:
            return ChatSelectResponse(code=err.code, message=err.message, data=[])
    part_chat_list = chat_list[offset:offset + limit]
    for chat in part_chat_list:
        chat.chat_history = chat.chat_history[chat_history_offset:chat_history_offset + chat_history_limit]
    return ChatSelectResponse(code=0, message="ok", data=part_chat_list)





# # /chat/select
# @router.get("/chat/select")
# async def select_chat_record(
#     cid: int,
#     token: str,
#     db: Annotated[InheritDataBaseProxy, Depends(dependency=database_proxy)],
# ) -> dict[str, Union[int, str, List[dict]]]:
#     ErrorCodeV2, chat_id_list = db.get_chat_id_list_by_cid(cid)
#     if ErrorCodeV2.ok():
#         return {"code": 200, "message": "Success", "data": [{"chat_id_list":chat_id_list}]}
#     else:
#         return {"code": 500, "message": "Failed to select chat record", "data": []}


# # /chat/select
# @router.get("/chat/select")
# async def select_chat_record(
#     chat_id: int,
#     db: Annotated[InheritDataBaseProxy, Depends(dependency=database_proxy)],
# ) -> dict[str, Union[int, str, List[dict]]]:
#     ErrorCodeV2, chat_history = db.get_chat_history_by_chat_id(chat_id)
#     if ErrorCodeV2.ok():
#         return {"code": 200, "message": "Success", "data": [{"chat_history":chat_history}]}
#     else:
#         return {"code": 500, "message": "Failed to select chat record", "data": []}
