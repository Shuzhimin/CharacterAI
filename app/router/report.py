import os
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from matplotlib import pyplot as plt

from app.common import minio, model
from app.common.error import InternalException
from app.llm import glm
from app.llm.tool import Tool

report = APIRouter()

# implement tool in this file
# 支持中文
plt.rcParams["font.sans-serif"] = ["SimHei"]  # 用来正常显示中文标签
plt.rcParams["axes.unicode_minus"] = False  # 用来正常显示负号


# 在此处添加你想加入的工具
@Tool()
def get_data():
    """用于获取角色数据信息"""
    data = [
        {"cid": 1, "class": "科技", "create_time": 1, "attribute": "share"},
        {"cid": 2, "class": "科技", "create_time": 1, "attribute": "normal"},
        {"cid": 3, "class": "旅游", "create_time": 2, "attribute": "normal"},
        {"cid": 4, "class": "法律", "create_time": 3, "attribute": "share"},
        {"cid": 5, "class": "健康", "create_time": 4, "attribute": "normal"},
        {"cid": 6, "class": "美食", "create_time": 4, "attribute": "share"},
        {"cid": 7, "class": "美食", "create_time": 5, "attribute": "normal"},
        {"cid": 8, "class": "美食", "create_time": 6, "attribute": "normal"},
        {"cid": 9, "class": "健康", "create_time": 6, "attribute": "normal"},
        {"cid": 10, "class": "美食", "create_time": 6, "attribute": "normal"},
    ]
    return data


@Tool()
def class_num_pie(
    data: Annotated[
        dict, '角色数据信息，输入参数的结构为：{"类别1"：数量1, "类别12"：数量2,...}'
    ],
):
    """角用于绘制角色类别饼状图"""
    # 不同角色类别和对应的数量
    categories = [key for key in data.keys()]
    sizes = [value for value in data.values()]
    print(categories)
    # 创建饼状图
    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=categories, autopct="%1.1f%%", startangle=140)
    plt.title("角色各类别的占比")
    plt.savefig("app/assets/character_form.png")


@Tool()
def class_num_bar(
    data: Annotated[
        dict, '角色数据信息，输入参数的结构为：{"类别1"：数量1, "类别12"：数量2,...}'
    ],
):
    """用于绘制不同角色类别数量的柱状图"""
    categories = [key for key in data.keys()]
    sizes = [value for value in data.values()]

    # Creating the bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(categories, sizes)
    plt.title("不同角色类别的数量")
    plt.xlabel("角色类别")
    plt.ylabel("数量")
    plt.xticks(rotation=45)
    plt.grid(axis="y")
    # Save the plot to a file
    plt.savefig("app/assets/character_form.png")


@Tool()
def character_num_line(
    data: Annotated[
        dict, '角色数据信息，输入参数的结构为：{"类别1"：数量1, "类别12"：数量2,...}'
    ],
):
    """用于绘制每天创建角色数量折线图"""
    # 每天创建的角色数量
    days = [key for key in data.keys()]
    characters_created = [value for value in data.values()]
    # 绘制折线图
    plt.figure(figsize=(10, 6))
    plt.plot(days, characters_created, marker="o")
    plt.title("每天创建的角色数量")
    plt.xlabel("日期")
    plt.ylabel("角色数量")
    plt.grid(True)
    plt.savefig("app/assets/character_form.png")


@Tool()
def share_pie(
    data: Annotated[
        dict, '角色数据信息，输入参数的结构为：{"类别1"：数量1, "类别12"：数量2,...}'
    ],
):
    """用于绘制共享角色与正常角色数量的饼状图"""
    shared_characters = data["share"]
    normal_characters = data["normal"]
    # 绘制饼状图
    plt.figure(figsize=(8, 8))
    plt.pie(
        [shared_characters, normal_characters],
        labels=["共享角色", "正常角色"],
        autopct="%1.1f%%",
        startangle=140,
        colors=["#ff9999", "#66b3ff"],
    )
    plt.title("共享角色与正常角色数量的比例")
    plt.savefig("app/assets/character_form.png")


@report.post("/api/report/character")
async def report_form(request: model.ReportRequest) -> model.ReportResponseV2:
    try:
        # url 应该由函数返回
        # 或者说函数返回的仅仅是一张图片的路径
        # 然后我们需要在下面将图片上传到minio
        # 完成之后再删除图片 然后返回url
        function_result, model_response = glm.invoke_report(request.content)
    except:
        raise InternalException(code=1, message="报表生成失败")
    # 将生成的图片转成url
    minio.upload_file(image_path="app/assets/character_form.png")
    url = minio.get_url()
    if url == "":
        raise InternalException(code=1, message="报表生成失败")

    # if not os.path.exists("app/assets/character_form.png"):
    #     raise InternalException(code=1, message="报表生成失败")
    #
    return model.ReportResponseV2(content=model_response, url=url)
    # return model.ReportResponse(code=0, message="ok", data=[{"report_url": url}])
