# from Chatino.chatino import Chatino
# from Chatino.config import logger
from Chatino import utils
import websockets


def chat(chatino=None, ws: websockets.server.WebSocketServerProtocol = None,
         args: dict = None, cmd: str = None, logger=None) -> dict:
    logger.info('Command Chat started!')
    logger.info('cmd:' + cmd)
    logger.info('args:' + str(args))
    return utils.make_result(0)
