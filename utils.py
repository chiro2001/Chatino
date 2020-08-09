import json
import config
import hashlib


"""
返回值格式：
{
    code: ...,
    message: ...,
    data: ...,
}
"""


def make_result(code: int, message=None, data=None):
    result = {
        'code': code,
    }
    # 根据code选message
    if message is None:
        result['message'] = config.code[str(code)]
    else:
        result['message'] = message
    if data is not None:
        result['data'] = data
    return result


def make_error_result(error):
    return make_result(1, message=str(error))


def dump(data):
    return json.dumps(data)


# 命令基本合理性检查
def verify(data):
    if 'cmd' not in data or 'args' not in data:
        return False
    return True


# 生成随机字符串
# 62位进制转换法
def randstr(data):
    md5 = hashlib.md5(data.encode()).hexdigest()
    # md5长度32位，舍弃最后两位，每5位生成数字对62取模，然后对应secret_trip
    m = md5[:-2]
    li = []
    for i in range(6):
        li.append(int('0x' + m[i * 5: i * 5 + 5], 16))
    li = list(map(lambda x: config.Secret.trip[x % 62], li))
    result = ''
    for i in li:
        result = result + i
    return result


if __name__ == '__main__':
    print(randstr('fdsjioltdsarjhtkasuertiouytuewioptiu'))
