# import json

# import httpx
# from fastapi.testclient import TestClient

# from app.common import model
# from app.common.model import ChatMessage, ReportResponseV2
# from app.main import app

# # from app.router.report import (
# #     character_num_line,
# #     class_num_bar,
# #     class_num_pie,
# #     share_pie,
# # )

# # TODO: 为了更方便的进行测试，我需要生成一些假的角色，这样生成的图表才会好看一些
# # 或者我在其他的测试中生成的角色就可以随机的引入一些category啊 对吧

# client = TestClient(app)


# # 所有的工具都应该可以被直接测试
# # def test_class_num_pie():
# #     data, path = class_num_pie()
# #     print(data, path)


# # def test_class_num_bar():
# #     data, path = class_num_bar()
# #     print(data, path)


# # def test_character_num_line():
# #     data, path = character_num_line()
# #     print(data, path)


# # def test_share_pie():
# #     data, path = share_pie()
# #     print(data, path)


# # def _test_report(content: str):
# #     response: httpx.Response = client.post(
# #         url="/api/report/character",
# #         json={"content": content},
# #     )
# #     print(response.json())
# #     assert response.status_code == 200
# #     report_response = ReportResponseV2(**response.json())
# #     assert report_response.url is not None


# # def test_report():
# #     contents = [
# #         "根据各个角色类型的数量生成饼状图",
# #         "根据各个角色类型的数量生成柱状图",
# #         "创建每日新增角色的折线图",
# #         "根据共享角色与正常角色数量生成饼状图",
# #     ]
# #     for content in contents:
# #         _test_report(content=content)


# # def test_report_unsupported_tool():
# #     response: httpx.Response = client.post(
# #         url="/api/report/character",
# #         json={"content": "今天天气不错"},
# #     )
# #     print(response.json())
# #     assert response.status_code == 200
# #     report_response = ReportResponseV2(**response.json())
# #     assert report_response.url is None
# def test_report(
#     token: model.Token,
# ):
#     with client.websocket_connect(
#         url=f"/ws/report?token={token.access_token}"
#     ) as websocket:
#         # 测试生成角色类别饼状图
#         user_message = ChatMessage(
#             # chat_id=1,
#             sender=1,
#             receiver=1,
#             is_end_of_stream=False,
#             content="根据各个角色类型的数量生成饼状图",
#         )
#         websocket.send_json(user_message.model_dump())
#         agent_message = websocket.receive_json()
#         print(agent_message)

#         # 测试生成角色饼状图
#         user_message = ChatMessage(
#             # chat_id=1,
#             sender=1,
#             receiver=1,
#             is_end_of_stream=False,
#             content="绘制共享角色与非共享角色数量的饼状图",
#         )
#         websocket.send_json(user_message.model_dump())
#         agent_message = websocket.receive_json()
#         print(agent_message)

#         # 测试绘制不同角色类别数量的柱状图
#         user_message = ChatMessage(
#             # chat_id=1,
#             sender=1,
#             receiver=1,
#             is_end_of_stream=False,
#             content="绘制不同角色类别数量的柱状图",
#         )
#         websocket.send_json(user_message.model_dump())
#         agent_message = websocket.receive_json()
#         print(agent_message)

#         # # 测试与报表功能不符的输入
#         user_message = ChatMessage(
#             # chat_id=1,
#             sender=1,
#             receiver=1,
#             is_end_of_stream=False,
#             content="你叫什么名字",
#         )
#         websocket.send_json(user_message.model_dump())
#         agent_message = websocket.receive_json()
#         print(agent_message)
