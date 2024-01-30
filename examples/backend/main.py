import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict

# 定义Bot模型
class Bot(BaseModel):
    bot_name: str
    bot_info: str
    user_name: str
    user_info: str

    def delete(self, bot_name: str):
        global bots
        bots = [bot for bot in bots if bot.bot_name != bot_name]

bots = [
    Bot(bot_name="Alice", bot_info="This is Alice, a helpful bot.",user_name="xiao ming",user_info="我很开心"),
    Bot(bot_name="Bob", bot_info="This is Bob, a friendly bot.",user_name="xiao hong",user_info="我不高下"),
]


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
    return [bot.bot_name for bot in bots]

# 获取机器人信息
@app.get('/character/query')
async def get_character(bot_name: str):
    bot = next((bot for bot in bots if bot.bot_name == bot_name), None)
    if bot:
        return {"bot_name": bot.bot_name, "bot_info": bot.bot_info, "user_name": bot.user_name, "user_info": bot.user_info}
    else:
        return {"error": f"Bot with name '{bot_name}' not found"}

# 删除机器人
@app.delete('/character/delete')
async def delete_character(bot_name: str):
    # 查找要删除的机器人
    bot_to_delete = next((bot for bot in bots if bot.bot_name == bot_name), None)
    if bot_to_delete:
        # 调用Bot模型的delete方法删除bot
        bot_to_delete.delete(bot_name)
        return {"success": True}
    else:
        raise HTTPException(status_code=404, detail=f"Bot with name '{bot_name}' not found")

# 运行FastAPI服务
if __name__ == "__main__":
    uvicorn.run(app="main:app", host='127.0.0.1', port=8000, reload=True, workers=1)
