# DEPRECATED
#
# import os
# import uuid
# from typing import Annotated, List
#
# import matplotlib.pyplot
# from fastapi import APIRouter, Depends, HTTPException, WebSocket
# from matplotlib import pyplot as plt
#
# from app.aibot.reporter import Reporter
# from app.common import conf, minio, model
# from app.common.error import InternalException
# from app.common.minio import minio_service
# from app.common.model import ChatMessage, FunctionToolResult
# from app.database import DatabaseService
# from app.dependency import get_db, get_token_data, get_user
# from app.llm import glm
# from app.llm.tool import Tool
#
# db = DatabaseService()
# report = APIRouter()
#
# # implement tool in this file
# # 支持中文
# plt.rcParams["font.sans-serif"] = ["SimHei"]  # 用来正常显示中文标签
# plt.rcParams["axes.unicode_minus"] = False  # 用来正常显示负号


# 在此处添加你想加入的工具
# @Tool()
# def get_data():
#     """用于获取角色数据信息"""
#     data = [
#         {"cid": 1, "class": "科技", "create_time": 1, "attribute": "share"},
#         {"cid": 2, "class": "科技", "create_time": 1, "attribute": "normal"},
#         {"cid": 3, "class": "旅游", "create_time": 2, "attribute": "normal"},
#         {"cid": 4, "class": "法律", "create_time": 3, "attribute": "share"},
#         {"cid": 5, "class": "健康", "create_time": 4, "attribute": "normal"},
#         {"cid": 6, "class": "美食", "create_time": 4, "attribute": "share"},
#         {"cid": 7, "class": "美食", "create_time": 5, "attribute": "normal"},
#         {"cid": 8, "class": "美食", "create_time": 6, "attribute": "normal"},
#         {"cid": 9, "class": "健康", "create_time": 6, "attribute": "normal"},
#         {"cid": 10, "class": "美食", "create_time": 6, "attribute": "normal"},
#     ]
#     return data
#

# 接下来要做的就是实现下面这四个函数，但是我们先不修改他们的功能
# 时刻注意重构的两顶帽子 现在是重构的阶段 不是添加功能的阶段
# 等重构完成之后 单元测试通过了 我们再尝试添加功能


# def _generate_image_path() -> str:
#     return os.path.join(conf.get_save_image_path(), f"{uuid.uuid4()}.png")


# @Tool()
# def class_num_pie() -> FunctionToolResult:
#     """用于绘制角色类别饼状图"""

#     # 我有什么方法可以拿到callid吗 我们可以使用那个callid作为文件名字
#     # 很显然，我们是可以传入这个参数的，而且在分析的时候，我们也可以去掉这个参数
#     # 因为这个装饰器是我们自己控制的呀
#     # 不同角色类别和对应的数量
#     # 1. 获取所有的角色
#     characters = db.get_characters(where=model.CharacterWhere())
#     # 统计characters中各个category的数
#     data: dict[str, int] = {}
#     for character in characters:
#         data[character.category] = data.get(character.category, 0) + 1
#     categories = [key for key in data.keys()]
#     sizes = [value for value in data.values()]
#     print(categories)
#     # 创建饼状图
#     # https://stackoverflow.com/questions/63412583/nswindow-drag-regions-should-only-be-invalidated-on-the-main-thread-this-will-t
#     matplotlib.pyplot.switch_backend("Agg")
#     plt.figure(figsize=(8, 8))
#     plt.pie(sizes, labels=categories, autopct="%1.1f%%", startangle=140)
#     plt.title("角色各类别的占比")
#     # 图片保存再一个单独的地方 名字使用uuid即可 之后删除即可
#     # 我们需要返回一个dict 让大模型生成对应的文本
#     path = _generate_image_path()
#     plt.savefig(path)
#     # 我就知道 返回path会让大模型在输出中加入path
#     # 如何才能做到只返回data呢
#     return FunctionToolResult(data=data, path=path)
#     # 不同的工具函数返回的图片是不一样的 所以很难写成一个通用的函数
#     # 所以画图需要在每个tool内部实现
#     # 同时我们并不希望将url作为函数的返回值进行返回
#     # 但是data是需要返回的
#     # 问题是我们返回图片URL呢?
#     # plt.savefig("app/assets/character_form.png")


# # 把绘图函数拆开 我们在拿到数据之后，在router的实现里面再调用绘图函数 这样不好的一点是
# # 代码的可读性差


# @Tool()
# def class_num_bar() -> FunctionToolResult:
#     """用于绘制不同角色类别数量的柱状图"""
#     characters = db.get_characters(where=model.CharacterWhere())
#     # 统计characters中各个category的数
#     data: dict[str, int] = {}
#     for character in characters:
#         data[character.category] = data.get(character.category, 0) + 1

