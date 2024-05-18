# 2024/4/10
# zhangzhong

from fastapi import APIRouter

from app import llm
from app.common.model import GenerationRequestBody

generation = APIRouter(prefix="/api/generation")


@generation.post("/image")
def generate_image(generation: GenerationRequestBody) -> str:
    return llm.generate_image(generation.prompt)
