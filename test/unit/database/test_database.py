import uuid
from test.unit.utils import random_character, random_character_category

from app.common import model
from app.database import DatabaseService, schema
from app.database.schema import Base, engine

# TODO: 这句话必须在运行所有代码之前运行 否则就会出错
# 这显然不合理呀
# 现在的单元测试写的不好，因为测试之间竟然有依赖关系，这显然是不对的
Base.metadata.create_all(bind=engine)

# TODO: 当测试一个空的数据库的时候，会导致测试出错，测试用例写的不好

# 现在用户名不准重复了
# 我们需要重新设计我们的单元测试
db = DatabaseService()


def create_user() -> schema.User:
    name = str(uuid.uuid4())
    password = str(uuid.uuid4())
    description = str(uuid.uuid4())

    user = db.create_user(
        model.UserCreate(
            name=name,
            password=password,
            avatar_description=description,
            avatar_url="avatar url",
        )
    )
    return user


# 为什么我的单元测试会写的这么乱呢？
# 我觉得在我继续实现新功能之前 还是好好重构一下单元测试吧
def create_character(user: schema.User) -> schema.Character:
    # 提供一个random的方法让其他的单元测试进行调用？
    # 这是好的吗，如果一个代码只有单元测试才需要使用
    # 哪他就不应该出现在代码里 而应该仅仅出现的测试代码库中
    # 所以我们真正要做的是提供一个random_character的方法
    # 才是对的
    # 我们应该提供一个专用于测试的模块 然后其他的测试可以调用这个模块
    character = db.create_character(character=random_character(uid=user.uid))
    return character


def create_chat(user: schema.User, character: schema.Character) -> schema.Chat:
    chat = db.create_chat(
        model.ChatCreate(
            uid=user.uid,
            cid=character.cid,
        )
    )
    return chat


def test_create_update_delete_user():
    user = create_user()
    print(user.uid)

    new_username = str(uuid.uuid4())
    new_description = str(uuid.uuid4())
    new_user = db.update_user(
        uid=user.uid,  # 卧槽啊，果然就没有type hint error了
        user_update=model.UserUpdate(
            name=new_username,
            avatar_description=new_description,
            avatar_url="avatar url",
        ),
    )
    assert new_user.name == new_username
    assert new_user.password == user.password
    assert new_user.avatar_description == new_description

    db.delete_user(uid=user.uid)
    user = db.get_user(uid=user.uid)
    assert user.is_deleted


def test_create_update_delete_character():
    user = create_user()
    character = create_character(user=user)

    new_character_name = str(uuid.uuid4())
    new_character_description = str(uuid.uuid4())
    new_character_category = random_character_category()
    new_character = db.update_character(
        cid=character.cid,
        character_update=model.CharacterUpdate(
            name=new_character_name,
            description=new_character_description,
            category=new_character_category,
        ),
    )
    assert new_character.name == new_character_name
    assert new_character.description == new_character_description
    assert new_character.category == new_character_category

    db.delete_character(cid=character.cid)
    character = db.get_character(cid=character.cid)
    assert character.is_deleted


def test_chat():
    user = create_user()
    character = create_character(user=user)
    chat = create_chat(user=user, character=character)

    db.create_content(
        content_create=model.MessageCreate(
            chat_id=chat.chat_id, content="test", sender=user.uid
        )
    )
    db.create_content(
        content_create=model.MessageCreate(
            chat_id=chat.chat_id, content="test", sender=character.cid
        )
    )
    print(chat.messages)
