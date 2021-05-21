import datetime
import json

from django.core import serializers
from django.db.models import Q
from django.http import JsonResponse
from news_api.models import user, history, newsdetail, recommend, hotword, message, comments


def add_user(request):
    '''
        @Description：管理员新增用户
        @:param userid---用户id
        @:param username---用户名
        @:param gender---性别
        @:param ip---IP地址
        @:param tags---用户标签
    '''
    if request.method == "POST":
        req = json.loads(request.body)
        if True:
            userid = req["userid"]
            username = req["username"]
            gender = req["gender"]
            ip = req["ip"]
            password = req["password"]
            tags = req["tags"]
            '''插入数据'''
            add_user = user(userid=userid, username=username, gender=gender, ip=ip, password=password, tags=tags)
            add_user.save()
            return JsonResponse({"status": "200", "msg": "add user sucess."})
        else:
            return JsonResponse({"status": "400", "message": "please check param."})


def all_user(request):
    '''
        @Description：管理员获取所有用户信息
    '''
    if request.method == "GET":
        userlist = serializers.serialize("json", user.objects.all())
        response = JsonResponse({"status": 100, "userlist": userlist})
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Methods"] = "GET,POST"
        response["Access-Control-Allow-Headers"] = "Origin,Content-Type,Cookie,Accept,Token"
        response["Cache-Control"] = "no-cache"
        return response


def getall_comments(request):
    '''
        @Description：管理员获取所有评论信息
    '''
    if request.method == "GET":
        response = JsonResponse({"status": 100, "commentslist": serializers.serialize("json", comments.objects.all())})
        return response


def del_comments(request):
    '''
        @Description：管理员获取所有评论信息
    '''
    if request.method == "GET":
        commentsid = request.GET.get('commentsid')
        newsid = request.GET.get('newsid')
        userid = request.GET.get('userid')
        choose = int(request.GET.get('choose'))
        print(choose)
        if choose == 1:
            res = comments.objects.filter(id=commentsid).update(status="封禁")
            sendMessage = "尊敬的用户您好，您在标题《" + newsdetail.objects.filter(news_id=newsid)[
                0].title + "》的新闻评论，存在言论不当的问题，评论内容已被管理员封禁！"
            time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            message(userid=userid, message=sendMessage, newsid=newsid, time=time, title="来自管理员的信息", hadread=0).save()
            if res == 0:
                return JsonResponse({"status": "100", "message": "Fail."})
            else:
                return JsonResponse({"status": "100", "message": "Success."})
        elif choose == 0:
            res = comments.objects.filter(id=commentsid).update(status="正常")
            sendMessage = "尊敬的用户您好，您在标题《" + newsdetail.objects.filter(news_id=newsid)[
                0].title + "》的新闻评论，已被管理员解除封禁，给您带来不便，十分抱歉！"
            time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            message(userid=userid, message=sendMessage, newsid=newsid, time=time, title="来自管理员的信息", hadread=0).save()
            if res == 0:
                return JsonResponse({"status": "100", "message": "Fail."})
            else:
                return JsonResponse({"status": "100", "message": "Success."})


def del_user(request):
    '''
        @Description：管理员删除用户信息
        @:param userid---用户id
    '''
    if request.method == "GET":
        userid = request.GET.get('userid')
        # print(user.objects.filter(userid=userid).delete()[0])
        if user.objects.filter(userid=userid).delete()[0] == 0:
            return JsonResponse({"status": "100", "message": "Fail."})
        else:
            return JsonResponse({"status": "100", "message": "Success."})


def up_user(request):
    '''
        @Description：管理员更新用户信息
        @:param userid---用户id
        @:param username---用户名
        @:param gender---性别
        @:param ip---IP地址
        @:param tags---用户标签
    '''
    if request.method == "POST":
        req = json.loads(request.body)
        userid = req['userid']
        username = req['username']
        gender = req['gender']
        ip = req['ip']
        tags = req['tags']
        res = user.objects.filter(userid=userid).update(username=username, gender=gender, ip=ip, tags=tags)
        # print(res)
        if res == 0:
            return JsonResponse({"status": "100", "message": "Fail."})
        else:
            return JsonResponse({"status": "100", "message": "Success."})


