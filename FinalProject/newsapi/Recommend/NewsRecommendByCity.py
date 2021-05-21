# -*- coding: utf-8 -*-
'''
@FileName：NewsRecommendByCity.py
@Description：通过ip获取到用户登录的所在区域，并通过区域进行内容匹配，然后给用户进行新闻推荐
@Author：Zline
@Time：2021/3/21 9:11
@Copyright：©2019-2021 Zline
'''
import datetime
import logging
import os
import re
from logging.handlers import TimedRotatingFileHandler

import pymysql
import requests

from Spider.settings import DB_HOST, DB_USER, DB_PASSWD, DB_NAME, DB_PORT


logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)-7s - %(message)s')

# 2. 初始化handler,并配置formater
log_file_handler = TimedRotatingFileHandler(filename="Recommend/recommend/clg.log",
                                            when="S", interval=10,
                                            backupCount=20)
log_file_handler.setFormatter(formatter)

# 3. 向logger对象中添加handler
logger.addHandler(log_file_handler)

# http://ip.ws.126.net/ipquery?ip=223.104.63.12
class NewsRecommendByCity():
    def __init__(self):
        self.file = self.getFile()
        self.db = self.connect()
        self.cursor = self.db.cursor()
        # self.userid = userid
        self.userslist = self.getUserData()
        self.news_tags = self.loadFileData()
        self.region = self.getRegion()
        self.reco = self.getRecommendByCity()
        self.result = self.writeToMySQL()

    # 连接mysql数据库
    def connect(self):
        db = pymysql.Connect(host=DB_HOST, user=DB_USER, password=DB_PASSWD, database=DB_NAME, port=DB_PORT,
                             charset='utf8')
        return db

    def getRecommendByCity(self):
        '''
            @Description：通过地区匹配新闻内容
            @:param region ----> 地区
        '''
        city_cor_list = list()
        for user in self.userslist:
            userid = user[0]
            # print('region', self.region)
            logger.info("region：{}".format(self.region))
            # print('user', user)
            city_key = {dict(self.region).get(userid)}
            # print(city_key)
            for newsid in self.news_tags:
                newstags = set(self.news_tags[newsid].split(","))
                # print(city_key,newstags)
                if len(city_key & newstags) > 0:
                    city_cor_list.append([int(userid), int(newsid), 1])
                    logger.info("city_cor_list.append：{}".format(str(userid)+":"+str(newsid)))
        return city_cor_list

    def getRegion(self):
        '''
            @Description：通过ip获取用户所在地区
            @:param  ip ----> 用户登录ip
        '''
        poslist = dict()
        for user in self.userslist:
            # print(user)
            # print(user[0])
            userid = user[0]
            ip = user[1]
            url = 'http://ip.ws.126.net/ipquery?ip=' + str(ip)
            res = requests.get(url)
            pos = re.findall('lo="(.*?)"', res.text)
            poslist[userid] = list(pos)[0]
        return poslist

    def getUserData(self):
        '''
            @Description：通过数据库获取用户的ip
            @:param
        '''
        users = ''
        sql_s = 'select userid,ip from news_api_user '
        try:
            self.cursor.execute(sql_s)
            users = self.cursor.fetchall()
            print(users)
        except Exception:
            print("Demo Error")
        return users

    def getFile(self):
        '''
           @Description：获取新闻对象
           @:param
        '''
        original_data_path = "Recommend/data/keywords/"
        files = os.listdir(original_data_path)
        for file in files:
            return original_data_path + file

    def loadFileData(self):
        '''
            @Description：加载本地的新闻标签词库
            @:param
        '''
        print("开始加载文件数据：%s" % self.file)
        news_tags = dict()
        for line in open(self.file, "r", encoding="utf-8").readlines():
            try:
                newid, newtags = line.strip().split("\t")
                news_tags[newid] = newtags
            except:
                print("读取分词数据过程中出现错误，错误行为：{}".format(line))
                pass
        return news_tags

    def writeToMySQL(self):
        logging.info("将数据写入数据库...")
        print(self.reco)
        time = datetime.datetime.now().strftime("%Y-%m-%d")
        print(time)
        for user in self.userslist:
            userid = user[0]
            sql_u_region = "update news_api_user set region='%s' where userid=%d" % (dict(self.region).get(userid).replace("省", ""), userid)
            try:
                self.cursor.execute(sql_u_region)
                self.db.commit()
            except Exception:
                logger.error("rollback:{}".format(userid))
                self.db.rollback()
        for row in self.reco:
            sql_i = 'insert into news_api_recommend(userid, newsid, hadread, cor, species ,time) values (%d, %d, 0, %.2f, 1, \'%s\')' % \
                    (int(row[0]), int(row[1]), float(row[2]), time)
            print(sql_i)
            try:
                self.cursor.execute(sql_i)
                self.db.commit()
            except Exception:
                logger.error("rollback:{}".format(row))
                # print("rollback", row)
                self.db.rollback()
        logger.info("推荐内容数据写入完成....")
        print('结束')
        return 1


def beginrecommendbycity():
    NewsRecommendByCity()
