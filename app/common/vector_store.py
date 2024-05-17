# 2024/5/9
# zhangzhong


import uuid

from langchain_community.document_loaders import (
    PDFMinerLoader,
    TextLoader,
    WebBaseLoader,
)
from langchain_community.document_loaders.base import BaseLoader
from langchain_community.vectorstores.qdrant import Qdrant
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.common import conf
from app.llm import ZhipuAIEmbeddings


class LoaderFactory:
    def __init__(self, file: str):
        self.file = file

    def new(self) -> BaseLoader:
        if self.file.endswith("txt"):
            return TextLoader(file_path=self.file)
        elif self.file.endswith("pdf"):
            return PDFMinerLoader(file_path=self.file)
        else:
            raise ValueError(f"Unsupported file type: {self.file}")


class KnowledgeBase:
    def __init__(self, urls: list[str] = [], files: list[str] = []):
        documents: list[Document] = []
        for url in urls:
            documents.extend(WebBaseLoader(web_path=url).load())
        for file in files:
            documents.extend(LoaderFactory(file=file).new().load())

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200, add_start_index=True
        )
        documents = splitter.split_documents(documents=documents)

        # add metadata for multi tenancy
        self.knowledge_id = str(uuid.uuid4())
        for doc in documents:
            doc.metadata["knowledge_id"] = self.knowledge_id

        self.collection_name = "my_documents"
        self.vector_store = Qdrant.from_documents(
            documents=documents,
            embedding=ZhipuAIEmbeddings(api_key=conf.get_zhipuai_key()),
            url=conf.get_qdrant_host(),
            prefer_grpc=conf.get_qdrant_prefer_grpc(),
            collection_name=conf.get_qdrant_collection_name(),
        )

    @staticmethod
    def as_retriever(knowledge_id: str):
        vector_store = Qdrant.from_documents(
            documents=[],
            embedding=ZhipuAIEmbeddings(api_key=conf.get_zhipuai_key()),
            url=conf.get_qdrant_host(),
            prefer_grpc=conf.get_qdrant_prefer_grpc(),
            collection_name=conf.get_qdrant_collection_name(),
        )
        return vector_store.as_retriever(
            search_kwargs={"filter": {"knowledge_id": knowledge_id}}
        )

    def get_knowledge_id(self) -> str:
        return self.knowledge_id
