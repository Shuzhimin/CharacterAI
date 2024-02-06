# 2024/2/6
# zhangzhong

from app.common.conf import conf
import zhipuai
from app.models import Character
import json


def invoke_character_glm_api(character: Character) -> dict:
    zhipuai.api_key = conf.get_zhipuai_key()
    prompt_list = [
        eval(json.dumps(record.model_dump(), ensure_ascii=False))
        for record in character.chat_history[-2:]
    ]
    response = zhipuai.model_api.invoke(
        model="characterglm",
        meta={
            "user_info": character.user_info,
            "user_name": character.user_name,
            "bot_info": character.bot_info,
            "bot_name": character.bot_name,
        },
        prompt=prompt_list,
    )
    return response


def get_content_from_response(response: dict) -> str:
    ass_content = response["data"]["choices"][0]["content"]
    ass_content = eval(ass_content).replace("\n", "")
    response["data"]["choices"][0]["content"] = ass_content
    return response["data"]["choices"][0]["content"]
