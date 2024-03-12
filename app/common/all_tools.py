from .create_tools import Tool
import matplotlib.pyplot as plt

# 支持中文
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


class BaseTool:
    @staticmethod
    @Tool(name='load_tool', description='加载工具', params={'tool_name': {'type': 'string', 'description': '工具名称'}},
          required_params=['tool_name'])
    def load_tool(tool_name: str):
        Tool.load_tool(tool_name)
        return f"Tool '{tool_name}' loaded successfully."

    @staticmethod
    @Tool(name='unload_tool', description='卸载工具',
          params={'tool_name': {'type': 'string', 'description': '工具名称'}}, required_params=['tool_name'])
    def unload_tool(tool_name: str):
        Tool.unload_tool(tool_name)
        return f"Tool '{tool_name}' unloaded successfully."

    @staticmethod
    @Tool(name='list_tools', description='列出所有可用工具', params={}, required_params=[])
    def list_tools():
        return Tool.list_available_tools()


Tool.load_tool('list_tools')
Tool.load_tool('load_tool')
Tool.load_tool('unload_tool')


# 在此处添加你想加入的工具
@Tool(
    name='get_data',
    description='用于获取角色数据信息',
    params={},
    required_params=[]
)
def get_data():
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


@Tool(
    name='class_num_pie',
    description='用于绘制角色类别饼状图',
    params={
        'data': {'type': 'Dict', 'description': '角色数据信息，输入参数的结构为：{"类别1"：数量1, "类别12"：数量2,...}'}},
    required_params=['data']
)
def class_num_pie(data):
    # 不同角色类别和对应的数量
    categories = [key for key in data.keys()]
    sizes = [value for value in data.values()]
    print(categories)
    # 创建饼状图
    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=categories, autopct='%1.1f%%', startangle=140)
    plt.title('角色各类别的占比')
    plt.savefig('common/character_form.png')


@Tool(
    name='class_num_bar',
    description='用于绘制不同角色类别数量的柱状图',
    params={
        'data': {'type': 'Dict', 'description': '角色数据信息，输入参数的结构为：{"类别1"：数量1, "类别12"：数量2,...}'}},
    required_params=['data']
)
def class_num_bar(data):
    categories = [key for key in data.keys()]
    sizes = [value for value in data.values()]

    # Creating the bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(categories, sizes)
    plt.title('不同角色类别的数量')
    plt.xlabel('角色类别')
    plt.ylabel('数量')
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    # Save the plot to a file
    plt.savefig('common/character_form.png')


@Tool(
    name='character_num_line',
    description='用于绘制每天创建角色数量折线图',
    params={'data': {'type': 'Dict',
                     'description': '每天创建的角色数量，输入参数的结构为：{"时间1"：数量1, "时间2"：数量2,...}'}},
    required_params=['data']
)
def character_num_line(data):
    # 每天创建的角色数量
    days = [key for key in data.keys()]
    characters_created = [value for value in data.values()]
    # 绘制折线图
    plt.figure(figsize=(10, 6))
    plt.plot(days, characters_created, marker='o')
    plt.title("每天创建的角色数量")
    plt.xlabel("日期")
    plt.ylabel("角色数量")
    plt.grid(True)
    plt.savefig('common/character_form.png')


@Tool(
    name='share_pie',
    description='用于绘制共享角色与正常角色数量的饼状图',
    params={'data': {'type': 'Dict',
                     'description': '共享角色和正常角色的数量，输入参数的结构为：{"share"：数量1, "normal"：数量2,...}'}},
    required_params=['data']
)
def share_pie(data):
    shared_characters = data["share"]
    normal_characters = data["normal"]
    # 绘制饼状图
    plt.figure(figsize=(8, 8))
    plt.pie([shared_characters, normal_characters], labels=["共享角色", "正常角色"], autopct='%1.1f%%', startangle=140,
            colors=['#ff9999', '#66b3ff'])
    plt.title("共享角色与正常角色数量的比例")
    plt.savefig('common/character_form.png')
