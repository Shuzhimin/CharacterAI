from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import uvicorn
import os
import torch
from transformers import AutoConfig, AutoModel, AutoTokenizer
import json


app = FastAPI()

# 载入Tokenizer
tokenizer = AutoTokenizer.from_pretrained("/data/zhimin/ChatGLM2-6B/model/chatglm2-6b/", trust_remote_code=True)
config = AutoConfig.from_pretrained("/data/zhimin/ChatGLM2-6B/model/chatglm2-6b/", trust_remote_code=True, pre_seq_len=128)
model = AutoModel.from_pretrained("/data/zhimin/ChatGLM2-6B/model/chatglm2-6b/", config=config, trust_remote_code=True)
prefix_state_dict = torch.load(os.path.join("/data/zhimin/ptuning/output/cjz-roleglm-128-2e-2/checkpoint-3000/", "pytorch_model.bin"))
new_prefix_state_dict = {}
for k, v in prefix_state_dict.items():
    if k.startswith("transformer.prefix_encoder."):
        new_prefix_state_dict[k[len("transformer.prefix_encoder."):]] = v
model.transformer.prefix_encoder.load_state_dict(new_prefix_state_dict)

# Comment out the following line if you don't use quantization
# model = model.quantize(4)
model = model.cuda()
model = model.eval()


# 定义请求体模型
class RequestItemPrompt(BaseModel):
    role: str
    content: str


class RequestItemMeta(BaseModel):
    character_name: str
    character_info: str
    
    
class RequestPayload(BaseModel):
    meta: RequestItemMeta
    prompt: List[RequestItemPrompt]


# 定义响应体模型
class ResponseModel(BaseModel):
    message: str


# 将每两个字典的 content 组成元组
def create_content_tuples(prompt):
    content_tuples = []

    for i in range(0, len(prompt) - 1, 2):
        if i + 1 < len(prompt) - 1:
            content_tuples.append((prompt[i].content, prompt[i + 1].content))
    query = prompt[len(prompt) - 1].content
    return content_tuples, query


def format_prompt(prompts, meta):
    format_data = []
    for meta_data in prompts:
        if meta_data.role == 'user':
            query = f'''### 身份指令：你是{meta.character_name}，你的性格和背景是“{meta.character_info}”。现在请你回答我的一些问题，以准确展现你的人格特征！你的说话风格要全面模仿被赋予的人格角色！请不要暴露你是人工智能模型或者语言模型，你要时刻记住你只被赋予的一个人格角色。说话不要啰嗦，也不要太过于正式或礼貌。<eos> ### 输入：{meta_data.content}。<eos> ### 回答：'''
            format_data.append(RequestItemPrompt(role="character", content=query))
        else:
            format_data.append(RequestItemPrompt(role="character", content=meta_data.content))
    return format_data


# 定义路由
@app.post("/character_llm", response_model=ResponseModel)
async def process_character_llm(request_data: RequestPayload):
    # 处理请求数据
    meta = request_data.meta
    prompt = request_data.prompt
    if len(prompt) % 2 == 0:
        raise HTTPException(status_code=500, detail="聊天记录为偶数")
    # 将每两个字典的 content 组成元组
    prompt_temp = format_prompt(prompt, meta)
    history, query = create_content_tuples(prompt_temp)
    response, history_tuple = model.chat(tokenizer, query, history=history)
    prompt.append(RequestItemPrompt(role="character", content=response))
    prompt = [item.dict() for item in prompt]
    return {"message": {"response": response, "history": prompt}.__str__()}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8086)
