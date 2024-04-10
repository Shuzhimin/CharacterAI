import os
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException

from app.common import minio, model
from app.common.error import InternalException
from app.llm import glm

report = APIRouter()


@report.post("/api/report/character")
async def report_form(data: model.ReportRequest) -> model.ReportResponse:
    try:
        glm.invoke_report(data.content)
    except:
        raise InternalException(code=1, message="报表生成失败")
    # 将生成的图片转成url
    minio.upload_file(image_path="app/assets/character_form.png")
    url = minio.get_url()
    if url == "":
        raise InternalException(code=1, message="报表生成失败")

    if not os.path.exists("app/assets/character_form.png"):
        raise InternalException(code=1, message="报表生成失败")

    return model.ReportResponse(code=0, message="ok", data=[{"report_url": url}])
