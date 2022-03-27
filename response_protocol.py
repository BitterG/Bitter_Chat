# -*- coding:utf-8- -*-
"""
作者：苦瓜
日期：2022年03月23日
"""
from config import *

class ResponseProtocol(object):
    """服务器响应格式化字符串"""

    @staticmethod
    def response_login_result(result, nickname, username):
        """
        生成用户登录请求的结果
        :param result: 成功登录返回1 登陆失败返回0
        :param nickname: 登录用户的名称 登录失败返回空
        :param username: 登录用户的账号 登录失败返回空
        :return: 返回给用户格式化信息
        """
        return DELIMITER.join([RESPONSE_LOGIN_RESULT, result, nickname, username])

    @staticmethod
    def response_chat(nickname, messages):
        """
        生成返回给用户的消息字符串
        :param nickname: 发送消息的用户账号
        :param messages: 发送消息的用户名称
        :return: 返回字符串消息给用户
        """
        return DELIMITER.join([RESPONSE_CHAT, nickname, messages])
