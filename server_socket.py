# -*- coding:utf-8- -*-
"""
作者：苦瓜
日期：2022年03月23日
"""
import socket
from config import *

class ServerSoket(socket.socket):
    """定义socket，初始化服务器socket需要的参数"""
    def __init__(self):
        # 设置TCP类型， 创建套接字
        super(ServerSoket, self).__init__(socket.AF_INET, socket.SOCK_STREAM)

        # 绑定端口号和地址
        self.bind((SERVER_IP, SERVER_PORT))

        # 设置监听模式
        self.listen(16)
