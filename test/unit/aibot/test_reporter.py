from app.aibot.reporter import Reporter
from app.common.model import ChatMessage, ReportResponseV2


def test_reporter():
    uid = 21
    reporter = Reporter(uid=uid)
    # 测试是否能拒绝不符合规定的输入
    check_result = reporter.check_question(question="今天天气怎么样")
    print(check_result)

    # 测试能否获得数据
    question = "绘制角色类别的饼状图"
    check_result = reporter.check_question(question=question)
    print(check_result)
    data_question, data_content = reporter.get_data(question=question, uid=uid)
    print(data_question)
    print(data_content)

    # 测试能否正确用一句话描述数据
    description = reporter.get_data_description(
        data_question=data_question, data_content=data_content
    )
    print(description)

    # 测试能否生成代码并绘制图表
    path = reporter._generate_image_path()
    code_text = reporter.code_plot(
        data_content=data_content,
        question=question,
        save_path=path,
    )
    print(code_text)
    print(path)

    # 测试完整流程
    response = reporter.reporter_llm(question=question, uid=uid)
    print(response)

    # 测试唤醒智能体
    input = ChatMessage(
        # chat_id=1,
        sender=1,
        receiver=1,
        is_end_of_stream=False,
        content="根据各个角色类别的数量生成饼状图",
    )
    uid = 21
    response = reporter.ainvoke(input=input)
    print(response)
