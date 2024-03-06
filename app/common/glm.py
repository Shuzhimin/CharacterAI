# 2024/2/6
# zhangzhong

from app.common.conf import conf
from app.models import Character
import json
import requests


def invoke_model_api(character_name: str,character_info:str, content:str)->tuple[str, list[dict]]:
    prompts = []
    while True:
        if content == 'quit':
            break

        prompts.append({
            "role": "user",
            "content": content
        })

        response, history = character_llm(
            meta={
                "character_name": character_name,
                "character_info": character_info
            },
            prompt=prompts
        )
        prompts = history
        return response,history

def character_llm(meta, prompt)->tuple[str, list[dict]]:
    # 将两个字典作为参数发送到 FastAPI 接口
    response = requests.post("http://211.81.248.213:8086/character_llm", json={"meta": meta, "prompt": prompt})

    # 打印响应结果
    message_str = response.json()['message']
    # # 将字符串解析为字典
    message_dict = eval(message_str)

    # 提取 response 和 history
    response = message_dict['response']
    # 这里的history没有create_time
    history = message_dict['history']
    return response, history

