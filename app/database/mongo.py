# from pymongo import MongoClient
# from app.models import Character
# from app.common.conf import conf
# from app.common.error import Error

# client = MongoClient(**conf.get_mongo_setting())
# db = client[conf.get_mongo_database()]
# collection = db[conf.get_mongo_character_collname()]


# def create_character(character: Character) -> Error:
#     result = collection.find_one(filter={"bot_name": character.bot_name})
#     if result is None:
#         collection.insert_one(document=character.model_dump())
#         return Error.OK
#     else:
#         return Error.CHARACTER_ALREADY_EXISTS


# def update_character(character: Character) -> Error:
#     result = collection.find_one(filter={"bot_name": character.bot_name})
#     if result is None:
#         return Error.CHARACTER_NOT_FOUND

#     collection.update_one(
#         filter={"bot_name": character.bot_name},
#         update={"$set": character.model_dump()},
#     )
#     return Error.OK


# def get_character(filter: dict) -> tuple[Error, Character | None]:
#     result = collection.find_one(filter=filter)
#     if result is None:
#         return Error.CHARACTER_NOT_FOUND, None
#     else:
#         return Error.OK, Character(**result)


# def get_characters(filter: dict) -> tuple[Error, list[Character]]:
#     result = collection.find(filter=filter)
#     characters = [Character(**item) for item in result]
#     return Error.OK, characters


# def delete_character(filter: dict) -> Error:
#     result = collection.delete_one(filter=filter)
#     if result.deleted_count == 0:
#         return Error.CHARACTER_NOT_FOUND
#     else:
#         return Error.OK
