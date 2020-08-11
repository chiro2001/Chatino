import json
import os
import time
import requests
from ws4py.client.threadedclient import WebSocketClient
from base_logger import get_logger

target = 'ws://localhost:10086/'
logger = get_logger(__name__)


class MyClient(WebSocketClient):
    def opened(self):
        pass

    def closed(self, code, reason=None):
        pass

    def received_message(self, resp):
        logger.info(str(resp))


def main():
    ws = MyClient(target)
    ws.connect()
    time.sleep(0.1)
    time.sleep(0.1)
    ws.close()
    time.sleep(0.1)


def test_chat():
    ws = MyClient(target)
    ws.connect()
    time.sleep(0.5)
    ws.send(json.dumps({
        'cmd': 'start',
        'args': {
            'username': 'lance',
        }
    }))
    time.sleep(0.5)
    ws.send(json.dumps({
        'cmd': 'join',
        'args': {
            'room': 'my_room',
        }
    }))
    while True:
        time.sleep(0.5)
    # ws.close()


if __name__ == '__main__':
    # main()
    test_chat()
