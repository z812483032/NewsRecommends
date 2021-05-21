
'''
    Author: Zeng
    Desc：
        代码11-3 每个类型下新闻的相似度计算
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
log_file_handler = TimedRotatingFileHandler(filename="Recommend/analysis/ccg.log",
                                            when="S", interval=5,
                                            backupCount=20)
log_file_handler.setFormatter(formatter)

# 3. 向logger对象中添加handler
logger.addHandler(log_file_handler)


class Correlation:
    def __init__(self, file):
        # self.db = self.connection()
        # self.cursor = self.db.cursor()

        self.file = file
        self.news_tags = self.loadData()
        self.news_cor_list = self.getCorrelation()

    # 连接mysql数据库
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

    # 加载数据
    def loadData(self):
        '''
            @Description：加载关键词分析结果文件
            @:param None
        '''
        # print("开始加载文件数据：%s" % self.file)
        news_tags = dict()
        for line in open(self.file, "r", encoding="utf-8").readlines():
            try:
                newid, newtags = line.strip().split("\t")
                news_tags[newid] = newtags
            except:
                print("读取分词数据过程中出现错误，错误行为：{}".format(line))
                logger.error("Error：{}".format(line))
                pass
        return news_tags

    def getCorrelation(self):
        '''
            @Description：计算相关度
            @:param None
        '''
        news_cor_list = list()
        for newid1 in self.news_tags.keys():
            id1_tags = set(self.news_tags[newid1].split(","))
            for newid2 in self.news_tags.keys():
                id2_tags = set(self.news_tags[newid2].split(","))
                if newid1 != newid2:
                    # print(newid1 + "\t" + newid2 + "\t" + str(id1_tags & id2_tags))
                    cor = (len(id1_tags & id2_tags)) / len(id1_tags | id2_tags)
                    if cor > 0.0:
                        news_cor_list.append([newid1, newid2, format(cor, ".2f")])
                        logger.info("news_cor_list.append：{}".format([newid1, newid2, format(cor, ".2f")]))
        return news_cor_list

    def writeToMySQL(self):
        '''
            @Description：将相似度数据写入数据库
            @:param None
        '''
        db = pymysql.Connect(host=DB_HOST, user=DB_USER, password=DB_PASSWD, database=DB_NAME, port=DB_PORT,
                             charset='utf8')
        for row in self.news_cor_list:
            sql_w = "insert into news_api_newssimilar( new_id_base,new_id_sim,new_correlation ) values(%s, %s ,%s)" % (
                row[0], row[1], row[2])
            try:
                cur = db.cursor()
                cur.execute(sql_w)
                db.commit()
            except:
                print("rollback", row)
                logger.error("rollback：{}".format(row))
        print("相似度数据写入数据库：newsrec.newsim")


def beginCorrelation():
    '''
        @Description：启动相似度分析
        @:param None
    '''
    original_data_path = "Recommend/data/keywords/"
    files = os.listdir(original_data_path)
    for file in files:
        # print("开始计算文件 %s 下的新闻相关度。" % file)
        cor = Correlation(original_data_path + file)
        cor.writeToMySQL()
    # print("\n相关度计算完毕，数据写入路径 z-othersd/data/correlation")
