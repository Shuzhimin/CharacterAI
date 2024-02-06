# 2024/2/6
# zhangzhong
from app.models import ChatRecord, Character
from pydantic import ValidationError


def test_chat_record() -> None:
    chat_record = ChatRecord(role="user", content="hello")
    assert chat_record.role == "user"
    assert chat_record.content == "hello"

    try:
        chat_record = ChatRecord(role="should_fail", content="hello")  # type: ignore
        assert False
    except ValidationError as e:
        assert True
    except:
        assert False


def test_dump_chat_history() -> None:
    character = Character(
        bot_name="bot_name",
        bot_info="bot_info",
        user_name="user_name",
        user_info="user_info",
        chat_history=[
            ChatRecord(role="user", content="hello"),
            ChatRecord(role="assistant", content="hi"),
        ],
    )

    character_dict = character.model_dump()
    print(character_dict)
    print(character_dict["chat_history"])
    # 他俩为什么是一样的？
    assert character_dict["chat_history"] == character.dump_chat_history()