def user_login(request):
    '''
        @Description：用户登录
        @:param userid---用户id
        @:param password---用户密码
    '''
    if request.method == "POST":
        req = json.loads(request.body)
        userid = req['userid']
        password = req['password']
        res = user.objects.filter(userid=userid, password=password)
        if len(res) > 0:
            # print(res[0].userid)
            # res[0].userid
            username = res[0].username
            if res[0].gender == 1:
                gender = '男'
            else:
                gender = '女'
            pict = res[0].headPortrait
            data = {
                "userid": userid,
                "username": username,
                "gender": gender,
                "headPortrait": pict,
            }
            ip = get_ip(request)
            print(ip)
            user.objects.filter(userid=userid).update(ip=str(ip))
            if int(userid) != 100000:
                users = user.objects.filter(userid=userid)[0]
                usertags = set(users.tags.split(','))
                if len(users.tagsweight) > 0:
                    weight = eval(users.tagsweight)
                    for item in list(weight):
                        if weight[item] >= 0.05:
                            weight[item] = float(format(weight.get(item) - 0.15, ".3f"))
                            if weight.get(item) > 0:
                                user.objects.filter(userid=userid).update(tagsweight=str(weight).replace("\'", "\""))
                            else:
                                weight.pop(item)
                                print('weight', weight)
                                user.objects.filter(userid=userid).update(tagsweight=str(weight).replace("\'", "\""))
                                try:
                                    usertags.remove(item)
                                except Exception:
                                    print(Exception)
                                newusertags = ','.join(usertags)
                                user.objects.filter(userid=userid).update(tags=newusertags)
        if len(res):
            return JsonResponse({"status": "100", "message": "Success.", "data": data})
        else:
            return JsonResponse({"status": "400", "message": "Fail."})


def tourists_login(request):
    if request.method == "GET":
        tourist = user.objects.filter(userid=100000)[0]
        data = {
            'userid': 100000,
            'username': "游客",
            "gender": '男',
            "headPortrait": tourist.headPortrait,
        }
        return JsonResponse({"status": "100", "message": "Success.", "data": data})
    return JsonResponse({"status": "100", "message": "Fail."})


def user_register(request):
    '''
        @Description：用户登录
        @:param userid---用户id
        @:param username---用户名
        @:param password---用户密码
        @:param tags---用户自选标签
    '''
    if request.method == "POST":
        req = json.loads(request.body)
        userid = req['userid']
        password = req['password']
        username = req['username']
        gender = req['gender']
        if gender == '男':
            gender = 1
        elif gender == '女':
            gender = 0
        tags = req['tags']
        ip = get_ip(request)
        tagsweight = {}
        tag = str(tags).split(",")
        for i in tag:
            tagsweight[i] = 0.5
        print(tagsweight)
        tagsweight = str(tagsweight).replace("\'", "\"")
        add_user = user(userid=userid, username=username, gender=gender, ip=ip, password=password, tags=tags,
                        tagsweight=tagsweight)
        add_user.save()
        return JsonResponse({"status": 200, "message": "Success."})
    return JsonResponse({"status": 200, "message": "Fail."})


def get_ip(request):
    '''获取请求者的IP信息'''
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')  # 判断是否使用代理
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # 使用代理获取真实的ip
    else:
        ip = request.META.get('REMOTE_ADDR')  # 未使用代理获取IP
    return ip


def getHistory(request):
    '''
       @Description：获取用户浏览历史记录
       @:param userid---用户id
    '''
    if request.method == "GET":
        userid = request.GET.get('userid')
        historylist = history.objects.filter(userid=userid).order_by('-id')
        newslist = dict()
        for historyitem in historylist:
            if len(newsdetail.objects.filter(news_id=historyitem.history_newsid)) > 0:
                news = newsdetail.objects.filter(news_id=historyitem.history_newsid)[0]
                # print(historyitem.history_newsid)
                data = {
                    'newsid': historyitem.history_newsid,
                    'time': historyitem.time,
                }
                newslist[news.title] = data
        # print(newslist)
        # return JsonResponse({"status": "200", 'newslist': serializers.serialize("json", newslist)})
        return JsonResponse({"status": "200", 'newslist': newslist})


def getRecNes(request):
    '''
       @Description：获取用户推荐新闻
       @:param userid---用户id
   '''
    if request.method == "GET":
        userid = request.GET.get('userid')
        if userid != None:
            recnewslist = recommend.objects.filter(userid=userid, hadread=0).order_by('-time')
            recnewsdetaillist = list()
            for renews in recnewslist:
                recnewsdetailfromdata = newsdetail.objects.filter(news_id=renews.newsid)
                data = {
                    'newsid': recnewsdetailfromdata[0].news_id,
                    'title': recnewsdetailfromdata[0].title,
                    'date': recnewsdetailfromdata[0].date,
                    'species': renews.species,
                    'pic_url': recnewsdetailfromdata[0].pic_url,
                    'mainpage': recnewsdetailfromdata[0].mainpage,
                    'readnum': recnewsdetailfromdata[0].readnum,
                    'comments': recnewsdetailfromdata[0].comments,
                }
                recnewsdetaillist.append(data)
        return JsonResponse({"status": "200", 'newslist': recnewsdetaillist})
    else:
        return JsonResponse({"status": "200", 'newslist': None})


def getUserMessage(request):
    '''
        @Description：获取用户推荐新闻
        @:param userid---用户id
    '''
    userid = request.GET.get('userid')
    userdetail = user.objects.filter(userid=userid)[0]
    if userdetail.gender == 1:
        gender = '男'
    else:
        gender = '女'
    hotwordlist = hotword.objects.all().order_by('-num')[:60]
    wordlist = list()
    for hotwords in hotwordlist:
        wordlist.append(hotwords.hotword)
    tags = userdetail.tags
    if tags != None:
        tags = str(tags.split(','))
    else:
        tags = []
    data = {
        'userid': userdetail.userid,
        'username': userdetail.username,
        'gender': gender,
        'tags': tags,
        'headportrait': userdetail.headPortrait,
        'hotword': wordlist,
    }
    return JsonResponse({"status": "200", 'userdetail': data})


