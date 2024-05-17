# 2024/5/7
# zhangzhong
# retriever
# https://python.langchain.com/docs/use_cases/question_answering/
# https://python.langchain.com/docs/integrations/vectorstores/qdrant/
# question-answering (Q&A) chatbots.
# These applications use a technique known as Retrieval Augmented Generation, or RAG.
# RAG is a technique for augmenting LLM knowledge with additional data.
# RAG Architecture
# https://python.langchain.com/docs/use_cases/question_answering/#rag-architecture

from typing import AsyncGenerator
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.chat_models.zhipuai import ChatZhipuAI
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from app.common.vector_store import KnowledgeBase
from app.common import conf, model
from app.common.model import ChatMessage
from app.database import schema
from app.llm import ZhipuAIEmbeddings

from .interface import AIBot


def from_schema_message_to_langchain_message(message: schema.Message) -> BaseMessage:
    match model.MessageSender(message.sender):
        case model.MessageSender.HUMAN:
            return HumanMessage(content=message.content)
        case model.MessageSender.AI:
            return AIMessage(content=message.content)
        case model.MessageSender.SYSTEM:
            return SystemMessage(content=message.content)
        case _:
            raise ValueError(f"unsupported message type: {message}")


class RAG(AIBot):
    def __init__(
        self,
        cid: int,
        uid: int,
        chat_id: int,
        knowledge_id: str,
        chat_history: list[schema.Message] = [],
    ) -> None:
        assert knowledge_id, "empty knowledge id"
        self.cid = cid
        self.uid = uid
        self.knowledge_id = knowledge_id

        self.session_id = str(chat_id)
        self.model = ChatZhipuAI(
            temperature=0.95,
            model="glm-4",
            api_key=conf.get_zhipuai_key(),
        )
        self.embeddings = ZhipuAIEmbeddings(api_key=conf.get_zhipuai_key())

        # add chat history
        # https://python.langchain.com/docs/integrations/memory/sql_chat_message_history/
        self.store: dict[str, BaseChatMessageHistory] = {}
        history = self._get_session_history(session_id=self.session_id)
        for message in chat_history:
            history.add_message(
                message=from_schema_message_to_langchain_message(message=message)
            )

        self.rag = self.create_rag()

    def _get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        if session_id not in self.store:
            self.store[session_id] = ChatMessageHistory()
        return self.store[session_id]

    def create_retriever(self):
        history_aware_prompt = ChatPromptTemplate.from_messages(
            messages=[
                (
                    "system",
                    """Given a chat history and the latest user question \
        which might reference context in the chat history, formulate a standalone question \
        which can be understood without the chat history. Do NOT answer the question, \
        just reformulate it if needed and otherwise return it as is.""",
                ),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )
        return create_history_aware_retriever(
            prompt=history_aware_prompt,
            llm=self.model,
            retriever=KnowledgeBase.as_retriever(knowledge_id=self.knowledge_id),
        )

    def create_qabot(self):
        # 2. QA chain
        return create_stuff_documents_chain(
            prompt=ChatPromptTemplate.from_messages(
                messages=[
                    (
                        "system",
                        """You are an assistant for question-answering tasks. \
        Use the following pieces of retrieved context to answer the question. \
        If you don't know the answer, just say that you don't know. \
        Use three sentences maximum and keep the answer concise.\

        {context}""",
                    ),
                    MessagesPlaceholder("chat_history"),
                    ("human", "{input}"),
                ]
            ),
            llm=self.model,
        )

    def create_rag(self):
        def get_session_history(session_id: str) -> BaseChatMessageHistory:
            if session_id not in self.store:
                self.store[session_id] = ChatMessageHistory()
            return self.store[session_id]

        return RunnableWithMessageHistory(
            runnable=create_retrieval_chain(
                retriever=self.create_retriever(),
                combine_docs_chain=self.create_qabot(),
            ),
            get_session_history=get_session_history,
            input_messages_key="input",
            output_messages_key="answer",
            history_messages_key="chat_history",
        )

    async def ainvoke(self, input: ChatMessage) -> AsyncGenerator[ChatMessage, None]:
        async for output in self.rag.ainvoke(
            {"input": input.content},
            config={"configurable": {"session_id": self.session_id}},
        ):
            yield ChatMessage(
                sender=self.cid,
                receiver=self.uid,
                is_end_of_stream=False,
                content=output["answer"],
            )
        yield ChatMessage(
            sender=self.cid, receiver=self.uid, is_end_of_stream=True, content=""
        )
