# -*- coding: utf-8 -*-
'''
    Author:Z
    Desc：通过热值对用户进行推送新闻
'''
import datetime
import logging
from logging.handlers import TimedRotatingFileHandler

import pymysql

from Spider.settings import DB_HOST, DB_USER, DB_PASSWD, DB_NAME, DB_PORT

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)-7s - %(message)s')

# 2. 初始化handler,并配置formater
log_file_handler = TimedRotatingFileHandler(filename="Recommend/recommend/hlg.log",
                                            when="S", interval=10,
                                            backupCount=20)
log_file_handler.setFormatter(formatter)

# 3. 向logger对象中添加handler
logger.addHandler(log_file_handler)

class NewsRecommendByHotValue():
    def __init__(self):
        self.db = self.connect()
        self.cursor = self.db.cursor()
        self.userlist = self.loadDBData()
        # self.news_tags = self.loadFileData()
        self.result = self.getRecResult()

    def connect(self):
        '''
            @Description：数据库连接
            @:param host --> 数据库链接
            @:param user --> 用户名
            @:param password --> 密码
            @:param database --> 数据库名
            @:param port --> 端口号
            @:param charset --> 编码
        '''
        db = pymysql.Connect(host=DB_HOST, user=DB_USER, password=DB_PASSWD, database=DB_NAME, port=DB_PORT,
                             charset='utf8')
        return db

    def loadDBData(self):
        '''
            @Description：加载数据库用户数据
            @:param None
        '''
        sql_s = 'select userid from news_api_user'
        try:
            self.cursor.execute(sql_s)
            useridlist = self.cursor.fetchall()
        except:
            logging.error("Database Error")
            self.db.rollback()
        return useridlist

    def getRecResult(self):
        '''
            @Description：加载数据库新闻热度数据并进行热度推荐
            @:param None
        '''
        sql_s = 'select news_id,news_hot from news_api_newshot order by news_hot DESC limit 0,20;'
        self.cursor.execute(sql_s)
        newsidlist = self.cursor.fetchall()
        print(newsidlist)
        time = datetime.datetime.now().strftime("%Y-%m-%d")
        for user in self.userlist:
            print(user[0])
            for newsid in newsidlist:
                sql_w = 'insert into news_api_recommend(userid, newsid, hadread, cor, species, time) values (%d, %d, 0, %.2f, 2, \'%s\')' % \
                    (int(user[0]), int(newsid[0]), 1, time)
                logger.info("sql_w：{}".format(sql_w))
                try:
                    self.cursor.execute(sql_w)
                    self.db.commit()
                except:
                    logger.error("rollback：{}".format(newsid[0]))
                    self.db.rollback()
        return True

def beginrecommendbyhotvalue():
    NewsRecommendByHotValue()