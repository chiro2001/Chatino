"""
Description: Chatino主逻辑
"""


import json
import asyncio
import websockets
from Chatino.database import *
from Chatino import config, Commamnds as commands
from Chatino.config import logger, ChatinoException
from Chatino import utils


class Chatino:
    def __init__(self):
        self.db = ChatinoDB()
        self.myws = websockets.serve(self.ws_main, config.WS_BIND, config.WS_PORT)

    # 这个函数在每一次打开新的连接就会打开
    async def ws_main(self, ws, path):
        logger.debug(str(type(ws)))
        logger.info('started new conn(path=%s)' % path)
        # 必须经过start阶段才能继续
        unit: config.Unit = await self.ws_start(ws)
        # 然后开始处理命令
        if unit is None:
            return
        await self.parser(ws, unit)

        # 执行结束，注销用户的token
        self.logout(unit.username)

    async def ws_start(self, ws) -> config.Unit:
        while True:
            try:
                try:
                    raw = await ws.recv()
                    # print('raw', raw)
                    data = json.loads(raw)
                except Exception as e:
                    print('except:', utils.make_error_result(e))
                    # 还是有可能发送失败
                    try:
                        await ws.send(utils.dump(utils.make_error_result(e)))
                    except (websockets.exceptions.ConnectionClosedOK, websockets.exceptions.ConnectionClosedError) as e2:
                        logger.warning('Connection error: ' + str(e2))
                        break
                    continue
                # print(data)
                if data is None:
                    # 数据无效
                    await ws.send(utils.dump(utils.make_result(2)))
                    continue
                # 处理数据
                if not utils.verify(data) or data['cmd'] != 'start':
                    # 命令无效
                    await ws.send(utils.dump(utils.make_result(2)))
                    continue
                args = data['args']
                if ('username' not in args and 'token' not in args) or ('username' in args and 'token' in args):
                    # 命令无效（token和username必须有且只有一个）
                    await ws.send(utils.dump(utils.make_result(2)))
                    continue

                # 一下几个选项必须生成token
                token = ''
                unit = None
                if 'username' in args and 'password' not in args:
                    # 匿名模式
                    # 先创建token
                    username = args['username']
                    unit = self.db.token_create(username)
                    token = unit.token
                if 'username' in args and 'password' in args:
                    # 登录模式
                    # 登录校验
                    username, password = args['username'], args['password']
                    if not self.db.user_verify(username, password=password):
                        # 登录失败
                        await ws.send(utils.dump(utils.make_result(3)))
                        continue
                    unit = self.db.token_create(username)
                    token = unit.token
                if 'token' in args:
                    token = args['token']

                username = self.db.token_to_username(token)
                if username is None:
                    # 认证失败
                    await ws.send(utils.dump(utils.make_result(3)))
                    continue
                user = None
                try:
                    user = self.db.user_find(username)
                except ChatinoException.UsernameNotFound:
                    # 找不到user的情况下，user在unit中是None
                    pass
                # for i in user:
                #     unit['user'][i] = user[i]
                # unit = self.unit_create(username, token, ws, user=user)
                # 只提供了token的情况
                if unit is None:
                    unit = config.Unit(username, token, ws, user=user)
                # ws的补充
                if unit.ws is None:
                    unit.ws = ws
                if unit.user is None:
                    unit.user = user
                    # 补充了user之后也可能是None

                # 最后加入online_users，当做登录
                # global config.online_users
                # 注意这里的username变量已经变成None了
                config.online_users[unit.username] = unit
                # 返回成功的值
                await ws.send(utils.dump(utils.make_result(0, data=unit.to_dict())))
                # break
                return unit
            except (websockets.exceptions.ConnectionClosedOK, websockets.exceptions.ConnectionClosedError) as e2:
                logger.warning('Connection error: ' + str(e2))
                break

    # @staticmethod
    def logout(self, username):
        if username not in config.online_users:
            raise ChatinoException.UsernameNotFound("Username %s Not Found!" % username)
        # 退出所有房间
        # 这里有点浪费时间... TODO: 增加用户-房间结构
        # TODO: 增加自动登录房间（放在info里面）
        for room in config.room_users:
            if username in config.room_users[room]:
                del config.room_users[room][username]
        # 注销登录
        del config.online_users[username]
        # 删除token
        self.db.token_destroy(username)

    async def parser(self, ws, unit: config.Unit):
        while True:
            # 还是有可能接收失败
            try:
                try:
                    resp = await ws.recv()
                except (websockets.exceptions.ConnectionClosedError, websockets.exceptions.ConnectionClosedOK) as e:
                    logger.warning('Connection error: ' + str(e))
                    break
                try:
                    data = json.loads(str(resp))
                except json.decoder.JSONDecodeError:
                    # 数据错误
                    await ws.send(utils.dump(utils.make_result(2)))
                    continue
                # 找找有没有对应命令
                cmd = data['cmd']
                args = data['args']
                if cmd not in commands.commands_table:
                    # 命令错误
                    await ws.send(utils.dump(utils.make_result(4)))
                    continue
                # 检查参数合理性
                reasonable = True
                for arg in commands.commands_table[cmd]['args']:
                    if arg not in args and commands.commands_table[cmd]['args'][arg]['necessary']:
                        reasonable = False
                        break
                    if commands.commands_table[cmd]['args'][arg]['type'] is not None and \
                            type(args[arg]) is not commands.commands_table[cmd]['args'][arg]['type']:
                        reasonable = False
                        break
                if not reasonable:
                    # 参数不合理
                    await ws.send(utils.dump(utils.make_result(5)))
                    continue
                logger.debug('Recv: ' + str(resp))
                # username = unit.username
                function = commands.commands_table[cmd]['function']
                result = await function(chatino=self, unit=unit, ws=ws, cmd=cmd, args=args, logger=logger)
                await ws.send(utils.dump(result))
            except (websockets.exceptions.ConnectionClosedError, websockets.exceptions.ConnectionClosedOK) as e:
                logger.warning('Connection error: ' + str(e))
                break

    @staticmethod
    async def join_room(username: str, room: str):
        if username not in config.online_users:
            raise ChatinoException.UsernameNotFound('Username %s Not Found!' % username)
        # 房间不存在，新建房间
        if room not in config.room_users:
            config.room_users[room] = {}
        else:
            # 房间存在，判断是否已经在房间内然后加入
            if username in config.room_users[room]:
                raise ChatinoException.HasInRoom('You Have In Room %s.' % room)
        config.room_users[room][username] = config.online_users[username]

    @staticmethod
    async def exit_room(username: str, room: str):
        if username not in config.online_users:
            raise ChatinoException.UsernameNotFound('Username %s Not Found!' % username)
        if room not in config.room_users:
            raise ChatinoException.RoomNotFound('Room %s Not Found!' % room)
        if username not in config.room_users[room]:
            raise ChatinoException.NotInRoom('Username %s Not In Room %s!' % (username, room))
        del config.room_users[room][username]
        # 房间没人了就删除房间
        if len(config.room_users[room]) == 0:
            del config.room_users[room]

    @staticmethod
    async def push_message(message: config.Message):
        if message.room not in config.room_users:
            raise ChatinoException.RoomNotFound("Room %s Not Found!" % message.room)
        # TODO: 修复public用户收不到私聊的问题（修改config.Direction.pbilic）
        if message.direction == config.Direction.public:
            for username in config.room_users[message.room]:
                unit = config.room_users[message.room][username]
                logger.debug('send message: ' + str(message.to_dict()))
                # logger.debug(message.username + '->' + unit.username + ': [%s]' % message.type_ + message.content)
                await unit.ws.send(utils.dump(utils.make_message(message)))
        else:
            # 属于私聊
            target = message.direction
            # 是否在房间中
            in_room = False
            target_unit = None
            if target not in config.room_users[message.room]:
                raise ChatinoException.UsernameNotFound('Username %s Not Found!' % target)
            target_unit = config.online_users[target]
            await target_unit.ws.send(utils.dump(utils.make_message(message)))

    def run(self):
        logger.info('Chatino running on ws://%s:%s...' % (config.WS_BIND, config.WS_PORT))
        asyncio.get_event_loop().run_until_complete(self.myws)
        asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    _c = Chatino()
    _c.run()
