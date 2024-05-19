# 2024/2/6
# zhangzhong

import json

import requests
from zhipuai import ZhipuAI
from zhipuai.types.chat.chat_completion import Completion

from app.common import conf
from app.common.model import FunctionToolResult, RequestPayload, ResponseModel
from app.llm.tool import Tool

client = ZhipuAI(api_key=conf.get_zhipuai_key())


def character_llm(payload: RequestPayload) -> ResponseModel:
    response = requests.post(
        conf.get_glm2_url(),
        json=payload.model_dump(),
    )
    response_dict = eval(response.json()["message"])
    return ResponseModel(message=response_dict["response"])


def invoke_report(content: str) -> tuple[FunctionToolResult | None, str]:
    messages = [
        {"role": "user", "content": content},
    ]
    response = client.chat.completions.create(
        model="glm-4",
        messages=messages,
        tools=Tool.tools,
    )

    function_result = None
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
                "content": f"函数调用成功，请以文字的方式从返回值中提取并总结信息，不要生成创建图像的代码。返回值：{json.dumps(function_result.data)}",
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

    response = client.chat.completions.create(
        model="glm-4",
        messages=messages,
    )
    assert isinstance(response, Completion)
    message = response.choices[0].message
    assert message.content is not None, f"message content is None: {message}"
    return function_result, message.content
