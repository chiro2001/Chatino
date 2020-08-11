# from Chatino.chatino import Chatino
# from Chatino.config import logger
from Chatino import utils
from Chatino.config import *
import websockets
import time


async def chat(chatino=None, unit: Unit = None, ws: websockets.server.WebSocketServerProtocol = None,
               args: dict = None, cmd: str = None, logger=None) -> dict:
    logger.info('Command Chat started!')
    logger.info('cmd:' + cmd)
    logger.info('args:' + str(args))
    room = args['room']
    text = args['text']

    message: Message = Message(room, unit.username, text, time.time(),
                               type_=args.get('type', MessageType.text),
                               visibility=args.get('visibility', Visibility.public),
                               status=args.get('status', Status.available),
                               direction=args.get('direction', Direction.public))
    try:
         await chatino.push_message(message)
    except ChatinoException.BaseException as e:
        return utils.make_result(1, message=str(e))
    return utils.make_result(0)
