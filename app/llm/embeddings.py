# 2024/5/9
# zhangzhong

# https://github.com/langchain-ai/langchain/blob/master/libs/core/langchain_core/embeddings/embeddings.py
# https://stackoverflow.com/questions/77217193/langchain-how-to-use-a-custom-embedding-model-locally

from typing import List

from langchain_core.embeddings import Embeddings  # embeddings interface
from zhipuai import ZhipuAI


class ZhipuAIEmbeddings(Embeddings):
    def __init__(self, api_key: str, model: str = "embedding-2"):
        self.api_key = api_key
        self.model = model
        self.client = ZhipuAI(api_key=self.api_key)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        embeddings: list[list[float]] = []
        # 看起来模型是可以直接输出好几个文本的呀
        for text in texts:
            response = self.client.embeddings.create(
                model=self.model,
                input=text,
            )
            embeddings.append(response.data[0].embedding)
        return embeddings
        # 应该是不行的，不然在教程里面就直接batch了
        # response = self.client.embeddings.create(input=texts, model=self.model)
        # return [embedding.embedding for embedding in response.data]

    def embed_query(self, text: str) -> List[float]:
        return self.embed_documents([text])[0]
