# 2024/3/7
# zhangzhong
# common response model

from pydantic import BaseModel, Field


class CommonResponse(BaseModel):
    code: int = Field(..., description="response code")
    message: str = Field(..., description="response message")
