# -*- coding: utf-8 -*-
'''
    Author:Z
    Desc：通过用户标签进行内容用户推送分析，并把推送结果导入数据库
'''
import datetime
import logging
import os
from logging.handlers import TimedRotatingFileHandler

import pymysql

from Spider.settings import DB_HOST, DB_USER, DB_PASSWD, DB_NAME, DB_PORT

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)-7s - %(message)s')

# 2. 初始化handler,并配置formater
log_file_handler = TimedRotatingFileHandler(filename="Recommend/recommend/rlg.log",
                                            when="S", interval=10,
                                            backupCount=20)
log_file_handler.setFormatter(formatter)

# 3. 向logger对象中添加handler
logger.addHandler(log_file_handler)

class NewsRecommend:
    def __init__(self, file):
        self.file = file
        self.db = self.connect()
        self.cursor = self.db.cursor()
        self.user_dict = self.loadDBData()
        self.news_tags = self.loadFileData()
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
            @Description：从数据库加载
            @:param None
        '''
        logging.info("从数据库获取数据")
        sql_s = 'select userid,tags from news_api_user'
        try:
            self.cursor.execute(sql_s)
            message = self.cursor.fetchall()
        except:
            logging.error("Database Error")
            self.db.rollback()
        return message


    def loadFileData(self):
        '''
            @Description：从文件中加载分词数据
            @:param None
        '''
        print("开始加载文件数据：%s" % self.file)
        news_tags = dict()
        for line in open(self.file, "r", encoding="utf-8").readlines():
            try:
                newid, newtags = line.strip().split("\t")
                news_tags[newid] = newtags
                logger.info("Loading：{}".format(newtags))
            except:
                logger.info("读取分词数据过程中出现错误，错误行为：{}".format(line))
                pass
        return news_tags

    def getRecResult(self):
        '''
            @Description：获取标签推荐的结果
            @:param None
        '''
        news_cor_list = list()
        # 取出user的标签“user[1]”
        for user in self.user_dict:
            # 取出news的标签self。news_tags[newsid]
            usertags = set(user[1].split(","))
            count = 0
            for newsid in self.news_tags:
                newstags = set(self.news_tags[newsid].split(","))
                cor = (len(usertags & newstags) / len(usertags | newstags))
                if cor > 0.0 and count < 20:
                    count += 1
                    news_cor_list.append([user[0], int(newsid), float(format(cor, ".2f"))])
                    logger.info("news_cor_list:{}".format(news_cor_list))
        return news_cor_list

    def writeToMySQL(self):
        '''
            @Description：将推荐结果写入数据库
            @:param None
        '''
        logging.info("将数据写入数据库...")
        for row in self.result:
            time = datetime.datetime.now().strftime("%Y-%m-%d")
            sql_i = 'insert into news_api_recommend(userid, newsid, hadread, cor, species, time) values (%d, %d, 0, %.2f, 0, \'%s\')'%\
                    (int(row[0]), int(row[1]), float(row[2]), time)
            try:
                self.cursor.execute(sql_i)
                self.db.commit()
            except Exception:
                logger.error("rollback:{}".format(row))
                self.db.rollback()
        logging.info("推荐内容数据写入完成....")



def beginNewsRecommendByTags():
    original_data_path = "Recommend/data/keywords/"
    files = os.listdir(original_data_path)
    for file in files:
        print("开始计算文件 %s 下的新闻相关度。" % file)
        cor = NewsRecommend(original_data_path + file)
        cor.writeToMySQL()
    print("\n相关度计算完毕")