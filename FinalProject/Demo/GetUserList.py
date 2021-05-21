import logging

import pymysql

from newsapi.Spider.settings import DB_HOST, DB_USER, DB_PASSWD, DB_NAME, DB_PORT


class GetUserList:
    def __init__(self):
        self.db = self.connection()
        self.cursor = self.db.cursor()

    def connection(self):
        db = pymysql.Connect(host=DB_HOST, user=DB_USER, password=DB_PASSWD, database=DB_NAME, port=DB_PORT,
                             charset='utf8')
        # db = pymysql.connections.Connection.connect(DB_HOST, DB_USER, DB_PASSWD, DB_NAME, DB_PORT, charset='utf8')
        return db

    def getDataList(self):
        sql = 'select * from user'
        userlist = {}
        try:
            self.cursor.execute(sql)
            userlist = self.cursor.fetchall()
        except Exception:
            logging.error("Demo Error!")
        return userlist

if __name__ == '__main__':
    userlist = GetUserList().getDataList()
    print(userlist)