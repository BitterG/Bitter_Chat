# -*- coding:utf-8- -*-
"""
作者：苦瓜
日期：2022年03月27日
"""
import threading
from threading import Thread
import tkinter as tk
from socket import *
import tkinter.messagebox   # 弹窗
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from pymysql import connect

class Client(object):

    def __init__(self):
        self.IP = '127.0.0.1'
        self.SERVER_PORT = 8888
        self.BUFLEN = 512

        # 实例化一个socket对象，指明协议
        self.dataSocket = socket(AF_INET, SOCK_STREAM)

        # 连接服务端socket
        self.dataSocket.connect((self.IP, self.SERVER_PORT))

        t1 = threading.Thread(target=self.input_inf, args=(self.dataSocket,))
        t1.start()
        t2 = threading.Thread(target=self.recv_inf, args=(self.dataSocket,))
        t2.start()
        t3 = threading.Thread(target=self.recv_inf_send, args=(self.dataSocket,))
        t3.start()


    def startup(self):
        self.window = tk.Tk()
        self.window.title('欢迎')
        self.window.geometry('512x336')


        # 图片封面
        canvas = tk.Canvas(self.window, height=500, width=900)
        image_file = tk.PhotoImage(file='fm_rem.gif')
        image = canvas.create_image(0, 0, anchor='nw', image=image_file)
        canvas.pack()
        self.window.resizable(False, False)

        tk.Label(self.window, text='用户名:').place(x=140, y=180)
        tk.Label(self.window, text='密码:').place(x=140, y=230)

        self.var_usr_name = tk.StringVar()
        self.var_usr_name.set('请输入账号')
        entry_usr_name = tk.Entry(self.window, textvariable=self.var_usr_name)
        entry_usr_name.place(x=200, y=180)

        self.var_usr_pwd = tk.StringVar()
        entry_usr_pwd = tk.Entry(self.window, textvariable=self.var_usr_pwd, show='*')
        entry_usr_pwd.place(x=200, y=230)

        button_login = Button(self.window, text='登录', command=self.on_log_button)
        button_login.place(x=180, y=280)
        button_register = Button(self.window, text='注册', command=self.on_reg_button)
        button_register.place(x=280, y=280)

        self.window_chat = Toplevel()
        Label(self.window_chat, text='hello')

        self.window_chat.geometry('%dx%d' % (795, 505))
        self.window_chat.resizable(False, False)


        self.scroll = ScrolledText(self.window_chat)
        self.scroll['width'] = 96
        self.scroll['height'] = 25
        self.scroll.place(x=0, y=0)

        self.scroll.tag_config('green', foreground='#008B00')

        self.usr_input = tk.StringVar()
        chat_input_area = tk.Entry(self.window_chat, textvariable=self.usr_input, name='chat_input_area', width=50)
        chat_input_area.place(x=10, y=410)

        send_button = Button(self.window_chat, text='发送', command=self.on_send_button)
        send_button['width'] = 5
        send_button['height'] = 2
        send_button.place(x=720, y=420)

        self.window_chat.withdraw()  # 隐藏聊天窗口

        self.window_chat.mainloop()

        self.window.mainloop()


    def on_send_button(self):
        # print(username)
        username = self.var_usr_name.get()
        chat_input_area = self.usr_input.get()
        toSend = '0002' + "|" + username + "|" + chat_input_area
        print(toSend)
        self.dataSocket.send(toSend.encode('utf-8'))
        self.scroll.insert(tkinter.END, self.response_data['uname'] + '：' + '\n', 'green')
        self.scroll.insert(tkinter.END, '\t' + self.usr_input.get() + '\n')
        self.usr_input.set('')  # 发送消息后清空输入区域


    def input_inf(self, dataSocket):
        # 聊天功能
        while True:
            a = input(">>>")
            dataSocket.send(a.encode('utf-8'))

    def recv_inf_send(self, dataSocket):
        while True:
            t3 = threading.Thread(target=self.recv_inf_send, args=(self.dataSocket,))
            t3.start()
            # 等待接收服务端的消息
            recved = dataSocket.recv(self.BUFLEN)
            # 如果返回空bytes，表示对方关闭了连接
            # 打印读取的信息
            server_recv = recved.decode('utf-8').split('|')
            # print(server_recv.split('|'))
            num = len(server_recv)
            print(num)
            response_data = dict()
            if num == 3:
                """判断为聊天返回消息"""
                print("判断为聊天信息")
                self.response_data['type'] = server_recv[0]
                self.response_data['nickname'] = server_recv[1]
                self.response_data['ser_recv_msg'] = server_recv[2]
                print(self.response_data)
                self.scroll.insert(tkinter.END, self.response_data['nickname'] + '：' + '\n', 'green')
                self.scroll.insert(tkinter.END, '\t' + self.response_data['ser_recv_msg'] + '\n')
            else:
                print("88888888888")

    def on_log_button(self):
        # 点击登录按钮向服务器发送账号密码请求回应
        username = self.var_usr_name.get()
        userpassword = self.var_usr_pwd.get()

        toSend = "0001" + "|" + username + "|" + userpassword
        print(toSend)
        self.dataSocket.send(toSend.encode())

    def on_reg_button(self):
        username = self.var_usr_name.get()
        userpassword = self.var_usr_pwd.get()
        self.connection = connect(host='localhost', port=3306, user='root', password='123456', db='bitter_chat',
                                  charset='utf8')
        self.cursor = self.connection.cursor()
        sql = "select * from users where user_name = '{}';".format(username)
        self.cursor.execute(sql)
        recv_reg_result = self.cursor.fetchone()
        # print(recv_reg_result, 'yyyy')
        self.cursor.close()
        self.connection.close()
        if recv_reg_result:
            tk.messagebox.showinfo('提示', '账号存在请重新注册')
        elif not recv_reg_result:
            self.connection = connect(host='localhost', port=3306, user='root', password='123456', db='bitter_chat',
                                      charset='utf8')
            self.cursor = self.connection.cursor()
            print("执行插入")
            sql = "insert into users values(0, '{}', {}, '{}');".format(username, userpassword, username)
            self.cursor.execute(sql)

            self.connection.commit()

            self.cursor.close()
            self.connection.close()

    def recv_inf(self, dataSocket):
        while True:
            # 等待接收服务端的消息
            recved = dataSocket.recv(self.BUFLEN)
            # 如果返回空bytes，表示对方关闭了连接
            if not recved:
                break
            # 打印读取的信息
            server_recv = recved.decode('utf-8').split('|')
            # print(server_recv.split('|'))
            num = len(server_recv)
            print(num)
            self.response_data = dict()
            if num == 4:
                """判断为登录返回消息"""
                self.response_data['type'] = server_recv[0]
                self.response_data['res'] = server_recv[1]
                self.response_data['uid'] = server_recv[2]
                self.response_data['uname'] = server_recv[3]
                print(self.response_data)
                if self.response_data['res'] == '0':
                    tk.messagebox.showinfo('提示', '账号密码不匹配')
                elif self.response_data['res'] == '1':
                    self.window_chat.update()
                    self.window.withdraw()  # 隐藏登录窗口
                    self.window_chat.deiconify()    # 显示聊天窗口
                    self.window_chat.title('-欢迎{}进入聊天室-'.format(server_recv[3]))    # 更改聊天窗口标题
                else:
                    print("无效")



if __name__ == '__main__':
    Client().startup()