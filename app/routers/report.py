from fastapi import Depends, HTTPException, APIRouter
from fastapi.responses import FileResponse
from app.models import Character, ChatRecord
from typing import Annotated
from app.dependencies import database_proxy
from typing import List, Union
from app.common import image_to_url
import app.common.glm as glm
from app.common.error import ErrorV2, ErrorCode
import os

router = APIRouter()


@router.post("/character/report")
async def report_form(content: str):
    try:
        glm.invoke_report(content)
    except:
        raise HTTPException(status_code=500, detail="GLM-4 call failed")
    # 将生成的图片转成url
    try:
        image_to_url.upload_file(image_path="app/common/character_form.png")
        url = image_to_url.get_url()
    except:
        raise HTTPException(status_code=500, detail="File not found or bucket error")

    if not os.path.exists("app/common/character_form.png"):
        err = ErrorV2(ErrorCode.NOT_IDEAL_RESULTS, message="GLM-4 did not provide ideal results")
        return {
            "code": err.code,
            "message": err.message,
            "data": []
        }
    err = ErrorV2(ErrorCode.OK, message="Report generated successfully")
    return {
        "code": err.code,
        "message": err.message,
        "data": [
            {"report_url": url}
        ]
    }
