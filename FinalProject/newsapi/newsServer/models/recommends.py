
import os
import threading
from django.http import JsonResponse

from news_api.models import spiderstate
from news_api import models

from Recommend.Controller.RecommendController import beginRecommendSystem, stopRecommendSystem, beginAnalysisSystem, \
    stopAnalysisSystem


def beginRecommend(request):
    '''
        @Description：启动推荐系统
        @:param time  --> 系统运行间隔时间
        @:param oritime  --> 系统运行间隔时间（原始记录用于前端读取显示）
    '''
    if request.method == "GET":
        time = request.GET.get('time')
        oritime = request.GET.get('oritime')
        t = threading.Thread(target=beginRecommendSystem, kwargs={'time': time})
        t.setDaemon(True)
        t.start()
        spiderstate.objects.filter(spiderid=3).update(status=1, interval=oritime)
        return JsonResponse({"status": "200", 'message': 'Success.'})
    return JsonResponse({"status": "200", 'message': 'Fail.'})


def beginAnalysis(request):
    '''
        @Description：启动数据分析系统（关键词分析、新闻相似度分析、用户IP地址分析、新闻热度分析）
        @:param time  --> 系统运行间隔时间
        @:param oritime  --> 系统运行间隔时间（原始记录用于前端读取显示）
    '''
    if request.method == "GET":
        time = request.GET.get('time')
        oritime = request.GET.get('oritime')
        t = threading.Thread(target=beginAnalysisSystem, kwargs={'time': time})
        t.setDaemon(True)
        t.start()
        spiderstate.objects.filter(spiderid=4).update(status=1, interval=oritime)
        return JsonResponse({"status": "200", 'message': 'Success.'})
    return JsonResponse({"status": "200", 'message': 'Fail.'})


def closeRecommendThread(request):
    '''
        @Description：关闭推荐系统
        @:param None
    '''
    if request.method == "GET":
        servename = request.GET.get('servename')
        if servename == 'recommend':
            spiderstate.objects.filter(spiderid=3).update(status=0, interval='')
            stopRecommendSystem()
        elif servename == 'analysis':
            spiderstate.objects.filter(spiderid=4).update(status=0, interval='')
            stopAnalysisSystem()
        # getpidandkill(servename)
        return JsonResponse({"status": "200", 'message': 'Success.'})
    return JsonResponse({"status": "200", 'message': 'Fail.'})


def getRecommendPageData(request):
    '''
        @Description：获取推荐管理页数据
        @:param None
    '''
    if request.method == "GET":
        statelist = spiderstate.objects.all()
        recommendlist = models.recommend.objects.all()
        analysisloglist = dict()
        reclist = dict()
        original_data_path = "Recommend/analysis/"
        files = os.listdir(original_data_path)
        for file in files:
            if str(file) == 'log.log':
                pass
            time = file[8:].replace("_", ' ')
            time = time[:13] + ':' + time[14:16] + ':' + time[17:]
            filepath = os.path.join('D:\\FinalProject\\newsapi\\Recommend\\analysis', file)
            analysisloglist[file] = {
                'time': time,
                'filepath': filepath
            }
        original_data_path = "Recommend/recommend/"
        files = os.listdir(original_data_path)
        for file in files:
            if str(file) == 'log.log':
                pass
            time = file[8:].replace("_", ' ')
            time = time[:13] + ':' + time[14:16] + ':' + time[17:]
            filepath = os.path.join('D:\\FinalProject\\newsapi\\Recommend\\recommend', file)
            reclist[file] = {
                'time': time,
                'filepath': filepath
            }
        statistical = dict()
        for recommend in recommendlist:
            if statistical.get(recommend.time) == None:
                statistical[recommend.time] = 1
            else:
                statistical[recommend.time] = statistical[recommend.time] + 1
        spiderstatelist = dict()
        for state in statelist:
            spiderstatelist[state.spiderid] = [state.status, state.interval]
        data = {
            'spiderstatelist': spiderstatelist,
            'statistical': statistical,
            'analysisloglist': analysisloglist,
            'reclist': reclist,

        }
        return JsonResponse({"status": "200", 'message': data})
