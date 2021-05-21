import logging

import pymysql

from newsapi.Spider.settings import DB_HOST, DB_USER, DB_PASSWD, DB_NAME, DB_PORT
class GetNewsList:
    def __init__(self, _type):
        self._type = _type
        self.db = self.connection()
        self.cursor = self.db.cursor()

    def connection(self):
        db = pymysql.Connect(host=DB_HOST, user=DB_USER, password=DB_PASSWD, database=DB_NAME, port=DB_PORT,
                             charset='utf8')
        # db = pymysql.connections.Connection.connect(DB_HOST, DB_USER, DB_PASSWD, DB_NAME, DB_PORT, charset='utf8')
        return db

    def getDataList(self):
        sql = 'select * from news_api_newsdetail where category=%s'%self._type
        newslist = {}
        try:
            self.cursor.execute(sql)
            newslist = self.cursor.fetchall()
        except Exception:
            logging.warning("Demo Error!")
        return newslist


if __name__ == '__main__':
    newslist = GetNewsList(_type=1)
    print(newslist.getDataList())
