"""
Description: Chatino数据库操作部分
"""

import pymongo
import hashlib
import time
from Chatino.config import ChatinoException
from Chatino import utils, config


class ChatinoDB:
    # user部分以username为“主键”
    def __init__(self):
        self.db = pymongo.MongoClient()
        self.col = self.db.chatino
        self.message_mid_create()
        self.logs_lid_create()

    def user_find(self, username):
        data = list(self.col.user.find({'username': username}))
        if len(data) == 0:
            raise ChatinoException.UsernameNotFound('User %s not found!' % username)
        return data[0]

    # 用户是否存在
    def user_exist(self, username) -> bool:
        if len(list(self.col.user.find({'username': username}))) > 0:
            return True
        return False

    def user_verify(self, username: str, password=None, password_md5=None) -> bool:
        if password is None and password_md5 is None:
            raise ChatinoException.PasswordProvidingError('Must provide one password!')
        if password_md5 is None:
            password_md5 = hashlib.md5(password.encode()).hexdigest()
        data = list(self.col.user.find({'username': username, 'password': password_md5}))
        if len(data) == 0:
            return False
        return True

    def user_create(self, username: str, password=None, password_md5=None, trip=None) -> bool:
        if password is None and password_md5 is None:
            raise ChatinoException.PasswordProvidingError('Must provide one password!')
        if self.user_exist(username):
            return False
        if password_md5 is None:
            password_md5 = hashlib.md5(password.encode()).hexdigest()
        # trip可以自定义
        if trip is None:
            trip = utils.randstr(password_md5)
        self.col.user.insert_one({
            'username': username,
            # 这里的密码应该已经被加密
            'password': password_md5,
            'trip': trip,
            'info': {},
        })
        return False

    # 对info中的信息更新
    def user_info_update(self, username: str, info: dict) -> bool:
        if not self.user_exist(username):
            return False
        user = self.user_find(username)
        # 保留丢入参数之外的信息
        for i in info:
            user['info'][i] = info[i]
        # 直接替换文档
        self.col.user.update_one({'username': username}, {'$set': {'info': user['info']}})
        return True

    def user_delete(self, username: str) -> bool:
        # 请在移除用户之前验证身份并且保持用户存在
        if not self.user_exist(username):
            return False
        self.col.user.delete_one({'username': username})
        return True

    def token_exist(self, token: str) -> bool:
        if len(list(self.col.token.find({'token': token}))) == 0:
            return False
        return True

    def token_username_exist(self, username: str) -> bool:
        if len(list(self.col.token.find({'username': username}))) == 0:
            return False
        return True

    # 返回{username, token}
    def token_find_username(self, username: str):
        if not self.token_username_exist(username):
            return None
        return list(self.col.token.find({'username': username}))[0]

    def token_find(self, token: str):
        if not self.token_exist(token):
            return None
        return list(self.col.token.find({'token': token}))[0]

    def token_to_username(self, token):
        data = self.token_find(token)
        if data is None:
            return None
        return data['username']

    # 生成token，返回{'username': ..., 'token': ..., 'trip': ...}
    # token储存结构{username, token, create_time}
    # 生成token代码：md5(username + trip + time.time()), md5(username + time.time())
    def token_create(self, username) -> dict:
        # 匿名模式下不注册
        if not self.user_exist(username):
            # 匿名了
            # raise ChatinoException.UsernameNotFound('Username %s not found!' % username)
            token = hashlib.md5((username + str(time.time())).encode()).hexdigest()
            result = {'username': username, 'token': token}
        else:
            user = self.user_find(username)
            # 直接使用user结构，增加token项目
            result = user

            token = hashlib.md5((username + user['trip'] + str(time.time())).encode()).hexdigest()
            result['token'] = token

        # 在数据库中单独储存token
        if not self.token_username_exist(username):
            self.col.token.insert_one({
                'username': username,
                'token': token,
                'create_time': time.time(),
            })
        else:
            self.col.token.update_one({'username': username}, {'$set': {'token': token, 'create_time': time.time()}})

        return result

    def token_destroy(self, username):
        if not self.token_username_exist(username):
            raise ChatinoException.UsernameNotFound('Token %s not found!' % username)

    def message_mid_create(self):
        query = list(self.col.message.find({'updated': True}))
        if len(query) == 0:
            to_insert = {"_id": "mid", "val": 0, 'updated': True}
            self.col.message.insert_one(to_insert)

    # 使mid自增
    def message_mid_increase(self) -> int:
        # 初始化mid
        query = list(self.col.message.find({'updated': True}))
        data = query[0]
        val = data['val'] + 1
        self.col.message.update_one({'updated': True}, {'$set': {'val': val}})
        return val

    # message部分以mid为“主键”
    def message_insert(self, room: str, username: str, type_: str, content: str,
                       visibility: str = config.Visibility.public, status: str = config.Status.available,
                       direction=config.Direction.public):
        self.col.message.insert_one({
            # 把_id设置为自增，并且在每次插入都自动执行
            "_id": self.message_mid_increase(),
            'room': room,
            'username': username,
            'type': type_,
            'content': content,
            # 这里记录到毫秒后面，带小数点
            'time': time.time(),
            # 默认是公聊，可以私聊，私聊需要指定目标(->username)
            'visibility': visibility,
            'direction': direction,
            # unavailable来标志那些已经不可用的消息
            'status': status,
        })

    # 查询历史记录，注意是倒着查询
    # 查找某一条消息之前的limit条消息
    # 输入mid == 0表示从最先开始查询
    # 返回查找的结果（没有转化为list）
    def message_select(self, room: str, username: str, mid: int, limit: int = 30):
        # 设置最大的数
        if mid == 0:
            mid = 0x80000000
        return self.col.message.find({'$or': [
            {'_id': {'$lt': mid}, 'room': room, 'visibility': config.Visibility.public},
            {'_id': {'$lt': mid}, 'room': room, 'visibility': config.Visibility.private, 'direction': username},
        ]}).sort([("_id", -1), ]).limit(limit)

    def logs_lid_create(self):
        query = list(self.col.logs.find({'updated': True}))
        if len(query) == 0:
            to_insert = {"_id": "lid", "val": 0, 'updated': True}
            self.col.logs.insert_one(to_insert)

    # 使lid自增
    def logs_lid_increase(self) -> int:
        # 初始化mid
        query = list(self.col.logs.find({'updated': True}))
        data = query[0]
        val = data['val'] + 1
        self.col.logs.update_one({'updated': True}, {'$set': {'val': val}})
        return val

    def logs_insert(self, data: dict):
        self.col.logs.insert_one({
            "_id": self.logs_lid_increase(),
            "data": data,
        })

    def logs_select(self, lid: int, limit: int = 30):
        if lid == 0:
            lid = 0x800000
        return self.col.logs.find({'_id': {'$lt': lid}}).sort([('_id', -1), ]).limit(limit)


