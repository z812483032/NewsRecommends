# -- coding: utf-8 --
import logging
import time
from logging.handlers import TimedRotatingFileHandler

import requests, re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def getvideourl(url):
    # 获取新闻的视频
    # <video id="myMovie_html5_api" class="vjs-tech" tabindex="-1" role="application" preload="auto" playsinline="playsinline" src="https://edge.ivideo.sina.com.cn/37807320502.mp4?KID=sina,viask&Expires=1614268800&ssig=kj2tCE5xEu&reqid="></video>
    # 使用webdriver.Chrome的无头模式进行页面的完整加载，从而获取到对应的src连接
    try:
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(executable_path='C:\Program Files\Google\Chrome\Application\chromedriver.exe',
                                  options=chrome_options)
        # driver.set_page_load_timeout(20)
        # driver.maximize_window()
        driver.get(url)
        # print(driver.page_source)
        regex1 = re.compile('playsinline="playsinline" src="(.*?)"')
        video_url = regex1.findall(driver.page_source)
        for numbers in range(len(video_url)):
            video_url[numbers] = video_url[numbers].replace("amp;", "")
        # print('video_url:', video_url)
        gettime = time.time()
        logging.info("{}video_url:{}".format(gettime, video_url))
    except Exception:
        # logger.error("error:", Exception)
        video_url = []
        # print('video_url:', video_url)
    # gettime = time.time()
    # logger.info("video_url:{}".format(video_url))
    # print(driver.page_source)
    return video_url

if __name__ == '__main__':
    print(getvideourl('http://k.sina.com.cn/article_1698823241_m6541fc4902000xyok.html?cre=videopc&mod=zixun&loc=2&r=0&rfunc=88&tj=cxvertical_pc_videopc_zixun&from=movie'))