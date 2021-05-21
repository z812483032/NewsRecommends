# Python网络爬虫与推荐算法的新闻推荐平台

#### 介绍
网络爬虫：通过Python实现新浪新闻的爬取，可爬取新闻页面上的标题、文本、图片、视频链接（保留排版）
推荐算法：权重衰减+标签推荐+区域推荐+热点推荐


- 权重衰减进行用户兴趣标签权重的衰减，避免内容推荐的过度重复
- 标签推荐进行用户标签与新闻标签的匹配，按照匹配比例进行新闻的推荐
- 区域推荐进行IP区域确定，匹配区域性文章进行推荐
- 热点推荐进行新闻热点的计算的依据是新闻阅读量、新闻评论量、新闻发布时间



涉及框架：Django、jieba、selenium、BeautifulSoup、vue.js

#### 软件功能结构
![输入图片说明](https://images.gitee.com/uploads/images/2021/0521/115103_525fc802_5294263.png "功能结构图.png")


#### 安装教程

1.  安装Python依赖

```
pip install -r requirements.txt
#（requirements.txt文件已经包含在源码根目录下）
```

2.  安装Vue.js依赖

```
npm install
```
前端页面里用户端和管理端是分开的两个项目，所以需要再两个项目下都进行依赖安装！

3.  数据库创建/数据导入
SQL文件已经放在了Django项目根目录下，自行Navicat或其他方式导入即可

4.  数据库配置

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'news',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```


#### 使用说明

1.  Django项目启动

```
# 进入newsapi的目录
python manage.py runserver 0.0.0.0:8000
```

2.  Vue项目启动


```
//用户端
npm run dev 
//管理端
npm run serve
```

