# -- coding: utf-8 --
import pymysql, logging

from newsapi.Spider.settings import DB_HOST, DB_USER, DB_PASSWD, DB_NAME, DB_PORT


class TextTool:
    def __init__(self):
        self.db = self.connection()
        self.cursor = self.db.cursor()

    def connection(self):
        db = pymysql.Connect(host=DB_HOST, user=DB_USER, password=DB_PASSWD, database=DB_NAME, port=DB_PORT,
                             charset='utf8')
        return db

    def loadData(self):
        logging.info("开始加载数据库数据：")
        sql_s = "select url,mainpage from news_api_newsdetail"
        try:
            self.cursor.execute(sql_s)
            message = self.cursor.fetchall()
        except:
            logging.error("Database Error")
            self.db.rollback()
        return message

    def writeData(self):
        logging.info("开始数据写入：")

    def dataProcess(self, message):
        handletext = {}
        for numbers in range(len(message)):
            temp = eval(str(message[numbers][1]))
            text_all = ""
            for text in temp:
                print(text)
                text_all += text
            # message[numbers][1] = text_all
            handletext[message[numbers][0]] = text_all
        return handletext


if __name__ == '__main__':
    cor = TextTool()
    text = cor.loadData()
    handletext = cor.dataProcess(message=text)
    print(handletext)
