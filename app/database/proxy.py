# 2024/2/6
# zhangzhong
from app.common.conf import ZhipuAIConf
#from app.dependencies import get_current_uid
from app.models import Character, ChatRecord, CharacterV2, CharacterCreate, CharacterUpdate
import app.database.mongo as mongo
from app.common.error import Error, ErrorV2
import app.models as model
import app.common.error as error
import app.models as model
import app.database.pgsql as pg


# CRUD: Create, Read, Update, Delete
class DatabaseProxy:
    def __init__(self) -> None:
        pass

    # class CharacterV2(BaseModel):
    #     cid: int = Field(default=..., description="机器人id")1
    #     character_name: str = Field(default=..., description="机器人名称")1
    #     character_info: str = Field(default=..., description="机器人信息")1
    #     character_class: str = Field(default=..., description="机器人类型")1
    #     avatar_url: str = Field(default=..., description="头像url")1
    #     create_time: datetime = Field(default=..., description="创建时间")1
    #     update_time: datetime = Field(default=..., description="更新时间")1
    #     status: str = Field(default=..., description="状态")1
    #     attr: str = Field(default=..., description="属性")

    # class CharacterCreate(BaseModel):
    #     character_name: str = Field(default=..., description="机器人名称")1
    #     character_info: str = Field(default=..., description="机器人信息")1
    #     character_class: str = Field(default=..., description="机器人类型")1
    #     avatar_url: str = Field(default=..., description="头像url")1
    #     status: str = Field(default="active", description="状态")1
    #     attr: str = Field(default="normal", description="属性")

    def create_character(self, character: CharacterCreate) -> Error:
        err = mongo.get_character(character.character_name),
        if err.code == Error.OK:
            return Error(code=2, message="机器人已经存在")
        characterv2 = CharacterV2(),
        characterv2.cid = uuid.uuid4(),
        characterv2.character_name = character.character_name,
        characterv2.character_info = character.character_info,
        characterv2.character_class = character.character_class,
        characterv2.avatar_url = character.avatar_url,
        now = datetime.now(),
        characterv2.create_time = now.strftime("%Y-%m-%d %H:%M:%S"),
        characterv2.update_time = character.create_time,
        characterv2.status = character.status,
        uid = get_current_uid()
        if uid == "管理员uid":
            characterv2.attr = character.attr
        else:
            characterv2.attr = "Normal"
        return Error(code=0, message="OK")

    #    return mongo.create_character(character=character)

    def update_character(self, character: CharacterUpdate) -> Error:
        uid_owner = self.get_uid_by_cid()
        if uid_owner != get_current_uid() & get_current_uid() != "管理员uid":
            return Error(code=2, message="没有该机器人角色")

        return Error(code=0, message="OK")

    #        return mongo.update_character(character=character)

    def character_select1(self,cids,offset,limit,acsend):
        uid = get_current_uid(),
        #需要通过uid查询cid
        cids = self.get_cid_by_uid(),
        cids.sort(reversed=acsend)
        result = cids[offset:limit]
        #根据result里的/cid查询角色的相关信息  character_name, character_info, avatar, character_class
        return #返回这里写不来了




    def get_cid_by_uid(self, uid: str):
        return [22,12] #返回的应该是一个列表

    # TODO:
    # None对象和用NoneObject来代替呀，refactor一书中就提到了这个技巧
    # 这样我们就不用做none判断了
    def get_character_by_botname(self, botname: str) -> tuple[Error, Character | None]:
        return mongo.get_character(filter={"bot_name": botname})

    def delete_character_by_botname(self, botname: str) -> Error:
        return mongo.delete_character(filter={"bot_name": botname})

    def delete_character_by_cid(self, cid: list[int]):
        err, character = mongo.get_characters(cid)
        err1, uid = self.get_uid_by_cid(),
        if err.code == Error.CHARACTER_NOT_FOUND | uid != get_current_uid() | get_current_uid() != "管理员id":
            return Error(code=3, message="机器人不存在")
        # 还需要进行判断机器人的状态status是不是delete


        # 进行删除操作
        character.status = "delete"
        return Error(code=0, messagr="OK")

    def generate_avatar(self, avatar_describe: str):
        zhipu = ZhipuAIConf()
        client = ZhipuAI(api_key=zhipu.api_key)  # 请填写您自已的APIKey
        response = client.images.generations(
            model="cogview-3",
            prompt=avatar_describe, )
        return Error(code=0,message=response.data[0].url)
       # return (response.data[0].url)  #这里的返回值应该是什么我不清楚，或者说该怎么写呢

    def get_uid_by_cid(self, cid: str) -> tuple[Error, int]:
        return Error(code=0, message="OK"), 1

    def append_chat_recoards(
            self, botname: str, chat_records: list[ChatRecord]
    ) -> Error:
        error, character = self.get_character_by_botname(botname=botname)
        if not error.ok() or character is None:
            return error
        character.chat_history.extend(chat_records)
        return mongo.update_character(character=character)

    def get_all_characters(self) -> tuple[Error, list[Character]]:
        return mongo.get_characters(filter={})

    def authenticate_then_get_user(
        self, username: str, password: str
    ) -> tuple[ErrorV2, model.User | None]:
        err, user = self.get_user_by_username(username=username)
        if not err.is_ok() or not user:
            return err, None

        if user.passwd != password:
            return error.unauthorized(), None
        return error.ok(), user

    def create_user(
        self, username: str, password: str, avatar_url: str
    ) -> tuple[ErrorV2, model.User | None]:
        user = model.User.new(
            username=username, password=password, avatar_url=avatar_url
        )
        err = pg.create_user(user=user)
        # 然后我们还需要拿到这个user
        if not err.is_ok():
            return err, None
        err, user = self.get_user_by_username(username=username)
        return err, user
        # return err, user if err.is_ok() else None

    def get_user_by_username(self, username: str) -> tuple[ErrorV2, model.User | None]:
        users = pg.select_user(user_filter=model.UserFilter(username=username))
        if len(users) == 0:
            return error.not_found(), None
        else:
            return error.ok(), users[0]

    def delete_user_by_username(self, username: str) -> ErrorV2:
        return pg.delete_user(user_filter=model.UserFilter(username=username))

    def get_user_by_uid(self, uid: int) -> tuple[ErrorV2, model.User | None]:
        users = pg.select_user(user_filter=model.UserFilter(uid=uid))
        if len(users) == 0:
            return error.not_found(), None
        else:
            return error.ok(), users[0]

    def update_user_by_uid(self, uid: int, username: str, avatar_url: str) -> ErrorV2:
        return pg.update_user(
            user_update=model.UserUpdate(username=username, avatar_url=avatar_url),
            user_filter=model.UserFilter(uid=uid),
        )
