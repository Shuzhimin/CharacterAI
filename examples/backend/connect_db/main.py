from pymongo import MongoClient

# 创建MongoDB客户端
client = MongoClient('localhost', 27017)

# 连接到你的数据库
db = client.CharacterAI


# - 1、获取所有创建角色姓名 @app.get(/names/query')
#   - 输入：无
#   - 输出：{
#     "bot_names":  list
#     }
async def get_bot_name():
    table_info = db.character_info
    res=table_info.find({}, {'bot_name': 1})
    res1=list(res)
    bot_name_list = [doc['bot_name'] for doc in res1]
    return bot_name_list

#- 2、根据角色姓名(bot_name)返回角色信息 @app.get(/character/query')
  # - 输入：bot_name: str
  # - 输出：{
  #   "bot_name": str,
  #   "bot_info": str,
  #   "user_name": str,
  #   "user_info": str
  #   }
async def get_usr_bot_info(bot_name):
    table=db.character_info
    res=table.find({'bot_name':bot_name})
    #处理游标
    first_doc = next(res)
# 获取第一个文档的'username'字段值
    bot_name = first_doc['bot_name']
    bot_info=first_doc["bot_info"]
    user_name = first_doc['user_name']
    user_info=first_doc["user_info"]
    return bot_name,bot_info,user_name,user_info


# - 3、根据角色姓名(bot_name)删除该角色信息 @app.get('character/delete')
#   - 输入：bot_name: str
#   - 输出：{
#     "success": success / fail
#     }
async def delete_bot(bot_name):
    table=db.character_info
    x=table.delete_one({'bot_name':bot_name})
    # 检查删除是否成功
    if x.deleted_count > 0:
        return ("success")
    else:
        return ("fail")


# 关闭数据库连接
#client.close()