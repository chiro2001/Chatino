# from Chatino.chatino import Chatino
# from Chatino.config import logger
from Chatino import utils
from Chatino.config import ChatinoException, Unit
import websockets


async def join(chatino=None, unit: Unit = None, ws: websockets.server.WebSocketServerProtocol = None,
               args: dict = None, cmd: str = None, logger=None) -> dict:
    logger.info('Command Join started!')
    logger.info('cmd:' + cmd)
    logger.info('args:' + str(args))
    room = args['room']
    try:
        await chatino.join_room(unit.username, room)
    except ChatinoException.BaseException as e:
        return utils.make_result(1, message=str(e))
    return utils.make_result(0)
