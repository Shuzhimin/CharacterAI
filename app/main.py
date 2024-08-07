from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import router
from app.common import conf, model
from app.database.database import DatabaseService
from app.database.schema import init_db


def create_admin():
    db = DatabaseService()
    db.get_admin()
    db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    create_admin()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=router.user, tags=["user"])
app.include_router(router=router.character, tags=["character"])
app.include_router(router=router.chat, tags=["chat"])
app.include_router(router=router.generation, tags=["generation"])
app.include_router(router=router.admin, tags=["admin"])


app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app=app, host=conf.get_fastapi_host(), port=conf.get_fastapi_port())