#     categories = [key for key in data.keys()]
#     sizes = [value for value in data.values()]

#     # Creating the bar chart
#     plt.figure(figsize=(10, 6))
#     plt.bar(categories, sizes)
#     plt.title("不同角色类别的数量")
#     plt.xlabel("角色类别")
#     plt.ylabel("数量")
#     plt.xticks(rotation=45)
#     plt.grid(axis="y")
#     # Save the plot to a file
#     path = _generate_image_path()
#     plt.savefig(path)
#     return FunctionToolResult(data=data, path=path)


# @Tool()
# def character_num_line() -> FunctionToolResult:
#     """用于绘制每天创建角色数量折线图"""

#     # 没有指定日期啊
#     # 1. 首先获取所有角色
#     characters = db.get_characters(where=model.CharacterWhere())
#     # 然后把所有角色根据日期进行分类并排序
#     data: dict[str, int] = {}
#     # 实际上我们的角色是timestamp 我们需要将zhihuai的timestamp转换成日期
#     for character in characters:
#         date = character.created_at.strftime("%Y-%m-%d")
#         data[date] = data.get(date, 0) + 1

#     # sort by date
#     data = dict(sorted(data.items(), key=lambda item: item[0]))

#     # 每天创建的角色数量
#     days = [key for key in data.keys()]
#     characters_created = [value for value in data.values()]
#     # 绘制折线图
#     plt.figure(figsize=(10, 6))
#     plt.plot(days, characters_created, marker="o")
#     plt.title("每天创建的角色数量")
#     plt.xlabel("日期")
#     plt.ylabel("角色数量")
#     plt.grid(True)

#     path = _generate_image_path()
#     plt.savefig(path)
#     return FunctionToolResult(data=data, path=path)


# @Tool()
# def share_pie() -> FunctionToolResult:
#     """用于绘制共享角色与正常角色数量的饼状图"""

#     characters = db.get_characters(where=model.CharacterWhere())
#     data = {"share": 0, "normal": 0}
#     for character in characters:
#         if character.is_shared:
#             data["share"] += 1
#         else:
#             data["normal"] += 1
#     shared_characters = data["share"]
#     normal_characters = data["normal"]
#     # 绘制饼状图
#     plt.figure(figsize=(8, 8))
#     plt.pie(
#         [shared_characters, normal_characters],
#         labels=["共享角色", "正常角色"],
#         autopct="%1.1f%%",
#         startangle=140,
#         colors=["#ff9999", "#66b3ff"],
#     )
#     plt.title("共享角色与正常角色数量的比例")
#     path = _generate_image_path()
#     plt.savefig(path)
#     return FunctionToolResult(data=data, path=path)


# report V1
# @report.post("/api/report/character")
# async def report_form(request: model.ReportRequest) -> model.ReportResponseV2:
#     try:
#         # url 应该由函数返回
#         # 或者说函数返回的仅仅是一张图片的路径
#         # 然后我们需要在下面将图片上传到minio
#         # 完成之后再删除图片 然后返回url
#         function_result, model_response = glm.invoke_report(request.content)
#     except:
#         raise InternalException(code=1, message="报表生成失败")
#     # 将生成的图片转成url
#     url = None
#     if function_result is not None:
#         path: str = function_result.path
#         # minio.upload_file(image_path=path)
#         # url = minio.get_url()
#         url = minio_service.upload_file_from_file(filename=path)
#         if url == "":
#             raise InternalException(code=1, message="报表生成失败")

#     # if not os.path.exists("app/assets/character_form.png"):
#     #     raise InternalException(code=1, message="报表生成失败")
#     #
#     return model.ReportResponseV2(content=model_response, url=url)
#     # return model.ReportResponse(code=0, message="ok", data=[{"report_url": url}])


# report V2
# @report.websocket("/ws/report")
# async def websocket_endpoint(
#     websocket: WebSocket,
#     token: str,
#     db: Annotated[DatabaseService, Depends(get_db)],
# ):
#     # 验证token，获取用户
#     token_data = await get_token_data(token=token)
#     user = get_user(token_data=token_data, db=db)
#     # 创建一个报表智能体
#     reporter = Reporter()
#
#     await websocket.accept()
#
#     try:
#         while True:
#             # 从client接收一个ChatMessage类型的消息
#             user_content = await websocket.receive_json()
#             # 将消息传入报表智能体得到响应
#             # 得到的user_content是一个dict,用dict给ChatMessage赋值
#             user_content = ChatMessage.model_validate(user_content)
#             agent_content = reporter.ainvoke(input=user_content, uid=user.uid)
#             # 发送智能体的回复给client
#             # agent_content是一个ChatMessage类型的对象，将其转换为dict
#             await websocket.send_json(agent_content.model_dump())
#     except Exception as e:
#         print(e)
#         await websocket.close()
