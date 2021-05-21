# -*- coding：utf-8 -*-
import datetime
import logging
import os
from logging.handlers import TimedRotatingFileHandler

import requests, re, pymysql
from apscheduler.schedulers.blocking import BlockingScheduler

from Spider.OperationMysql import OperationMysql

'''
使用网易新闻滚动新闻的API进行新闻采集
参数分析：
        pageid      目前看应该是固定的参数默认值为153
        lid         类别ID 2509(全部) 2510（国内） 2511（国际） 2669（国际） 2512（体育） 2513（娱乐） 2514（军事） 2515（科技） 2516（财经） 2517（股市） 2518（美股）
        num         获取新闻数量 上限为50 
'''
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)-7s - %(message)s')

# 2. 初始化handler,并配置formater
log_file_handler = TimedRotatingFileHandler(filename="Spider/Urllogs/log.log",
                                            when="S", interval=5,
                                            backupCount=20)
log_file_handler.setFormatter(formatter)

# 3. 向logger对象中添加handler
logger.addHandler(log_file_handler)

def urlcollect(lid):
    op_mysql = OperationMysql() #创建数据库连接对象
    url = 'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid='+str(lid)+'&num=50' #网易新闻API
    result = requests.get(url) #对API发起请求
    result.encoding = 'utf-8' #由于API返回的数据为ISO编码的，中文在此处显示会出现乱码，因此更改为UTF-8编码
    # print('Web：', result.text)

    urls = re.findall(r'"url":"(.*?)"', result.text)    #获取API返回结果中的所有新闻详情页URL
    # times = re.findall(r'"ctime":"(.*?)"', result.text)

    # 逐条处理被\转义的字符，使之成为为转义的字符串
    # 并把处理号的URL导入到数据库中储存
    changedict = {"2518": 0, "2510": 1, "2511": 2, "2669": 3, "2512": 4, "2513": 5, "2514": 6, "2515": 7, "2516": 8, "2517": 9}
    Type = changedict.get(str(lid))
    for numbers in range(len(urls)):
        urls[numbers] = urls[numbers].replace('\\', '')
        logger.info("url:{}".format(urls[numbers]))
        time = datetime.datetime.now().strftime('%Y-%m-%d')
        sql_i = "INSERT INTO news_api_urlcollect(url, type, time) values ('%s', '%d', '%s')" % (urls[numbers], Type, time)
        op_mysql.insert_one(sql_i)
    op_mysql.conn.close()

#创建一个APScheduler对象（用于配置定时任务）
sched = BlockingScheduler()
def begincollect(time):
    time = int(time)
    try:
    # 'interval'关键词表示的是按照固定时间间隔进行的任务 add_job()添加一个定时任务
        sched.add_job(urlcollect, 'interval', max_instances=1, seconds=time, id='urlcollect1', kwargs={"lid": "2510",})
        sched.add_job(urlcollect, 'interval', max_instances=1, seconds=time, id='urlcollect2', kwargs={"lid": "2511",})
        sched.add_job(urlcollect, 'interval', max_instances=1, seconds=time, id='urlcollect3', kwargs={"lid": "2669",})
        sched.add_job(urlcollect, 'interval', max_instances=1, seconds=time, id='urlcollect4', kwargs={"lid": "2512",})
        sched.add_job(urlcollect, 'interval', max_instances=1, seconds=time, id='urlcollect5', kwargs={"lid": "2513",})
        sched.add_job(urlcollect, 'interval', max_instances=1, seconds=time, id='urlcollect6', kwargs={"lid": "2514",})
        sched.add_job(urlcollect, 'interval', max_instances=1, seconds=time, id='urlcollect7', kwargs={"lid": "2515",})
        sched.add_job(urlcollect, 'interval', max_instances=1, seconds=time, id='urlcollect8', kwargs={"lid": "2516",})
        sched.add_job(urlcollect, 'interval', max_instances=1, seconds=time, id='urlcollect9', kwargs={"lid": "2517",})
        sched.add_job(urlcollect, 'interval', max_instances=1, seconds=time, id='urlcollect10', kwargs={"lid": "2518",})
        # urlcollect(lid)
        # 为了可以控制定时任务的关闭因此需要在任务开始时保存下该进程的PID值并保存与文件中
        # 用于ClossScheduler.py中进行杀死进程
        pid = os.getpid()
        f1 = open(file='urlSpider.txt', mode='w')
        f1.write(pid.__str__())
        f1.close()
        sched.start()
    except Exception:
        logger.error('error:'+Exception)

def endsched():
    sched.shutdown()

