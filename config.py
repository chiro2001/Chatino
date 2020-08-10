class Message:
    class Error:
        error = 'Unknown Error.'
        data = 'Invalid data.'
        cmd = 'Invalid command.'

    class Success:
        success = 'Success.'


message = Message()

code = {
    '0': message.Success.success,
    '1': message.Error.error,
    '2': message.Error.data,
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


class Status:
    available = 'available'
    unavailable = 'unavailable'


class Visibility:
    public = 'public'
    private = 'private'


class Direction:
    public = None


'''
常量部分
'''

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
