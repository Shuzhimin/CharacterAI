from fastapi import FastAPI
from app_refactor.routers import character
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()
app.include_router(router=character.router)

# 允许跨域请求
app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0")
