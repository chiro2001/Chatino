"""
:Description: 这里是解析指令的包，你可以在此增加你自己的命令插件。
              你可以在提供的CommandTester测试插件（建设中）。
:Requests:    你需要在下面的commands_table指定你的命令名称、所需参数和对应函数,
              并且在__all__写上应该被import的包名。
:Providing:   处理函数的参数格式: (chatino=chatino, unit, ws=ws, args={...}, cmd="...")
              应该返回dict格式的result，请使用utils.make_result()。
              利用chatino的逻辑函数和ws的数据接口，你可以建立自己的逻辑函数和插件。
              注意，你只有一次返回数据的机会。每一次执行都是对单个用户的请求的独立线程。
"""

# from Chatino.config import logger
from Chatino.Commands import basic_functions


__all__ = ['basic_functions']


commands_table = {
    # 命令名称
    'chat': {
        # 所需参数
        'args': {
            # 参数1
            'text': {
                # 需要指定参数类型和是否为必须函数
                # 如果类型指定为None，可对应所有类型
                # 如果必须的参数缺少，则不会执行函数
                'type': str,
                'necessary': True,
            }
        },
        # 指向函数
        'function': basic_functions.chat
    },
    'join': {
        'args': {
            'room': {
                'type': str,
                'necessary': True,
            }
        },
        'function': basic_functions.join
    },
    'whisper': {
        'args': {
            'room': {
                'type': str,
                'necessary': True,
            },
            'text': {
                'type': str,
                'necessary': True,
            },
            'target': {
                'type': str,
                'necessary': True,
            }
        },
        'function': basic_functions.whisper
    },
    'exit': {
        'args': {},
        'function': basic_functions.exit_
    },
}
