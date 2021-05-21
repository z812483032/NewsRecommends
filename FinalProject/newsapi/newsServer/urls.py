
'''newsServer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
'''
from django.contrib import admin
from django.urls import path

from newsServer.models.news import all_news, del_news, reconewsbytags, typenews, reconewsbysimilar, getpicture, \
    getNewsDetailByNewsid, all_news_to_page, newsHistory, newsHotRec, getComments, gethotnews, updateGiveLike, submitComments, \
    submitCommenttoUser, getManageHomeData, updateRecHis, searchNews

from newsServer.models.user import add_user, all_user, del_user, up_user, user_login, user_register, getHistory, getRecNes, \
    getUserMessage, up_user_by_user, up_tags, getMessage, getTip, setMessageHadRead, getRegistrPageData, tourists_login, setUserHeadPic, \
    getall_comments, del_comments, searchUser, searchComments

from newsServer.models.spider import beginUrlSpider, beginDetailSpider, closeSpiderThread, getSpiderPageData

from newsServer.models.download import download

from newsServer.models.recommends import beginRecommend, closeRecommendThread, beginAnalysis, getRecommendPageData

urlpatterns = [
    path('admin/', admin.site.urls),
    path('news/', all_news),
    path('news/search/', searchNews),
    path('user/allcomments/', getall_comments),
    path('user/add/', add_user),
    path('user/all/', all_user),
    path('user/search/', searchUser),
    path('comments/search/', searchComments),
    path('user/del/', del_user),
    path('user/delcomment/', del_comments),
    path('user/up/', up_user),
    path('user/login/', user_login),
    path('user/tourists/', tourists_login),
    path('news/del/', del_news),
    path('news/recbt/', reconewsbytags),
    path('news/typ/', typenews),
    path('news/recbs/', reconewsbysimilar),
    path('user/regis/', user_register),
    path('news/pict/', getpicture),
    path('news/id/', getNewsDetailByNewsid),
    path('news/all/', all_news_to_page),
    path('news/his/', newsHistory),
    path('news/updateRec/', updateRecHis),
    path('user/his/', getHistory),
    path('user/rec/', getRecNes),
    path('news/nhr/', newsHotRec),
    path('news/com/', getComments),
    path('user/det/', getUserMessage),
    path('user/upb/', up_user_by_user),
    path('user/getRegistrPageData/', getRegistrPageData),
    path('user/uptags/', up_tags),
    path('news/hotnews/', gethotnews),
    path('news/updgivelike/', updateGiveLike),
    path('news/subcom/', submitComments),
    path('news/subcomtou/', submitCommenttoUser),
    path('user/message/', getMessage),
    path('user/gettip/', getTip),
    path('user/sethadread/', setMessageHadRead),
    path('user/updateheadpic/', setUserHeadPic),
    path('management/homedata/', getManageHomeData),
    path('spider/urlbegin/', beginUrlSpider),
    path('spider/detailbegin/', beginDetailSpider),
    path('spider/closeserve/', closeSpiderThread),
    path('spider/getspiderdata/', getSpiderPageData),
    path('recommend/getrecommenddata/', getRecommendPageData),
    path('recommend/startrecommend/', beginRecommend),
    path('recommend/startanalysis/', beginAnalysis),
    path('recommend/stopsystem/', closeRecommendThread),
    path('download/logs/', download),
]
