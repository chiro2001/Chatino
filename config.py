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
