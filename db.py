# -*- coding:utf-8- -*-
"""
作者：苦瓜
日期：2022年03月26日
"""
from pymysql import connect

class Db(object):

    def __init__(self):
        self.connection = connect(host='localhost', port=3306, user='root', password='123456', db='bitter_chat',
                                     charset='utf8')
        self.cursor = self.connection.cursor()

    def close(self):
        # 关闭Cursor对象
        self.cursor.close()
        self.connection.close()

    def get_user(self, sql):
        """执行sql语句查询"""

        self.cursor.execute(sql)

        get_result = self.cursor.fetchone()

        if not get_result:
            return None

        fileds = [filed[0] for filed in self.cursor.description]

        return_data = {}
        for filed, value in zip(fileds, get_result):
            return_data[filed] = value
        return return_data

if __name__ == '__main__':
    db = Db()
    data = db.get_user("select * from users where user_name='Bitter_Gourd'")
    print(data)
    db.close()
