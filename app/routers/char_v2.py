# 2024/4/7
# zhangzhong

from fastapi import WebSocket, APIRouter

chat = APIRouter()


@chat.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, cid, db):
    await websocket.accept()
    uid = data
    chat = db.create_chat(cid, uid)
    while True:
        data = await websocket.receive_text()

        # insert data into db
        db.append_chat_recoards(botname="botname", chat_records=[data])

        # ask chatglm
        response, history = glm.invoke_model_api(
            character_name, character_info, content
        )

        # send answer to client
        await websocket.send_text(f"Message text was: {data}")
