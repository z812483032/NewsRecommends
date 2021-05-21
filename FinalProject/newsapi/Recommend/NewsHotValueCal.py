
'''
    Author:Z
    Desc：新闻的热度值计算，并写入数据库
'''
import logging
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

import pymysql

from Spider.settings import DB_HOST, DB_USER, DB_PASSWD, DB_NAME, DB_PORT

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)-7s - %(message)s')

# 2. 初始化handler,并配置formater
log_file_handler = TimedRotatingFileHandler(filename="Recommend/analysis/hvg.log",
                                            when="S", interval=5,
                                            backupCount=20)
log_file_handler.setFormatter(formatter)

# 3. 向logger对象中添加handler
logger.addHandler(log_file_handler)

class CalHotValue:
    def __init__(self):
        self.db = self.connect()
        self.cursor = self.db.cursor()
        self.result = self.calHotValue()

    # 连接mysql数据库
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

    def calHotValue(self):
        '''
            @Description：计算热度值
            @:param None
        '''
        base_time = datetime.now()
        sql = "select news_id, category, readnum , comments, date from news_api_newsdetail"
        self.cursor.execute(sql)
        result_list = self.cursor.fetchall()
        result = list()

        for row in result_list:
            try:
                time = row[4].replace("年", "-").replace("月", "-").replace("日", " ")
                print(time)
                # diff = base_time - datetime.strptime(row[4], '%Y{y}%m{m}%d{d} %H:%M').__format__(y='年', m='月', d='日')
                diff = base_time - datetime.strptime(str(time), '%Y-%m-%d %H:%M')

                # print(f"base_time:{base_time}, diff:{diff}")
                hot_value = row[2] * 0.4 + row[3] * 0.5 - diff.days * 0.1
                logger.info("HotValue:{}".format(hot_value))
                result.append((row[0], row[1], format(hot_value, ".2f")))
            except Exception:
                logger.error("转换出错")
        logger.info("新闻热度值计算完毕,返回结果 ...")
        return result

    def writeToMySQL(self):
        '''
            @Description：将热度值写入数据库
            @:param None
        '''
        for row in self.result:
            sql_w = "insert into news_api_newshot( news_id,category,news_hot ) values(%s, %s ,%s)" % (
                row[0], row[1], row[2])
            try:
                # 执行sql语句
                self.cursor.execute(sql_w)
                # 提交到数据库执行
                self.db.commit()
            except Exception:
                logger.error("rollback:{}".format(row))
                print("rollback", row)
                # 发生错误时回滚
        logger.info("热度数据写入数据库:news.newshot")


def beginCalHotValue():
    '''
        @Description：开始计算新闻的热度值
        @:param None
    '''
    logger.info("开始计算新闻的热度值 ...")
    chv = CalHotValue()
    chv.writeToMySQL()
