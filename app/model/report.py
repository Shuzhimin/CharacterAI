from app.model.common import CommonResponse
from app.models import User
from pydantic import BaseModel, Field
from app.model.common import TokenData
from datetime import datetime


class ReportRequest(BaseModel):
    content: str = Field(..., description="发送给模型的内容")

class ReportResponse(CommonResponse):
    data: dict[str, str] | None = None