def up_user_by_user(request):
    '''
        @Description：用户更新用户信息
        @:param userid---用户id
        @:param username---用户名
        @:param gender---性别
    '''
    if request.method == "POST":
        req = json.loads(request.body)
        userid = req['userid']
        username = req['username']
        gender = req['gender']
        if gender == '男':
            gender = 1
        else:
            gender = 0
        res = user.objects.filter(userid=userid).update(userid=userid, username=username, gender=gender)
        # print(res)
        if res == 0:
            return JsonResponse({"status": "100", "message": "Fail."})
        else:
            return JsonResponse({"status": "100", "message": "Success."})


def up_tags(request):
    '''
       @Description：更新用户标签
       @:param userid---用户id
       @:param tags---标签详情
    '''
    if request.method == "POST":
        req = json.loads(request.body)
        userid = req['userid']
        tags = req['tags']
        userdetail = user.objects.filter(userid=userid)[0]
        if userdetail.tagsweight != None:
            oringin_weight = json.loads(str(userdetail.tagsweight))
        else:
            oringin_weight = {}
        new_weight = {}
        for tag in tags:
            if tag in oringin_weight:
                new_weight[tag] = oringin_weight[tag]
            else:
                new_weight[tag] = 0.5
        tags = list(set(tags))
        new_tags = ",".join(tags)
        new_weight = json.dumps(new_weight, ensure_ascii=False)
        user.objects.filter(userid=userid).update(tags=new_tags)
        user.objects.filter(userid=userid).update(tagsweight=new_weight)
        return JsonResponse({"status": "100", "message": new_weight})


def getMessage(request):
    '''
        @Description：获取用户消息
        @:param userid --> 用户ID
    '''
    if request.method == "GET":
        userid = request.GET.get('userid')
        print(userid)
        messagelist = message.objects.filter(userid=userid)
        mlist = list()
        for index in messagelist:
            data = {
                'id': index.id,
                'message': index.message,
                'time': index.time,
                'hadread': index.hadread,
                'newsid': index.newsid,
                'title': index.title,
            }
            mlist.append(data)
        return JsonResponse({"status": "100", "message": mlist})


def getTip(request):
    '''
        @Description：获取用户端是否有未读消息提示
        @:param userid --> 用户ID
    '''
    if request.method == "GET":
        userid = request.GET.get('userid')
        if userid != None:
            if len(message.objects.filter(userid=userid, hadread=0)):
                return JsonResponse({"status": "100", "message": 1})
            else:
                return JsonResponse({"status": "100", "message": 0})


def setMessageHadRead(request):
    '''
        @Description：更新用户消息已读状态
        @:param id --> 消息ID
    '''
    if request.method == "GET":
        id = request.GET.get('id')
        message.objects.filter(id=id).update(hadread=1)
        return JsonResponse({"status": "100", "message": 'Success.'})


def getRegistrPageData(request):
    '''
        @Description：获取注册页数据
        @:param None
    '''
    if request.method == "GET":
        hotwordlist = hotword.objects.all().order_by('-num')[0:150]
        resultlist = list()
        for worditem in hotwordlist:
            resultlist.append(worditem.hotword)
        return JsonResponse({"status": "100", "message": resultlist})
    return JsonResponse({"status": "100", "message": "Fail.."})


def setUserHeadPic(request):
    '''
        @Description：设置用户头像
        @:param userid --> 用户ID
        @:param picurl --> 头像URL
    '''
    if request.method == "POST":
        req = json.loads(request.body)
        userid = req['userid']
        picurl = req['picurl']
        try:
            user.objects.filter(userid=userid).update(headPortrait=picurl)
        except Exception:
            return JsonResponse({"status": "100", "message": "Fail.."})
        return JsonResponse({"status": "100", "message": "Success.."})


def searchUser(request):
    '''
        @Description：管理端搜索用户（模糊搜索）
        @:param keyword --> 关键词
    '''
    if request.method == "GET":
        keyword = request.GET.get('keyword')
        userlist = user.objects.filter(
            Q(userid__contains=keyword) | Q(username__contains=keyword) | Q(tags__contains=keyword))
        response = JsonResponse({"status": 100, "userlist": serializers.serialize("json", userlist)})
        return response


def searchComments(request):
    '''
        @Description：管理端搜索评论
        @:param keyword --> 关键词
    '''
    if request.method == "GET":
        keyword = request.GET.get('keyword')
        commentslist = comments.objects.filter(
            Q(newsid__contains=keyword) | Q(comments__contains=keyword) | Q(userid__contains=keyword) | Q(
                touserid__contains=keyword))
        response = JsonResponse({"status": 100, "commentslist": serializers.serialize("json", commentslist)})
        return response
