import httpx
from app.main import app
from fastapi.testclient import TestClient

from app.model.character import CharacterSelectRequests
from app.models import CharacterCreate


client = TestClient(app)
#有一个的cid是101
#接口1.1
def test_createcharacter():
    response: httpx.Response = client.post(
        url = '/character/create',
        json={"character_name": 'stcgwaza', 'character_info':'111' , 'character_class':'5455' , 'avatar_url':'222'}                
    )
    assert response.status_code == 200
    r = response.json()
    print(r)
    if r.get("code") == 1:
        print("")
    
#接口1.2
def test_deletecharacter():
    # 发送 DELETE 请求，包含 JSON 请求体
    response: httpx.Response = client.post(
        url='/character/delete',
        json={"cids": [100000000000,]}
        )
    
    assert response.status_code == 200
    print(response.json())

#接口1.3
def test_updatacharacter():
    response: httpx.Response = client.post(
    url='/character/update',
    json={"cid": 10,"character_name":"wad"}
    #params={"cids": 10,"character_name":"wad"}
    )
    print(response.json())
    assert response.status_code == 200
    print(response.json())

#接口1.6
def test_generate_avatar():
    response: httpx.Response = client.post(
        url='/character/avatar',
        params={"avatar_describe": '好看美丽的'}
    )
    assert response.status_code == 200
    print(response.json())

ca = CharacterSelectRequests()

#接口1.7  不传参 返回所有会失败  没有实现返回所有的角色
def test_character_select():
    response: httpx.Response = client.post(
        url='/character/select',
        json={"cids": [101]}
    )
    print(response.request)
    # print('1111111',response.text)
    # print('222222222222222222222222222222',response.json())
    assert response.status_code == 200
    print(response.json())
    





"""    response: httpx.Response = client.post(
        url="/register",
        data={"username": username, "password": password, "avatar_describe": "test"},
    )
 """


"""     character_name: str = Field(default=..., description="机器人名称")
    character_info: str = Field(default=..., description="机器人信息")
    character_class: str = Field(default=..., description="机器人类型")
    avatar_url: str = Field(default=..., description="头像url")
    status: str = Field(default="active", description="状态")
    attr: str = Field(default="normal", description="属性") """

""" client = TestClient(app)
username = "myname"
password = "123456"


# 但是我们首先需要创建用户啊
def test_register():
    # username = "myname"
    # 妈的 在最开始删掉这个角色吧
    db = DatabaseProxy()
    err = db.delete_user_by_username(username=username)
    assert err.is_ok()

    response: httpx.Response = client.post(
        url="/register",
        data={"username": username, "password": password, "avatar_describe": "test"},
    )
    assert response.status_code == 200
    # assert response.json() == {"code": 0, "message": "ok", "data": {"uid": 1}}
    assert response.json().get("code") == 0

    # 检查用户是否存在
    err, user = db.get_user_by_username(username=username)
    assert err.is_ok() and user
    assert str(user.uid) == response.json().get("data").get("uid") """