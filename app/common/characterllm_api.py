import json
import requests


def character_llm(meta, prompt):
    # 将两个字典作为参数发送到 FastAPI 接口
    response = requests.post("http://211.81.248.213:8086/character_llm", json={"meta": meta, "prompt": prompt})

    # 打印响应结果
    message_str = response.json()['message']
    # # 将字符串解析为字典
    message_dict = eval(message_str)

    # 提取 response 和 history
    response = message_dict['response']
    history = message_dict['history']
    return response, history
