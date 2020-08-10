import asyncio
import websockets
import json
from Chatino import utils


async def start(ws):
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
        if not utils.verify(data) or data['cmd'] != 'start' or 'password' not in data['args']:
            # 命令无效
            await ws.send(utils.dump(utils.make_result(3)))
            continue


async def parser(ws):
    while True:
        pass


# 这个函数在每一次打开新的连接就会打开
async def ws_main(ws, path):
    # 必须经过start阶段才能继续
    await start(ws)
    # 然后开始处理命令
    await parser(ws)


def run():
    print('ws running...')
    asyncio.get_event_loop().run_until_complete(myws)
    asyncio.get_event_loop().run_forever()


myws = websockets.serve(ws_main, '0.0.0.0', 10086)
if __name__ == '__main__':
    run()
