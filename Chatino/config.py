from Chatino.base_logger import get_logger


class ResultMessage:
    class Error:
        error = 'Unknown error.'
        data = 'Invalid data.'
        cmd = 'Invalid command.'
        login = 'Login failed.'
        args = 'Invalid args.'
        room = 'No such of this room.'

    class Success:
        success = 'Success.'


# result_message = ResultMessage()

code = {
    '0': ResultMessage.Success.success,
    '1': ResultMessage.Error.error,
    '2': ResultMessage.Error.data,
    '3': ResultMessage.Error.login,
    '4': ResultMessage.Error.cmd,
    '5': ResultMessage.Error.args,
    '6': ResultMessage.Error.room,
}


class Secret:
    # 长度为62，大小写加上数字再打乱。
    """
import random
s1 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
s2 = s1.lower()
s3 = '0123456789'
s = s1 +s2 + s3
z = list(s)
a = ''
for i in z:
    a = a + str(i)
print(a)
    """
    trip = 'Z5q19nAL7XJOR0dNugMk2HIQa6WifPVclzyK8SEoGeFh3TvUpDbxCBYsrw4jtm'


class MessageType:
    text = 'text'
    image = 'image'
    file = 'file'
    link = 'link'


class Visibility:
    public = 'public'
    private = 'private'


class Direction:
    public = None


class Status:
    available = 'available'
    unavailable = 'unavailable'


class Message:
    def __init__(self, room: str, username: str, content: str, time: float,
                 type_: MessageType = MessageType.text, visibility: Visibility = Visibility.public,
                 status: Status = Status.available, direction: Direction = Direction.public):
        self.room, self.username, self.content, self.time, self.type_, self.visibility, self.status, self.direction = \
            room, username, content, time, type_, visibility, status, direction

    def to_dict(self):
        return {
            'room': self.room,
            'username': self.username,
            'content': self.content,
            'time': self.time,
            'type': self.type_,
            'visibility': self.visibility,
            'status': self.status,
            'direction': self.direction,
        }


# 在内存中一个人表示成一个单位
class Unit:
    def __init__(self, username: str, token: str, ws, user: dict = None):
        self.username, self.token, self.ws, self.user = username, token, ws, user

    def to_dict(self):
        return {
            'username': self.username,
            'token': self.token,
            # 'ws': self.ws,
            'user': self.user,
        }


# 权限设置，数字越高权限越大。
# 不同操作需要的权限等级不同
class Role:
    # 使用匿名身份登录的人
    anonym = 0
    # 已经注册的用户
    member = 1
    # 机器人
    bot = 2
    # VIP用户
    vip = 3
    # admin管理用户，拥有很高权限
    admin = 81
    # 网站拥有者，拥有最高权限
    owner = 0x80000000


'''
常量部分
'''

# WS_BIND = '0.0.0.0'
WS_BIND = 'localhost'
WS_PORT = 10086

'''
Exception 部分
'''


class ChatinoException:
    class BaseException(Exception):
        def __init__(self, exception_message):
            self.message = exception_message
            self.error_type = ''
            self.my_init()

        def my_init(self):
            # 重写my_init方法可以做到在继承的class里面实现__init__的效果
            pass

        def __str__(self):
            e_type = ''
            if len(self.error_type) != 0:
                e_type = '(%s)' % self.error_type
            return 'Chatino Error ' + e_type + ': ' + self.message

    class PasswordProvidingError(BaseException):
        def my_init(self):
            self.error_type = 'Password Providing Error'

    class UsernameNotFound(BaseException):
        def my_init(self):
            self.error_type = 'Username Not Found Error'

    class RoomNotFound(BaseException):
        def my_init(self):
            self.error_type = 'Room Not Found Error'



'''
Running 部分：在运行中使用的全局变量
'''

logger = get_logger(__name__)

# 所有在线的用户
# 格式{user: {username: ..., trip: ..., status: ...}, ws, token: ..., web: {start_time, ip, }}
# 利用ws可以向单个用户post消息
online_users = {}

# 房间中的人，{username: unit}
room_users = {}

