# 2024/4/25
# zhangzhong

import random
import uuid

from app.common.model import CharacterCreate


def default_character_avatar_url() -> str:
    return "avatar url"


def random_character_category() -> str:
    return random.choice(["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"])


def random_character(uid: int) -> CharacterCreate:
    return CharacterCreate(
        uid=uid,
        name="test",
        description="random character description",
        avatar_url=default_character_avatar_url(),
        category=random_character_category(),
    )
