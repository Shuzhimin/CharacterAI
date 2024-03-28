from app.models import CharacterV2, CharacterCreate, CharacterUpdate, CharacterWhere
import app.database.pgsql as pg


def test_select_character():
    # 测试CharacterWhere的输入不为空的情况
    character_where = CharacterWhere(cid=1)
    characters = pg.select_character(where=character_where)

    print("------------------------------")
    # 测试CharacterWhere的输入为空的情况
    character_where = CharacterWhere()
    characters = pg.select_character(where=character_where)
    