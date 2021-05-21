# -- coding: utf-8 --
import logging
import os
import time

from logging.handlers import TimedRotatingFileHandler

import requests, re
from apscheduler.schedulers.blocking import BlockingScheduler
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from Spider.OperationMysql import OperationMysql

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)-7s - %(message)s')

# 2. 初始化handler,并配置formater
log_file_handler = TimedRotatingFileHandler(filename="Spider/Detaillogs/log.log",
                                            when="S", interval=5,
                                            backupCount=20)
log_file_handler.setFormatter(formatter)

# 3. 向logger对象中添加handler
logger.addHandler(log_file_handler)


def has_class_but_no_id(tag):
    return not tag.has_attr('class') and not tag.has_attr('id')


def getnewsdetail(url):
    # 获取页面上的详情内容并将详细的内容汇集在news集合中
    result = requests.get(url)
    result.encoding = 'utf-8'
    soup = BeautifulSoup(result.content, features="html.parser")
    title = getnewstitle(soup)
    if title == None:
        return None
    date = getnewsdate(soup)
    mainpage, orimainpage = getmainpage(soup)
    if mainpage == None:
        return None
    pic_url = getnewspic_url(soup)
    videourl = getvideourl(url)
    news = {'mainpage': mainpage,
            'pic_url': pic_url,
            'title': title,
            'date': date,
            'videourl': videourl,
            'origin': orimainpage,
            }
    return news


def getmainpage(soup):
    '''
        @Description：获取正文部分的p标签内容，网易对正文部分的内容通过文本前部的空白进行标识\u3000
        @:param None
    '''
    if soup.find('div', id='article') != None:
        soup = soup.find('div', id='article')
        p = soup.find_all('p')
        for numbers in range(len(p)):
            p[numbers] = p[numbers].get_text().replace("\u3000", "").replace("\xa0", "").replace("新浪", "新闻")
        text_all = ""
        for each in p:
            text_all += each
        logger.info("mainpage:{}".format(text_all))
        return text_all, p
    elif soup.find('div', id='artibody') != None:
        soup = soup.find('div', id='artibody')
        p = soup.find_all('p')
        for numbers in range(len(p)):
            p[numbers] = p[numbers].get_text().replace("\u3000", "").replace("\xa0", "").replace("新浪", "新闻")
        text_all = ""
        for each in p:
            text_all += each
        logger.info("mainpage:{}" + text_all)
        return text_all, p
    else:
        return None, None


def getnewspic_url(soup):
    '''
        @Description：获取正文部分的pic内容，网易对正文部分的图片内容通过div中class属性为“img_wrapper”
        @:param None
    '''
    pic = soup.find_all('div', class_='img_wrapper')
    pic_url = re.findall('src="(.*?)"', str(pic))
    for numbers in range(len(pic_url)):
        pic_url[numbers] = pic_url[numbers].replace("//", 'https://')
    logging.info("pic_url:{}".format(pic_url))
    return pic_url


def getnewsdate(soup):
    '''
        @Description：获取新闻的发布时间，网易对新闻的发布时间使用span的class属性为“date”
        @:param None
    '''
    if soup.find('span', class_='date') != None:
        date = str(soup.find('span', class_='date').text)
    else:
        date = str(soup.find('span', id="pub_date").text)
    logger.info("date:{}".format(date))
    return date


def getnewstitle(soup):
    '''
        @Description：获取新闻的标题，网易对新闻的标题使用h1的class属性为“main-title”
        @:param None
    '''
    if soup.find('h1', class_='main-title') != None:
        title = soup.find('h1', class_='main-title').text
    elif soup.find('h1', id='artibodyTitle') != None:
        title = soup.find('h1', id='artibodyTitle').text
    else:
        return None
    logger.info("title:{}".format(title))
    return title


def getvideourl(url):
    '''
        @Description：获取新闻的视频，使用webdriver.Chrome的无头模式进行页面的完整加载，从而获取到对应的src连接
        @:param None
    '''
    try:
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(executable_path='C:\Program Files\Google\Chrome\Application\chromedriver.exe',
                                  options=chrome_options)
        driver.get(url)
        regex1 = re.compile('playsinline="playsinline" src="(.*?)"')
        video_url = regex1.findall(driver.page_source)
        for numbers in range(len(video_url)):
            video_url[numbers] = video_url[numbers].replace("amp;", "")
    except Exception:
        video_url = []
    return video_url


def getdatabaseurl():
    '''
        @Description：获取数据库中的所有未进行详情内容爬取的URL
        @:param None
    '''
    op_mysql = OperationMysql()
    searchresult = op_mysql.search_all('select url, type from news_api_urlcollect where handle=0')
    op_mysql.conn.close()
    if len(searchresult) == 0:
        logger.warning(" No such url to get detail")
        return None
    else:
        logger.info("Got All Url")
        return searchresult


def insertdatabase(news, geturl, Type):
    '''
        @Description：将爬取到的页面详情内容存入数据库中
        @:param None
    '''
    op_mysql = OperationMysql()
    url = geturl['url']
    title = str(news['title'])
    date = str(news['date'])
    pic_url = str(news['pic_url'])
    videourl = str(news['videourl'])
    mainpage = str(news['mainpage'])
    orimainpage = str(news['origin'])
    sql = 'insert into news_api_newsdetail(url, title, date, pic_url, videourl, mainpage, category, readnum, comments, origin) values ("%s", "%s", "%s", "%s", "%s", "%s", %d, 0, 0, "%s")' % (
        url, title, date, pic_url, videourl, mainpage, Type, orimainpage)
    try:
        op_mysql.insert_one(sql)
        sql = 'update news_api_urlcollect set handle=1 where url="' + url + '"'
        op_mysql = OperationMysql()
        op_mysql.update_one(sql)
    except Exception:
        print('数据插入失败')


def deleteurl(url):
    '''
        @Description：删除数据库中错误（无效）的URL
        @:param None
    '''
    op_mysql = OperationMysql()
    sql = 'delete from news_api_urlcollect where url="' + url['url'] + '"'
    op_mysql.delete_one(sql)


def insertalldetial():
    '''
        @Description：循环进行urlcollect
        @:param None
    '''
    logger.info("Begin Collect News_Url")
    urllist = getdatabaseurl()
    if None != urllist:
        for url in urllist:
            logger.info(" Begin to handle url: %s" % url['url'])
            news = getnewsdetail(url['url'])
            if news == None:
                pass
            Type = url['type']
            if news == None:
                deleteurl(url)
            else:
                try:
                    insertdatabase(news=news, geturl=url, Type=Type)
                except Exception:
                    return None
                    logger.error("Insert News_url Error!!")


sched = BlockingScheduler()


def begindetailcollect(time):
    sched.add_job(insertalldetial, 'interval', max_instances=1, seconds=int(time), id='detailcollect1', kwargs={})
    pid = os.getpid()
    f1 = open(file='detailSpider.txt', mode='w')
    f1.write(pid.__str__())
    f1.close()
    sched.start()


def endsched():
    sched.pause_job("detailcollect1")
