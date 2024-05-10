# 2024/5/7
# zhangzhong
# retriever
# https://python.langchain.com/docs/use_cases/question_answering/
# question-answering (Q&A) chatbots.
# These applications use a technique known as Retrieval Augmented Generation, or RAG.
# RAG is a technique for augmenting LLM knowledge with additional data.
#

# RAG Architecture
# https://python.langchain.com/docs/use_cases/question_answering/#rag-architecture
import bs4
from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.history_aware_retriever import \
    create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.chat_message_histories import ChatMessageHistory
# 所以embedding并没有添加到langchain里面
from langchain_community.chat_models.zhipuai import ChatZhipuAI
# langchain_community.embeddings 里面确实没有ZhipuAI的embedding
from langchain_community.document_loaders import WebBaseLoader
# https://python.langchain.com/docs/integrations/vectorstores/qdrant/
from langchain_community.vectorstores import Qdrant
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import (AIMessage, BaseMessage, HumanMessage,
                                     SystemMessage)
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.common import conf, model
from app.common.model import ChatMessage
from app.database import schema
from app.llm import ZhipuAIEmbeddings

from .interface import AIBot


def from_schema_message_to_langchain_message(message: schema.Message) -> BaseMessage:
    # TODO: 这个Message消息格式绝对设计的不对
    # 我竟然不知道这个消息到底是谁发给谁的
    # 我还需要额外的代码上下文才能知道到底发生了什么
    # 仅仅依靠数据库中的数据却不能复现 这肯定是完全不合理的
    # sender 应该改成role 也就是一个字符串
    # human ai system tool 这种的，我可以知道这条消息是谁发的
    match message.sender:
        case "human":
            return HumanMessage(content=message.content)
        case "ai":
            return AIMessage(content=message.content)
        case "system":
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

        # 在这里创建我们的模型和embedding
        #
        self.session_id = str(chat_id)
        self.model = ChatZhipuAI(
            temperature=0.95,
            model="glm-4",
            api_key=conf.get_zhipuai_key(),
        )
        self.embeddings = ZhipuAIEmbeddings(api_key=conf.get_zhipuai_key())
        # 这里我们需要根据knowledge来获取retriver

        # add chat history
        # https://python.langchain.com/docs/integrations/memory/sql_chat_message_history/
        # 虽然有直接提供工具，但是数据库表我们不能自己控制，非常不灵活
        # 还是使用内存的方式进行存储吧，然后把消息自己保存在数据库中即可
        # 这样我们也可以根据自己设计的表自己提取历史记录来填充这个store内存结构
        # TODO: 不对啊，这里的store又不共享，所以没必要是一个dict呀
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
            # session id 应该是chatid吧
            # 这是异步的但是不是多线程的 所以不用加锁
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
