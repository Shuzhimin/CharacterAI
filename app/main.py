from fastapi import FastAPI
from app.routers import character, user, chat, login, report
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.common.conf import conf


app = FastAPI()
app.include_router(router=character.router)
app.include_router(router=user.router)
app.include_router(router=chat.router)
app.include_router(router=report.router)
app.include_router(router=login.router)

# 允许跨域请求
app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app=app, host=conf.get_fastapi_host(), port=conf.get_fastapi_port())
