from fastapi import Depends, HTTPException, APIRouter
from app.database.proxy import DatabaseProxy
from app.models import Character, ChatRecord
from typing import Annotated
from app.dependencies import database_proxy
from typing import Any
import app.common.glm as glm

router = APIRouter()

# /user/login
# /user/create
# /user/delete
# /user/update
# /user/select
# /user/me
