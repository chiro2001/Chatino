"""
Description: TCP类管理模块。
"""
from flask import *


app = Flask(__name__)


if __name__ == '__main__':
    app.run('0.0.0.0', port=80, debug=False)
