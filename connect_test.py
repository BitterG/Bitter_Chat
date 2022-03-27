# -*- coding:utf-8- -*-
"""
作者：苦瓜
日期：2022年03月24日
"""
import socket

def connect_test():
    # 测试连接
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 8888))

    while True:
        msg = input("请输入内容>>>")
        if msg == 'exit':
            break
        client_socket.send(msg.encode('utf-8'))
        recv_data = client_socket.recv(512)
        print(recv_data.decode('utf-8'))
    client_socket.close()

if __name__ == '__main__':
    connect_test()
