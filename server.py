# -*- coding:utf-8- -*-
"""
作者：苦瓜
日期：2022年03月24日
"""
from server_socket import ServerSoket
from socket_wrapper import SocketWrapper
from threading import Thread
from config import *
from response_protocol import *
from db import Db

class Server(object):
    """服务器核心"""

    def __init__(self):
        # 创建服务器套接字
        self.server_socket = ServerSoket()

        # 创建请求的id和方法关联字典 用于请求类型调用函数作出处理
        self.request_handle_function = {}
        self.register(REQUEST_LOGIN, self.request_login_handle)
        self.register(REQUEST_CHAT, self.request_chat_handle)

        # 创建保存当前用户登录的信息变量字典
        self.clients = {}

        # 创建数据库管理对象
        self.db = Db()

    def register(self, request_id, handle_function):
        """注册消息类型和处理函数到字典"""
        self.request_handle_function[request_id] = handle_function

    def startup(self):
        """获取链接"""
        while True:
            # 获取链接
            print('等待客户端连接！')
            soc, addr = self.server_socket.accept()
            print('已获取客户端连接！')

            # 使用套接字封装对象
            client_soc = SocketWrapper(soc)

            # 收发消息
            t = Thread(target=self.request_handle, args=(client_soc,))
            t.start()

            # # 关闭客户端套接字
            # soc.close()

    def request_handle(self, client_soc):
        """处理客户端请求"""
        while True:
            # 接收客户端数据
            recv_data = client_soc.recv_data()
            if not recv_data:
                """没有接收到客户端信息关闭"""
                self.remove_offline_user(client_soc)
                client_soc.close()
                break

            # 数据解析处理
            parse_data = self.parse_request_text(recv_data)

            # if parse_data['request_id'] == REQUEST_LOGIN:
            #     self.request_login_handle()
            # elif parse_data['request_id'] == REQUEST_CHAT:
            #     self.request_chat_handle()

            # 分析请求类型，并根据请求类型调用响应处理函数
            handle_function = self.request_handle_function.get(parse_data['request_id'])

            if handle_function:
                handle_function(client_soc, parse_data)

    def remove_offline_user(self, client_soc):
        """客户端下线处理"""
        print("有客户端下线")
        for username, info in self.clients.items():
            if info['sock'] == client_soc:
                # print(self.clients)
                del self.clients[username]
                # print(self.clients)
                break

    def parse_request_text(self, text):
        """
        解析客户端发送的数据
        登录信息：0001|username|password
        聊天信息：0002|username|message
        """
        print("解析客户端数据:" + text)
        request_list = text.split(DELIMITER)
        # 按照类型解析数据

        request_data = {}   # 保存分隔符分割的信息字典

        request_data['request_id'] = request_list[0]    # 用户请求类型

        if request_data['request_id'] == REQUEST_LOGIN:     # 0001登录请求
            # 用户请求登录
            request_data['username'] = request_list[1]      # 保存用户输入名称
            request_data['password'] = request_list[2]      # 保存用户输入密码

        elif request_data['request_id'] == REQUEST_CHAT:    # 0002聊天请求
            # 用户请求聊天
            request_data['username'] = request_list[1]      # 保存发送消息用户名
            request_data['message'] = request_list[2]       # 报讯发送消息的，消息内容

        return request_data

    def request_login_handle(self, client_soc, request_data):
        """处理登录请求"""
        print("收到登录请求-准备处理")
        # 获取账号密码
        username = request_data['username']
        password = request_data['password']

        # 检查是否能够登录
        ret, nickname, username = self.check_user_login(username, password)
        # 登录成功保存用户和密码
        if ret == '1':
            self.clients[username] = {'sock':client_soc, 'nickname':nickname}

        # 返回客户端消息
        response_text = ResponseProtocol.response_login_result(ret, nickname, username)

        # 把消息发送给客户端
        client_soc.send_data(response_text)

    def request_chat_handle(self, client_soc, request_data):
        """处理聊天功能"""
        print("收到聊天请求-准备处理", request_data)
        # 获取消息内容
        username = request_data['username']
        messages = request_data['message']
        nickname = self.clients[username]['nickname']

        # 拼接发送给客户端的文本消息
        msg = ResponseProtocol.response_chat(nickname, messages)

        # 转发消息至用户
        for u_name, info in self.clients.items():
            if username == u_name:  # 发消息的用户不需要服务武器返回消息
                continue
            info['sock'].send_data(msg)

    def check_user_login(self, username, password):
        """
        检查用户是否登录成功-用户-密码是否匹配（数据库）
        返回值ret 0失败 1成功
        """
        # 从数据库查询用户信息
        sql = "select * from users where user_name='%s'" % username
        result = self.db.get_user(sql)

        # 没有查询结果则用户不存在，登录失败
        if not result:
            return '0', '', username

        # 若密码不匹配，则说明密码错误，登陆失败
        if password != result['user_password']:
            return '0', '', username

        # 登录成功
        return '1', result['user_nickname'], username

if __name__ == '__main__':
    Server().startup()
