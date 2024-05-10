import os
import uuid
from operator import itemgetter
from typing import AsyncGenerator

import requests
from langchain.chains import create_sql_query_chain
from langchain_community.llms.chatglm3 import ChatGLM3
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_community.utilities import SQLDatabase
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (ChatPromptTemplate, MessagesPlaceholder,
                                    PromptTemplate)
from langchain_core.runnables import RunnablePassthrough
from langchain_experimental.utilities import PythonREPL

from app.common import conf
from app.common.minio import minio_service
from app.common.model import ChatMessage, ReportResponseV2

from .interface import AIBot


class Reporter(AIBot):
    def __init__(self):
        self.llm = ChatGLM3(
            temperature=0, endpoint_url="http://211.81.248.218:8000/v1/chat/completions"
        )
        self.db_url = conf.get_postgres_sqlalchemy_database_url()

    def check_question(self, question: str) -> str:
        """第一部分 检验输入是否符合功能设定"""
        check_template = """
            你只能回复“yes”和“no”。
            判断用户的输入是否与“生成代码绘制图表”有关。
            如果有关，你只需回答“yes”。
            如果无关，你只需回答“no”。
        """
        check_prompt = ChatPromptTemplate.from_messages(
            [("system", check_template), ("human", "{input}")]
        )
        chain = check_prompt | self.llm
        check_result = chain.invoke({"input": question})
        return check_result

    def get_data(self, question: str, uid: int) -> str:
        """第二部分 获取相应的数据"""
        db = SQLDatabase.from_uri(self.db_url)
        get_data_prompt = PromptTemplate.from_template(
            """给定以下用户问题、相应的SQL查询和SQL结果，回答用户问题。
                Question: {question}
                SQL Query: {query}
                SQL Result: {result}
                Answer: """
        )
        execute_query = QuerySQLDataBaseTool(db=db)
        write_query = create_sql_query_chain(self.llm, db)
        answer = get_data_prompt | self.llm | StrOutputParser()
        chain = (
            RunnablePassthrough.assign(query=write_query).assign(
                result=itemgetter("query") | execute_query
            )
            | answer
        )
        data_content = chain.invoke(
            {
                "question": f"""请判断characters表中是否有uid={uid}。
                                如果没有，你只需要回复“no”。
                                如果有，你只需要回复“yes”。
                                请不要回复其它无关内容。"""
            }
        )
        data_question = f"分析“{question}”应该需要用到哪些数据来绘图，并从characters表且uid={uid}中获取这些数据。你只需要用dict类型返回获取到的数据，不要输出其它无关信息。"
        if data_content == "yes":
            data_content = chain.invoke({"question": data_question})
        return data_question, data_content

    def get_data_description(self, data_question: str, data_content: str) -> str:
        """第三部分 获取数据的文本描述"""
        # 参考资料：https://python.langchain.com/v0.1/docs/use_cases/chatbots/memory_management/
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful assistant. Answer all questions to the best of your ability.",
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )
        chain = prompt | self.llm
        data_discription = chain.invoke(
            {
                "messages": [
                    HumanMessage(content=data_question),
                    AIMessage(content=data_content),
                    HumanMessage(content="用一句话提取和总结获取到的数据"),
                ],
            }
        )
        return data_discription

    def _sanitize_output(self, text: str):
        # 从大模型的输出中提取出代码
        _, after = text.split("```python")
        return after.split("```")[0]

    def code_plot(self, data_content: str, question: str, save_path: str) -> str:
        """第四部分 根据获取到的数据编写绘图代码并执行"""
        draw_template = f"""Write some Python code to help users draw graph. 

        The graph drawn in Python must specify a save path.

        The path to save the graph is "{save_path}".

        Return only python code in Markdown format, e.g.:

        ```python
        ....
        ```"""
        prompt = ChatPromptTemplate.from_messages(
            [("system", draw_template), ("human", "{input}")]
        )
        chain = prompt | self.llm | StrOutputParser()
        output = chain.invoke(
            {
                "input": f"数据为{data_content}，请将数据改为字典类型，在根据数据编写代码完成“{question}”任务。一定要根据指定路径保存图片"
            }
        )
        code_text = self._sanitize_output(output)
        PythonREPL().run(code_text)
        return code_text

    def _generate_image_path(self) -> str:
        path_prefix = conf.get_save_image_path()
        os.makedirs(path_prefix, exist_ok=True)
        return os.path.join(path_prefix, f"{uuid.uuid4()}.png")

    def reporter_llm(self, question: str, uid: int) -> ReportResponseV2:
        # 根据用户的content问题和uid，生成对应报表
        flag = self.check_question(question)
        # 初始化url和content
        content = "非常抱歉，我只能回答编写代码绘制图表的相关问题"
        url = ""
        if flag == "yes":
            data_question, data_content = self.get_data(question, uid)
            # 初始化当数据没有获取到时content的值
            content = "很抱歉，没有查询到该用户有创建角色"
            # 判断用户是否有创建角色
            if data_content != "no":
                data_discription = self.get_data_description(
                    data_question, data_content
                )
                save_path = self._generate_image_path()
                code_text = self.code_plot(data_content, question, save_path=save_path)
                content = data_discription + "\n" + code_text
                if os.path.exists(save_path):
                    url = minio_service.upload_file_from_file(filename=save_path)
        return ReportResponseV2(content=content, url=url)

    async def ainvoke(
        self, input: ChatMessage, uid: int
    ) -> AsyncGenerator[ChatMessage, None]:
        response_content = self.reporter_llm(question=input.content, uid=uid)
        yield ChatMessage(
            # chat_id=input.chat_id,
            sender=input.receiver,
            receiver=input.sender,
            is_end_of_stream=False,
            content=response_content.content,
            images=[response_content.url],
        )
