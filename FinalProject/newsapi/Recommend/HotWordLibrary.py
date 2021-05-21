# -- coding: utf-8 --
'''
    Author: Zeng
    Desc：
        3-19 使用分析出的KeyWord进行统计，获取热词
'''
import logging
import os
from logging.handlers import TimedRotatingFileHandler

import pymysql

from Spider.settings import DB_HOST, DB_USER, DB_PASSWD, DB_NAME, DB_PORT

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)-7s - %(message)s')

# 2. 初始化handler,并配置formater
log_file_handler = TimedRotatingFileHandler(filename="Recommend/analysis/hwg.log",
                                            when="S", interval=5,
                                            backupCount=20)
log_file_handler.setFormatter(formatter)

# 3. 向logger对象中添加handler
logger.addHandler(log_file_handler)

class HotWordLibrary():
    def __init__(self, file):
        self.file = file
        self.db = self.connect()
        self.cursor = self.db.cursor()
        self.news_tags = self.loadFileData()
        self.result = self.StatisticalHotKey()
        self.writeresult = self.writeToMySQL()

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
        # db = pymysql.connections.Connection.connect(DB_HOST, DB_USER, DB_PASSWD, DB_NAME, DB_PORT, charset='utf8')
        return db

    def loadFileData(self):
        '''
            @Description：加载关键词分析结果文件
            @:param None
        '''
        logger.info("开始加载文件数据：{}".format(self.file))
        news_tags = dict()
        for line in open(self.file, "r", encoding="utf-8").readlines():
            try:
                newid, newtags = line.strip().split("\t")
                news_tags[newid] = newtags
            except Exception:
                logger.info("读取分词数据过程中出现错误，错误行为：{}".format(line))
                pass
        return news_tags

    def StatisticalHotKey(self):
        '''
            @Description：统计热词
            @:param None
        '''
        hot_word_list = dict()
        for newsid in self.news_tags:
            newstags = set(self.news_tags[newsid].split(","))
            for keyword in newstags:
                if (hot_word_list.get(keyword) != None):
                    hot_word_list.update({keyword: hot_word_list.get(keyword) + 1})
                else:
                    hot_word_list[keyword] = 1
        # print(hot_word_list)
        return hot_word_list

    def writeToMySQL(self):
        '''
            @Description：统计热词结果写入数据库
            @:param None
        '''
        logger.info("将数据写入数据库...")
        sql_t = "truncate table news_api_hotword"
        try:
            self.cursor.execute(sql_t)
            self.db.commit()
        except Exception:
            self.db.rollback()
        for word in self.result:
            if (self.result.get(word) > 1):
                sql_i = 'insert into news_api_hotword(hotword, num) values ("%s", %s)' % (word, self.result.get(word))
                try:
                    self.cursor.execute(sql_i)
                    self.db.commit()
                except Exception:
                    logger.error("rollback:{}".format(word))
                    self.db.rollback()
        logger.info("推荐内容数据写入完成....")
        return 1


def beginHotWordLibrary():
    '''
        @Description：启动热词统计
        @:param None
    '''
    original_data_path = "Recommend/data/keywords/"
    files = os.listdir(original_data_path)
    for file in files:
        # print("开始统计文件 %s 下的热词。" % file)
        cor = HotWordLibrary(original_data_path + file)
        cor.writeToMySQL()
    # print("\n统计热词完毕")
