from fastapi import Depends, HTTPException, APIRouter
from app.model.report import ReportRequest, ReportResponse
from typing import Annotated
from app.dependencies import database_proxy
from typing import List
from app.common import image_to_url
import app.common.glm as glm
from app.common import error
import os


router = APIRouter()


@router.post("/character/report")
async def report_form(data: ReportRequest) -> ReportResponse:
    try:
        glm.invoke_report(data.content)
    except:
        raise HTTPException(status_code=500, detail="GLM-4 call failed")
    # 将生成的图片转成url
    try:
        image_to_url.upload_file(image_path="app/common/character_form.png")
        url = image_to_url.get_url()
    except:
        raise HTTPException(status_code=500, detail="File not found or bucket error")

    if not os.path.exists("app/common/character_form.png"):
        err = error.not_ideal_results()
        return ReportResponse(code=err.code, message=err.message)
    err = error.ok()
    return ReportResponse(code=err.code, message=err.message, data= {"report_url": url})
