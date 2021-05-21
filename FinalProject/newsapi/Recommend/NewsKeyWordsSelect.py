# -*- coding: utf-8 -*-
'''
    Author: x
    Desc：
        代码11-2 不同语料库下的新闻关键词抽取-基于TFIDF
'''
import logging
from logging.handlers import TimedRotatingFileHandler

import pymysql
import jieba.analyse

from Spider.settings import DB_HOST, DB_USER, DB_PASSWD, DB_NAME, DB_PORT

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)-7s - %(message)s')

# 2. 初始化handler,并配置formater
log_file_handler = TimedRotatingFileHandler(filename="Recommend/analysis/kwg.log",
                                            when="S", interval=5,
                                            backupCount=20)
log_file_handler.setFormatter(formatter)

# 3. 向logger对象中添加handler
logger.addHandler(log_file_handler)


class SelectKeyWord:
    def __init__(self, _type):
        self._type = _type
        self.db = self.connection()
        self.cursor = self.db.cursor()
        self.news_dict = self.loadData()
        self.key_words = self.getKeyWords()

    def connection(self):
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

    def loadData(self):
        '''
            @Description：加载数据
            @:param None
        '''
        news_dict = dict()
        table = self.getDataFromDB()
        # 遍历每一行
        # for row in range(1, table.nrows):
        for row in range(len(table)):
            line = table[row]
            news_id = int(line[0])
            news_dict.setdefault(news_id, {})
            news_dict[news_id]["tag"] = line[0]
            news_dict[news_id]["title"] = line[2]
            news_dict[news_id]["content"] = line[6]
        return news_dict

    def getDataFromDB(self):
        '''
            @Description：从数据库获取数据
            @:param None
        '''
        logger.info("从数据库获取数据")
        sql_s = "select * from news_api_newsdetail"
        try:
            self.cursor.execute(sql_s)
            message = self.cursor.fetchall()
        except:
            self.db.rollback()
        return message

    # 调用结巴分词获取每篇文章的关键词
    def getKeyWords(self):
        '''
            @Description：通过jieba提取关键词TF-IDF算法
            @:param _type --> 选择提取内容（标题提取、标题+内容提取）
        '''
        news_key_words = list()
        # 加载停用词表

        stop_words_list = [line.strip() for line in open("Recommend/stopwords/stop_words.txt", 'r').readlines()]
        for new_id in self.news_dict.keys():
            if self._type == 1:
                # allowPOS 提取地名、名词、动名词、动词
                keywords = jieba.analyse.extract_tags(
                    self.news_dict[new_id]["title"] + self.news_dict[new_id]["content"],
                    topK=10,
                    withWeight=False,
                    allowPOS=('ns', 'n', 'vn', 'rn', 'nz')
                )
                news_key_words.append(str(new_id) + '\t' + ",".join(keywords))
                sql_i = 'update news_api_newsdetail set keywords=\"%s\" where news_id=%d' % (",".join(kws), new_id)
                try:
                    self.cursor.execute(sql_i)
                    self.db.commit()
                except Exception:
                    logger.error("Error:KeyWords update Error!!")
                    self.db.rollback()
            elif self._type == 2:
                # cut_all :False 表示精确模式
                # keywords = jieba.cut(self.news_dict[new_id]["content"], cut_all=False)
                keywords = jieba.analyse.extract_tags(
                    self.news_dict[new_id]["title"] + self.news_dict[new_id]["content"],
                    topK=10,
                    withWeight=False,
                    allowPOS=('ns', 'n', 'vn', 'rn', 'nz')
                )
                kws = list()
                for kw in keywords:
                    if kw not in stop_words_list and kw != " " and kw != " ":
                        kws.append(kw)
                        logger.info("keyword:{}".format(kw))
                news_key_words.append(str(new_id) + '\t' + ",".join(kws))
                sql_i = 'update news_api_newsdetail set keywords=\"%s\" where news_id=%d' % (",".join(kws), new_id)
                try:
                    self.cursor.execute(sql_i)
                    self.db.commit()
                except Exception:
                    logger.error("Error:KeyWords update Error!!")
                    self.db.rollback()
            else:
                logger.error("请指定获取关键词的方法类型<1：TF-IDF 2：标题分词法>")
        return news_key_words

    def writeToFile(self):
        '''
            @Description：将关键词获取结果写入文件
            @:param None
        '''
        fw = open("Recommend/data/keywords/1.txt", "w", encoding="utf-8")
        fw.write("\n".join(self.key_words))
        fw.close()


def splitTxt():
    source_dir = 'Recommend/data/keywords/1.txt'
    target_dir = 'Recommend/data/keywords/split/'

    # 计数器
    flag = 0

    # 文件名
    name = 1

    # 存放数据
    dataList = []


    with open(source_dir, 'rb') as f_source:
        for line in f_source:
            flag += 1
            dataList.append(line)
            if flag == 200:
                with open(target_dir + "pass_" + str(name) + ".txt", 'wb+') as f_target:
                    for data in dataList:
                        f_target.write(data)
                name += 1
                flag = 0
                dataList = []

    # 处理最后一批行数少于200万行的
    with open(target_dir + "pass_" + str(name) + ".txt", 'wb+') as f_target:
        for data in dataList:
            f_target.write(data)


def beginSelectKeyWord(_type):
    skw = SelectKeyWord(_type=_type)
    skw.writeToFile()
    # print("\n关键词获取完毕，数据写入路径 Recommend/data/keywords")
    logger.info("关键词获取完毕，数据写入路径 Recommend/data/keywords")
