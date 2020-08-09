"""
Description: Chatino数据库操作部分
"""

import pymongo
import hashlib


class ChatinoDB:
    def __init__(self):
        self.db = pymongo.MongoClient()
        self.col = self.db.chatino

    def user_verify(self, username, password):
        self.col.user.find({})

    def user_new(self, username: str, password=None, password_md5=None, trip=None):
        if password is None and password_md5 is None:
            raise Exception("Must provide one password!")
        if password_md5 is None:
            password_md5 = hashlib.md5(password.encode()).hexdigest()
        self.col.user.insert_one({
            'username': username,
            # 这里的密码应该已经在上一层被加密
            'password': password_md5,
            'trip': trip,
        })

    def user_delete(self, username):
        # 请在移除用户之前验证身份
        self.col.user.remove({'username': username})

