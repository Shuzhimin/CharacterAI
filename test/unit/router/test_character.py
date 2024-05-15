import random
import uuid
from test.unit.utils import random_character_category

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
    # 这里就必须换成form了
    response = client.post(
        url=f"{prefix}/create",
        headers={"Authorization": f"{token.token_type} {token.access_token}"},
        data=model.CharacterCreate(
            name=str(uuid.uuid4()),
            description=str(uuid.uuid4()),
            avatar_description=str(uuid.uuid4()),
            avatar_url=avatar_url,
            category=random_character_category(),
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
    select_response = model.CharacterSelectResponse(**response.json())
    characters = select_response.characters
    print(characters)
    assert len(characters) > 0
    character = characters[0]

    # select character by query
    response = client.get(
        url=f"{prefix}/select?query={character.name}",
        headers={"Authorization": f"{token.token_type} {token.access_token}"},
    )
    assert response.status_code == 200
    print(response.json())
    select_response = model.CharacterSelectResponse(**response.json())
    characters = select_response.characters
    print(characters)
    assert len(characters) > 0
    character = characters[0]

    # update character
    new_character_name = str(uuid.uuid4())
    new_character_description = str(uuid.uuid4())
    new_character_category = random_character_category()
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

    # after delete, we should not get it from api
    response = client.get(
        url=f"{prefix}/select",
        headers={"Authorization": f"{token.token_type} {token.access_token}"},
    )
    select_response = model.CharacterSelectResponse(**response.json())
    characters = select_response.characters
    assert len(characters) == 0
