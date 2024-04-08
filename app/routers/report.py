from fastapi import Depends, HTTPException, APIRouter
from app.model_deprecated.report import ReportRequest, ReportResponse
from typing import Annotated
from app.dependency import database_proxy
from typing import List
from app.common import image_to_url
import app.common.glm as glm
from app import error
import os


router = APIRouter()


@router.post("/character/report")
async def report_form(data: ReportRequest) -> ReportResponse:
    try:
        glm.invoke_report(data.content)
    except:
        err = error.gLM4_call_fail()
        return ReportResponse(code=err.code, message=err.message)
    # 将生成的图片转成url
    image_to_url.upload_file(image_path="app/assets/character_form.png")
    url = image_to_url.get_url()
    if url == '':
        err = error.image_to_url_fail()
        return ReportResponse(code=err.code, message=err.message)
    
    if not os.path.exists("app/assets/character_form.png"):
        err = error.not_ideal_results()
        return ReportResponse(code=err.code, message=err.message)
    
    err = error.ok()
    return ReportResponse(code=err.code, message=err.message, data= [{"report_url": url}])
