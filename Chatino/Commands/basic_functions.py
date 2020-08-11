from Chatino import utils
from Chatino.config import *
import websockets
import time


async def chat(chatino=None, unit: Unit = None, ws: websockets.server.WebSocketServerProtocol = None,
               args: dict = None, cmd: str = None) -> dict:
    logger.debug('Command Chat started!')
    logger.debug('cmd:' + cmd)
    logger.debug('args:' + str(args))
    room = args['room']
    text = args['text']

    message: Message = Message(room, unit.username, text, time.time(),
                               type_=args.get('type', MessageType.text),
                               # visibility=args.get('visibility', Visibility.public),
                               # status=args.get('status', Status.available),
                               # direction=args.get('direction', Direction.public)
                               )
    try:
        await chatino.push_message(message)
    except ChatinoException.BaseException as e:
        return utils.make_result(1, message=str(e))
    return utils.make_result(0)


async def join(chatino=None, unit: Unit = None, ws: websockets.server.WebSocketServerProtocol = None,
               args: dict = None, cmd: str = None) -> dict:
    logger.debug('Command Join started!')
    logger.debug('cmd:' + cmd)
    logger.debug('args:' + str(args))
    room = args['room']
    try:
        await chatino.join_room(unit.username, room)
    except ChatinoException.BaseException as e:
        return utils.make_result(1, message=str(e))
    return utils.make_result(0)


async def exit_(chatino=None, unit: Unit = None, ws: websockets.server.WebSocketServerProtocol = None,
                args: dict = None, cmd: str = None) -> dict:
    logger.debug('Command Exit started!')
    logger.debug('cmd:' + cmd)
    logger.debug('args:' + str(args))
    room = args['room']
    try:
        await chatino.exit_room(unit.username, room)
    except ChatinoException.BaseException as e:
        return utils.make_result(1, message=str(e))
    return utils.make_result(0)


async def whisper(chatino=None, unit: Unit = None, ws: websockets.server.WebSocketServerProtocol = None,
                  args: dict = None, cmd: str = None) -> dict:
    logger.debug('Command Whisper started!')
    logger.debug('cmd:' + cmd)
    logger.debug('args:' + str(args))
    room = args['room']
    text = args['text']
    target = args['target']

    # 注意这些可选参数
    message: Message = Message(room, unit.username, text, time.time(),
                               type_=args.get('type', MessageType.text),
                               # visibility=args.get('visibility', Visibility.public),
                               # status=args.get('status', Status.available),
                               direction=target
                               )
    try:
        await chatino.push_message(message)
    except ChatinoException.BaseException as e:
        return utils.make_result(1, message=str(e))
    return utils.make_result(0)
