from fastapi import Depends, HTTPException, APIRouter
from app.database.proxy import DatabaseProxy
from app.models import Character, ChatRecord
from typing import Annotated
from app.dependencies import database_proxy
from typing import Any
import app.common.glm as glm

router = APIRouter()

# /chat/create
# /chat/delete
# /chat/append
# /chat/select
