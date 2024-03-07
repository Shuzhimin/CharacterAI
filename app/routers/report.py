from fastapi import Depends, HTTPException, APIRouter
from fastapi.responses import FileResponse
from app.models import Character, ChatRecord
from typing import Annotated
from app.dependencies import database_proxy
from typing import List, Union
import app.common.glm as glm
from app.common.error import ErrorV2, ErrorCode
import os


router = APIRouter()


@router.post("/character/report")
async def report_form(content: str) -> dict[str, Union[int, str, List[dict]]]:
    try:
        glm.invoke_report(content)
    except:
        raise HTTPException(status_code=500, detail="GLM-4 call failed")

    if os.path.exists("common/character_form.jpeg"):
        err = ErrorV2(ErrorCode.OK, message="Report generated successfully")
        return {
            "code": err.code,
            "message": err.message,
            "data": [
                {"report": FileResponse("common/character_form.jpeg", media_type="image/jpeg")}
            ]
        }
    err = ErrorV2(ErrorCode.NOT_IDEAL_RESULTS, message="GLM-4 did not provide ideal results")
    return {
        "code": err.code,
        "message": err.message,
        "data": []
    }
