# 2024/3/7
# zhangzhong
# common response model

from pydantic import BaseModel, Field
from datetime import datetime


class CommonResponse(BaseModel):
    code: int = Field(..., description="response code")
    message: str = Field(..., description="response message")


class TokenData(BaseModel):
    uid: str
