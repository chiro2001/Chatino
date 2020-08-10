"""
Description: Chatino主逻辑
"""


import json
import asyncio
import websockets
from database import *


class Chatino:
    def __init__(self):
        self.db = ChatinoDB()
        self.myws = websockets.serve(self.ws_main, '0.0.0.0', config.WS_PORT)

    # 这个函数在每一次打开新的连接就会打开
    async def ws_main(self, ws, path):
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
                await ws.send(utils.dump(utils.make_error_result(e)))
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
            if 'username' in args and 'password' not in args:
                # 匿名模式
                pass
            if 'username' in args and 'password' in args:
                # 登录模式
                pass
            if 'token' in args:
                # token访问模式
                pass

    async def parser(self, ws):
        pass

    def run(self):
        print('ws running...')
        asyncio.get_event_loop().run_until_complete(self.myws)
        asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    _c = Chatino()
    _c.run()