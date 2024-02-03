from fastapi import FastAPI
from app.routers import character
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(character.router)

# 允许跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
