from fastapi.testclient import TestClient
from app.database.proxy import DatabaseProxy
from app.main import app
from httpx import Response
from app.model_deprecated.user import UserMeResponse


client = TestClient(app)


def test_create_chat():
    db = DatabaseProxy()

    response = client.post(
        url="/chat/create?cid=10",
    )
    assert response.status_code == 200
    assert response.json().get("code") == 0

    err, chat = db.get_chat_by_cid_uid(cid=10, uid=3)
    print("chat:", chat)
    assert err.is_ok() and chat


def test_delete_chat():
    db = DatabaseProxy()
    response = client.post(
        url="/chat/delete?chat_id=11",
    )
    assert response.status_code == 200
    assert response.json().get("code") == 0


def test_append_chat():
    db = DatabaseProxy()
    response = client.post(
        url="/chat/append?character_name=苏梦远&character_info=苏梦远，本名苏远心，是一位当红的国内女歌手及演员。在参加选秀节目后，凭借独特的嗓音及出众的舞台魅力迅速成名，进入娱乐圈。她外表美丽动人，但真正的魅力在于她的才华和勤奋。苏梦远是音乐学院毕业的优秀生，善于创作，拥有多首热门原创歌曲。除了音乐方面的成就，她还热衷于慈善事业，积极参加公益活动，用实际行动传递正能量。在工作中，她对待工作非常敬业，拍戏时总是全身心投入角色，赢得了业内人士的赞誉和粉丝的喜爱。虽然在娱乐圈，但她始终保持低调、谦逊的态度，深得同行尊重。在表达时，苏梦远喜欢使用“我们”和“一起”，强调团队精神&chat_id=2&content=hello",
    )
    assert response.status_code == 200
    assert response.json().get("code") == 0


def test_select_chat():
    db = DatabaseProxy()
    response = client.get(
        url="/chat/select",
    )
    assert response.status_code == 200
    assert response.json().get("code") == 0


def test_clear_chat_history():
    db = DatabaseProxy()
    err = db.clear_chat_by_chat_id(chat_id=63)
    assert err.is_ok()


def test_chat_update_construction():
    from app.model_deprecated.chat import ChatRecord, ChatUpdate

    chat_record = ChatRecord(who="user", message="hello")
    chat_update = ChatUpdate(chat_record=chat_record)
    assert chat_record.who == "user" and chat_record.message == "hello"
    assert (
        chat_update.chat_record.who == "user"
        and chat_update.chat_record.message == "hello"
    )


def test_update_chat_pgsql():
    import app.database.pgsql as pg
    from app.model_deprecated.chat import ChatRecord, ChatUpdate, ChatWhere

    chat_record = ChatRecord(who="user", message="hello")
    chat_id = 7
    pg.update_chat(
        chat_update=ChatUpdate(chat_record=chat_record),
        where=ChatWhere(chat_id=chat_id),
    )
