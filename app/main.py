import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import router
# 咱们用这种全局变量的方式实现单例吧，虽然不是最好的方式
# 但是其他的方式实现起来太麻烦了 易读性差
from app.common import conf

app = FastAPI()
app.include_router(router=router.user, tags=["user"])
app.include_router(router=router.character, tags=["character"])
app.include_router(router=router.chat, tags=["chat"])
# app.include_router(router=router.report, tags=["report"])
app.include_router(router=router.generation, tags=["generation"])
app.include_router(router=router.admin, tags=["admin"])


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
