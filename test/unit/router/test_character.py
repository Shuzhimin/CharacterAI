import uuid

from fastapi.testclient import TestClient

from app.common import model
from app.database import DatabaseService
from app.dependency import parse_token
from app.main import app

client = TestClient(app)

db = DatabaseService()

prefix = "/api/character"


# 为痕么create character会去 update chats
def test_character(token: model.Token, avatar_url: str):
    uid = parse_token(token.access_token).uid

    # create character
    response = client.post(
        url=f"{prefix}/create",
        headers={"Authorization": f"{token.token_type} {token.access_token}"},
        json=model.CharacterCreate(
            name=str(uuid.uuid4()),
            description=str(uuid.uuid4()),
            avatar_description=str(uuid.uuid4()),
            avatar_url=avatar_url,
            category=str(uuid.uuid4()),
            uid=uid,
        ).model_dump(),
    )
    assert response.status_code == 200
    print(response.json())
    character = model.CharacterOut(**response.json())
    print(character)

    # select character
    response = client.get(
        url=f"{prefix}/select",
        headers={"Authorization": f"{token.token_type} {token.access_token}"},
    )
    assert response.status_code == 200
    print(response.json())
    characters = [model.CharacterOut(**c) for c in response.json()]
    print(characters)
    assert len(characters) > 0
    character = characters[0]

    # update character
    new_character_name = str(uuid.uuid4())
    new_character_description = str(uuid.uuid4())
    new_character_category = str(uuid.uuid4())
    response = client.post(
        url=f"{prefix}/update?cid={characters[0].cid}",
        headers={"Authorization": f"{token.token_type} {token.access_token}"},
        json=model.CharacterUpdate(
            name=new_character_name,
            description=new_character_description,
            category=new_character_category,
        ).model_dump(),
    )
    assert response.status_code == 200
    print(response.json())
    character = model.CharacterOut(**response.json())
    print(character)
    assert character.name == new_character_name
    assert character.description == new_character_description
    assert character.category == new_character_category

    # delete character
    response = client.post(
        url=f"{prefix}/delete",
        headers={"Authorization": f"{token.token_type} {token.access_token}"},
        json=[character.cid],
    )
    assert response.status_code == 200
    print(response.json())

    character = db.get_character(cid=character.cid)
    assert character.is_deleted
