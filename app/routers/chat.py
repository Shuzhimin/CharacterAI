from fastapi import Depends, HTTPException, APIRouter
from app.database.proxy import DatabaseProxy
from app.database.inhert_proxy import InheritDataBaseProxy
from app.models import ChatRecord, Chat
from typing import Annotated
from app.dependencies import database_proxy,get_cids,get_chat_ids
from typing import Any
import app.common.glm as glm
from typing import List, Union
from app.database.mongo import get_uid_by_cid
from app.common.error import ErrorV2
import app.common.error as error
from typing import Optional

router = APIRouter()
ChatRecord(role="user",content="你好",create_time="2022-02-02 12:12:12")

# /chat/create
@router.post("/chat/create")
async def create_chat_record(
    cid: int,
    db: Annotated[InheritDataBaseProxy, Depends(dependency=database_proxy)],
) -> dict[str, Union[int, str, List[dict]]]:
    err, uid = db.get_uid_by_cid(cid)
    if not err.is_ok() or uid is None:
    #创建Chat对象
        chat = Chat(cid=cid, uid=uid,history=[],status="normal")
        err,chat_id = db.create_chat(chat)
        if err.is_ok():
            return {"code": err.code, "message":err.message, "data": [{"chat_id": chat_id}]}
        else:
            return {"code": err.code, "message": err.message, "data": []}
    else:
        return {"code":err.code, "message":err.message, "data":[]}     

# /chat/delete
@router.post("/chat/delete")
async def delete_chat_record(
    chat_id: int,
    db: Annotated[InheritDataBaseProxy, Depends(dependency=database_proxy)],
) -> dict[str, Union[int, str, List[dict]]]:
    err = db.delete_chat_by_chat_id(chat_id)
    return {"code":err.code, "message":err.message, "data":[]}
    

# /chat/append
@router.post("/chat/append")
async def append_chat_record(
        character_name: str,
        charater_info: str,
        chat_id: int,
        content: str,
        db: Annotated[InheritDataBaseProxy, Depends(dependency=database_proxy)],
) -> dict[str, Union[int, str, List[dict]]]:
    #创建ChatRecord对象
    err,chat= db.get_chat_by_chat_id(chat_id)
    if not err.is_ok() or chat is None:
        return {"code":err.code, "message":err.message, "data":[]}  
    response,history = glm.invoke_model_api(character_name, charater_info, content)
    # 将history转为ChatRecord对象,此处的history为此次对话所有的ChatRecord，包含user的和character的
    for i in range(len(history)):
        history[i]=ChatRecord(**history[i])
    err= db.append_chat_records(chat_id, history)
    if err.is_ok():
        return {"code":err.code, "message":err.message, "data": [{"response": response}]}
    else:
        return {"code":err.code, "message":err.message, "data": []}

# /chat/select
@router.get("/chat/select")
async def select_chat_record(
    db: Annotated[InheritDataBaseProxy, Depends(dependency=database_proxy)],
    chat_ids: Optional[List[int]]=Depends(dependency=get_chat_ids),
    cids: Optional[List[int]]=Depends(dependency=get_cids),
    # 从第几个开始
    offset: Optional[int] = 0,
    # 一共返回多少个    
    limit: Optional[int] = 1,
    # 是否升序
    ascend: Optional[bool] = True,
    chat_history_offset: Optional[int] = 0,
    chat_history_limit: Optional[int] = 1,
    chat_history_ascend: Optional[bool] = True,
) -> dict[str, Union[int, str, List[dict]]]:
    chat_list = []
    for chat_id,cid in zip(chat_ids,cids):
        err, chat = db.get_chat_by_chat_id_cid(chat_id,cid)
        if err.is_ok():
            chat=Chat(**chat)
            chat_list.append(chat)
        else:
            return {"code":err.code, "message":err.message, "data": []}
    part_chat_list = chat_list[offset:offset+limit]
    part_chat_list = sorted(part_chat_list, key=lambda x: x.create_time, reverse=ascend)
    for chat in part_chat_list:
        chat.history = chat.history[chat_history_offset:chat_history_offset+chat_history_limit]
        chat.history = sorted(chat.history, key=lambda x: x.create_time, reverse=chat_history_ascend)
    return {"code": 0, "message": "OK", "data": part_chat_list}



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