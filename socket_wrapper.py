# -*- coding:utf-8- -*-
"""
作者：苦瓜
日期：2022年03月25日
"""

class SocketWrapper(object):
    """套接字包装类-接收发送"""

    def __init__(self, sock):
        self.sock = sock

    def recv_data(self):
        """接收数据并解码为字符串"""
        try:
            return self.sock.recv(512).decode('utf-8')
        except:
            return ""

    def send_data(self, message):
        return self.sock.send(message.encode('utf-8'))

    def close(self):
        """关闭套接字请求"""
        self.sock.close()
