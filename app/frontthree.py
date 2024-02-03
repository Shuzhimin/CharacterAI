import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from db import main
from db.main import get_bot_name,get_usr_bot_info,delete_bot

app = FastAPI()

# 允许跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 获取机器人名称列表
@app.get('/names/query')
async def get_bot_names():
    return [get_bot_name()]

# 获取机器人信息
@app.get('/character/query')
async def get_character(bot_name: str):
    return get_usr_bot_info(bot_name)

# 删除机器人
@app.delete('/character/delete')
async def delete_character(bot_name: str):
    return delete_bot(bot_name)

# 运行FastAPI服务
if __name__ == "__main__":
    uvicorn.run(app="frontthree:app", host='127.0.0.1', port=8000, reload=True, workers=1)