if __name__ == '__main__':
    _db = ChatinoDB()

    # # 用户部分测试
    # print('user_find', _db.user_find('chino'))
    # print('user_create', _db.user_create('chino', ''))
    # print('user_find', _db.user_find('chino'))
    # print('user_info_update', _db.user_info_update('chino', {'motto': 'less is more.'}))
    # print('user_find', _db.user_find('chino'))
    # print('user_delete', _db.user_delete('chino'))
    # print('user_find', _db.user_find('chino'))

    # # 消息测试
    # print('message_insert', _db.message_insert('lounge', 'chino', config.MessageType.text, 'TEST TEXT'))
    # print('message_select', list(_db.message_select('lounge', 'chiro', 0)))

    # # 日志系统测试
    # print('logs_insert', _db.logs_insert({'code': 0, 'message': 'Success', 'data': {}}))
    # print('logs_select', list(_db.logs_select(0)))

    # # token系统测试
    # _create = _db.token_create('chino')
    # print('token_create', _create)
    # _token = _create['token']
    # print('token_find', _db.token_find('chino'))
    # print('token_username_exist', _db.token_username_exist('chino'))
    # print('token_to_username', _db.token_to_username(_token))
    # print('token_destroy', _db.token_destroy('chino'))
    # print('token_find', _db.token_find('chino'))

    pass


