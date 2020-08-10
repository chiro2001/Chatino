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
        await self.ws_start(ws)
        # 然后开始处理命令
        await self.parser(ws)

    async def ws_start(self, ws):
        while True:
            try:
                raw = await ws.recv()
                # print('raw', raw)
                data = json.loads(raw)
            except Exception as e:
                print('except:', utils.make_error_result(e))
                # 还是有可能发送失败
                try:
                    await ws.send(utils.dump(utils.make_error_result(e)))
                except (websockets.exceptions.ConnectionClosedError, websockets.exceptions.ConnectionClosedError) as e2:
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
            if 'username' in args and 'password' not in args:
                # 匿名模式
                # 先创建token
                username = args['username']
                token = self.db.token_create(username)
            if 'username' in args and 'password' in args:
                # 登录模式
                # 登录校验
                username, password = args['username'], args['password']
                if not self.db.user_verify(username, password=password):
                    # 登录失败
                    await ws.send(utils.dump(utils.make_result(3)))
                    continue
                result = self.db.token_create(username)
                token = result['token']
            if 'token' in args:
                token = args['token']

            username = self.db.token_to_username(token)
            user = None
            try:
                user = self.db.user_find(username)
            except ChatinoException.UsernameNotFound:
                pass
            # for i in user:
            #     unit['user'][i] = user[i]
            # unit = self.unit_create(username, token, ws, user=user)
            unit = config.Unit(username, token, ws, user=user)

            # 最后加入online_users
            # global config.online_users
            config.online_users[username] = unit
            # 返回成功的值
            await ws.send(utils.dump(utils.make_result(0, data=unit.to_dict())))
            break

    async def parser(self, ws):
        while True:
            # 还是有可能接收失败
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
            commands.commands_table[cmd]['function'](chatino=self, ws=ws, cmd=cmd, args=args, logger=logger)

    def push_message(self, message: config.Message):
        if message.room not in config.room_users:
            raise ChatinoException.RoomNotFound("Room %s Not Found!" % message.room)
        # TODO: 修复public用户收不到私聊的问题
        if message.direction == config.Direction.public:
            for unit in config.room_users[message.room]:
                logger.debug(message.username + '->' + unit.username + ': [%s]' % message.type_ + message.content)
                await unit.ws.send(utils.dump(utils.make_message(message)))
        else:
            # 属于私聊
            target = message.direction
            in_room = False
            for i in config.room_users[message.room]:
                if i.username == target:
                    in_room = True
                    break
            if not in_room:
                raise ChatinoException.UsernameNotFound('Username %s Not Found!' % target)


    def run(self):
        logger.info('Chatino running on ws://%s:%s...' % (config.WS_BIND, config.WS_PORT))
        asyncio.get_event_loop().run_until_complete(self.myws)
        asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    _c = Chatino()
    _c.run()
