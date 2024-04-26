# 2024/2/6
# zhangzhong
import json
from typing import Any

import requests
from zhipuai import ZhipuAI
from zhipuai.types.chat.chat_completion import Completion

from app.common import conf
# from app.llm.all_tools import Tool
from app.llm.tool import Tool

client = ZhipuAI(api_key=conf.get_zhipuai_key())


def invoke_model_api(character_name: str, character_info: str, content: str) -> str:
    prompts = []
    while True:
        if content == "quit":
            break

        prompts.append({"role": "user", "content": content})

        response, history = character_llm(
            meta={"character_name": character_name, "character_info": character_info},
            prompt=prompts,
        )
        prompts = history
        return response


def character_llm(meta: dict, prompt: str) -> tuple[str, list[dict]]:
    # 将两个字典作为参数发送到 FastAPI 接口
    response = requests.post(
        "http://211.81.248.213:8086/character_llm",
        json={"meta": meta, "prompt": prompt},
    )

    # 打印响应结果
    message_str = response.json()["message"]
    # # 将字符串解析为字典
    message_dict = eval(message_str)

    # 提取 response 和 history
    response = message_dict["response"]
    # 这里的history没有create_time
    history = message_dict["history"]
    return response, history


# 为了防止写错，这个函数还是直接重写吧
def invoke_report(content: str) -> tuple[Any, str | None]:
    # print("报表生成成功: character_form.png")
    messages = [
        # {
        #     "role": "system",
        #     "content": """你是一个能够调用工具的AI助手，系统将提供三个基础函数: list_tools, load_tool, unload_tool，list_tools是用来查看所有可以使用的工具；load_tool是用来加载需要使用的工具；unload_tool是用来释放使用完的工具。你回答问题时必须遵循这个顺序：首先使用list_tools查看所有可用的工具，如果存在合适的工具，你将使用load_tool加载该工具，然后调用该工具，使用完毕后调用unload_tool释放工具。""",
        # },
        {"role": "user", "content": content},
    ]
    response = client.chat.completions.create(
        model="glm-4",
        messages=messages,
        tools=Tool.tools,
    )

    function_result = None
    # 就只做一轮吧，这些函数设计出来也是这样的
    if response.choices[0].message.tool_calls:
        messages.append(response.choices[0].message.model_dump())
        tool_call = response.choices[0].message.tool_calls[0]
        args = tool_call.function.arguments

        function_result = Tool.dispatch(
            name=tool_call.function.name, **json.loads(args)
        )
        messages.append(
            {
                "role": "tool",
                "content": f"{json.dumps(function_result)}",
                "tool_call_id": tool_call.id,
            }
        )
    else:
        messages.append(
            {
                "role": "user",
                "content": "目前尚未实现该功能，请根据历史聊天生成一条合适的道歉信息。",
            }
        )

    # 这里的调用应该不需要再传递tools了吧，我们只是想要获取一个结果
    response = client.chat.completions.create(
        model="glm-4",  # 填写需要调用的模型名称
        messages=messages,
    )
    assert isinstance(response, Completion)
    # 1. 我们想要函数的返回值，
    # 2. 我们想要模型的返回值
    return function_result, response.choices[0].message.content
