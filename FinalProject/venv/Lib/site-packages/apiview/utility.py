# encoding: utf-8
from __future__ import absolute_import, unicode_literals

import six
import base64
import decimal
import datetime
from functools import partial
import hashlib
import imghdr
import json
import logging
import math
import os
import random
import re
import string
import urllib
import uuid
import posixpath

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import default_storage
from django.core.mail.message import EmailMultiAlternatives
from django.utils.encoding import force_str, force_text, force_bytes

from . import validators


DATE_FORMAT = getattr(settings, 'DATE_FORMAT', None)
TIME_FORMAT = getattr(settings, 'TIME_FORMAT', '%H:%M:%S')
DATETIME_FORMAT = getattr(settings, 'DATETIME_FORMAT', None)
ASCII_CHARS = 'ABCDEFGHJKLMNPQRSTUVWXYZ'
DIGIT_CHARS = '23456789'
CHARS = DIGIT_CHARS + ASCII_CHARS


def id_generator(size=6, chars=CHARS):
    return ''.join(random.sample(chars, int(size)))


def ids_generator(size=6, amount=10, chars=CHARS):
    return [id_generator() for _ in range(amount)]


def unique_ids_generator(ids, size=6, amount=10, chars=CHARS):
    local_ids = []
    count = 0
    while count < amount:
        local_id = id_generator()
        if local_id not in ids and local_id not in local_ids:
            local_ids.append(local_id)
            count += 1
    return local_ids


# 用于ImageFiled的upload_to参数，生成文件名，useuuid＝True使用uuid
# secs为字段列表组成文件名
def uuid_filename_generator(instance, filename, path_format):
    filetype = os.path.splitext(filename)[1]
    if len(filetype) == 0:
        filetype = '.'

    basename = ''.join((force_text(uuid.uuid4()), filetype))

    dirname = force_text(datetime.datetime.now().strftime(force_str(path_format)))
    filename = posixpath.join(dirname, basename)
    return default_storage.generate_filename(filename)
    # expandpath = datetime.datetime.strftime(datetime.datetime.now(), path)
    # return os.path.join(expandpath, filename)


def get_uuid_filename(path_format):
    return partial(uuid_filename_generator, path_format=path_format)


# 判断是否手机号
def IsMobileNumber(mobile):
    return validators.mobile.is_valid(mobile)


g_weekdaystr = ('周一', '周二', '周三', '周四', '周五', '周六', '周日')


def get_weekday_str(date):
    return g_weekdaystr[date.weekday()]


def safeMobile(mobile):
    if len(mobile) != 11:
        return ''
    return mobile[:3]+'****'+mobile[-4:]


def priceFormat(price, decimal_places=2):
    return (('%%.%df' % decimal_places) % price).strip('0').strip('.')

# def getResponseErr(ecode, loginfo, **kwargs):
#     from errDef import errResponse
#     from rest_framework.response import Response
#     err = errResponse(ecode, kwargs)
#     logging.debug(loginfo, err)
#     return(Response(err))


# 定义枚举
class Enum(object):
    def __init__(self, **kwargs):
        for attr, val in kwargs.items():
            setattr(self, attr, val)


def enum(**enums):
    return Enum(**enums)


def safe_loadjson(jstr):
    retobj = None
    try:
        retobj = json.loads(jstr)
    except Exception:
        reportExceptionByMail("json load error")

    return retobj

# def prase_url(request, value):
#     if not value or value.strip() == '':
#         return ''
#     if '://' in value:
#         return value
#     if request:
#         return request.build_absolute_uri(value)
#     else:
#         return config.SL_HTTP_HOST + value


def appendMediaURL(value):
    if hasattr(value, 'url'):
        return value.url

    if not value or value.strip() == '':
        return ''
    else:
        return os.path.join(settings.MEDIA_URL, value)

# def real_url(request, pic_field):
#     if not pic_field:
#         return ''
#     if hasattr(pic_field, 'name'):
#         pic_field = pic_field.name
#     return prase_url(request, appendMediaURL(pic_field))


def hash_sha1(str):
    if not str or str.strip() == '':
        return None

    mdTemp = hashlib.sha1()
    mdTemp.update(str)

    return mdTemp.hexdigest()


def getServerIP():
    import socket
    ip = '0.0.0.0'
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('114.114.114.114', 53))
        ip = s.getsockname()[0]
    except Exception:
        reportExceptionByMail('get server ip failed')

    return ip


LST_COLOR_CHARS = ('白', '黑', '红', '绿', '蓝', '黄', '银', '灰', '粉', '紫', '橙', '棕', '香槟', '咖啡', '金')


def colorValidate(color):
    if not color or len(color) == 0:
        return '请输入颜色'

    if len(color) > 10:
        return '颜色输入过长'

    if 0 not in [string.find(color, c) == -1 for c in LST_COLOR_CHARS]:
        return '请用中文正确输入颜色'

    return ''


def sendEmail(subject, add_to, html_content):
    from django.conf import settings

    if isinstance(add_to, six.string_types):
        addr1 = add_to
        add_to = list()
        add_to.append(addr1)
    subject = force_text(subject)
    if subject.find(settings.EMAIL_SUBJECT_PREFIX) < 0:
        subject = settings.EMAIL_SUBJECT_PREFIX + subject

    # send_mail(subject, html_content, settings.EMAIL_HOST_USER,
    # add_to, fail_silently=False)

    # text_content = 'This is an important message.'
    # html_content = '<p>This is an <strong>important</strong> message.</p>'

    msg = EmailMultiAlternatives(subject, html_content, settings.EMAIL_HOST_USER, add_to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def earth_distance(lat1, lon1, lat2, lon2):
    radlat1 = (math.pi/180)*lat1
    radlat2 = (math.pi/180)*lat2

    radlon1 = (math.pi/180)*lon1
    radlon2 = (math.pi/180)*lon2

    a = radlat1-radlat2
    b = radlon1-radlon2
    s = 2 * math.asin(math.sqrt(math.pow(math.sin(a / 2), 2) +
                                math.cos(radlat1) *
                                math.cos(radlat2) *
                                math.pow(math.sin(b / 2), 2)))
    earth_radius = 6378.137
    s = s * earth_radius
    if s < 0:
        return -s
    else:
        return s


# 返回一天的最开始时间和返回时间，组成元组
def dayRange(day):
    day_min = datetime.datetime.combine(day, datetime.time.min)
    day_max = datetime.datetime.combine(day, datetime.time.max)
    return day_min, day_max


# 返回一月的最开始时间和返回时间，组成元组
def monthRange(day):
    import calendar

    lastday = calendar.monthrange(day.year, day.month)

    fromday = datetime.datetime(day.year, day.month, 1)
    today = datetime.datetime(day.year, day.month, lastday[1])

    return fromday, today


def rsa_decrypt(srcStr, prikey):
    import rsa
    res_data = base64.b64decode(srcStr)
    lendata = len(res_data)
    patch = lendata % 128
    if patch > 0:
        patch = 128 - patch
        res_data += '\0' * patch
    secs = len(res_data) / 128
    result = ''
    for sec in range(0, secs):
        result += rsa.decrypt(res_data[sec*128:sec*128+128], prikey)

    return result


def querystring2dict(querystring):
    from six.moves.urllib_parse import urlparse
    resultDict = dict((k, v if len(v) > 1 else v[0]) for k, v in urlparse.parse_qs(querystring).items())
    return resultDict


# 获取严重级别颜色
def getSeverityColor(val, step, shreshold=0):
    level = (val - shreshold) / step
    if level > 255:
        level = 255
    if level < 0:
        level = 0

    return '#%02x%02x00' % (level, 255-level)


# 时间差对象转字符串
def timedelta2Str(dt, ms=False):
    secs = dt.total_seconds()
    sign = "-" if secs < 0 else ""

    if secs < 0:
        dt = datetime.timedelta(seconds=-secs)
    sdt = str(dt)
    if not ms:
        sdt = sign + sdt.split('.')[0]
    return sdt


_logger_exception = logging.getLogger('exception')


def reportExceptionByMail(msg, *args, **kwargs):

    _logger_exception.exception(msg, *args, **kwargs)


def yields(listobj, n=1000):
    i = 0
    len_ = len(listobj)
    while n*i < len_:
        yield listobj[n*i:(i+1)*n]
        i += 1


# sql执行结果cursor转换为字典
def getCursorDict(c):
    fnames = [fd[0] for fd in c.description]

    result = list()
    for row in c:
        result.append(dict(zip(fnames, row)))

    return result


def filter_emoji(desstr, restr=''):
    '''
    过滤表情
    '''
    try:
        co = re.compile('[\U00010000-\U0010ffff]')
    except re.error:
        co = re.compile('[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return co.sub(restr, desstr)


def str_2_emoji(emoji_str):
    if six.PY3:
        from html.parser import HTMLParser
    else:
        from HTMLParser import HTMLParser
    '''
    把字符串转换为表情
    '''
    if not emoji_str:
        return emoji_str
    h = HTMLParser.HTMLParser()
    emoji_str = h.unescape(h.unescape(emoji_str))
    # 匹配u"\U0001f61c"和u"\u274c"这种表情的字符串
    co = re.compile(r"u[\'\"]\\[Uu]([\w\"]{9}|[\w\"]{5})")
    pos_list = []
    result = emoji_str
    # 先找位置
    for m in co.finditer(emoji_str):
        pos_list.append((m.start(), m.end()))
    # 根据位置拼接替换
    for pos in range(len(pos_list)):
        if pos == 0:
            result = emoji_str[0:pos_list[0][0]]
        else:
            result = result + emoji_str[pos_list[pos-1][1]:pos_list[pos][0]]
        result = result + eval(emoji_str[pos_list[pos][0]:pos_list[pos][1]])
        if pos == len(pos_list) - 1:
            result = result + emoji_str[pos_list[pos][1]:len(emoji_str)]
    return result


def datetime2timestamp(dtime):
    import time
    if not dtime:
        return 0
    return int(time.mktime(dtime.timetuple()))


def timestamp2datetime(timestamp):
    return datetime.datetime.fromtimestamp(timestamp)


def datetime2str(dtime, format):
    return dtime.strfomrt(format)


def format_res_data(data):

    if hasattr(data, 'items'):
        for k, v in data.items():
            data[k] = format_res_data(v)
        return data
    elif isinstance(data, (tuple, list)):
        tmp = []
        for item in data:
            tmp.append(format_res_data(item))
        return tmp
    elif isinstance(data, decimal.Decimal):
        return six.text_type(data)
    else:
        timeformat = None
        canstamp = False
        if isinstance(data, datetime.datetime):
            canstamp = True
            timeformat = DATETIME_FORMAT
        elif isinstance(data, datetime.date):
            canstamp = True
            timeformat = DATE_FORMAT
        elif isinstance(data, datetime.time):
            canstamp = False
            timeformat = TIME_FORMAT
        if timeformat is not None:
            return data.strftime(timeformat)
        elif canstamp:
            return datetime2timestamp(data)
        else:
            return data


# 把字典内容赋值给对象属性
def copy_dict2obj(dict, obj):
    if not dict or not obj:
        return
    for key in dict.keys():
        setattr(obj, key, dict[key])


def percentage(i1, i2):
    if i2 == 0:
        return None
    return round((i1 * 1.0) / (i2 * 100.0), 2)


def time_to_second(t):
    if not t or not isinstance(t, datetime.time):
        return 0
    return t.hour * 3600 + t.minute * 60 + t.second


# des加解密
def des_encode(inputdes, key):
    from . import des
    try:
        des_enc = des.des(key[:8], padmode=des.PAD_PKCS5)
        inputdes = force_bytes(inputdes)
        return base64.b64encode(des_enc.encrypt(inputdes))
    except Exception:
        import inspect
        msg = "des_encode error"
        msg += ","
        inspect.stack()
        msg += ' => '.join('%s-%s:%d' % (item[1], item[3], item[2]) for item in inspect.stack())
        reportExceptionByMail(msg)
        return None


def des_decode(inputdes, key):
    from . import des

    debase64 = None
    try:
        debase64 = base64.b64decode(inputdes)
    except Exception:
        reportExceptionByMail("'" + inputdes + "'")
        return None

    try:
        des_dec = des.des(key[:8], padmode=des.PAD_PKCS5)
        return des_dec.decrypt(debase64)
    except Exception:
        import inspect
        msg = "des_decode error"
        msg += ","
        inspect.stack()
        msg += ' => '.join('%s-%s:%d' % (item[1], item[3], item[2]) for item in inspect.stack())
        reportExceptionByMail(msg)
        return None


def pad(s, pad_size):
    return s + (pad_size - len(s) % pad_size) * chr(pad_size - len(s) % pad_size)


def unpad(s):
    return s[0:-ord(s[-1])]


def aes_encode(inputdes, key):
    from Crypto.Cipher import AES
    iv = str(bytearray(16))
    cipher = AES.new(key[:16], AES.MODE_ECB, iv)
    inputdes = force_bytes(inputdes)
    return base64.b64encode(cipher.encrypt(pad(inputdes, 16)))


def aes_decode(inputdes, key):
    from Crypto.Cipher import AES
    iv = str(bytearray(16))
    cipher = AES.new(key[:16], AES.MODE_ECB, iv)
    return unpad(cipher.decrypt(base64.b64decode(inputdes)))


def get_host_from_url(url):
    protocol, s1 = urllib.splittype(url)
    host, s2 = urllib.splithost(s1)
    host, port = urllib.splitport(host)
    if port is None:
        port = 80
    return host, port


def date_format(date_str):
    try:
        _date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        return _date
    except Exception:
        return None


def month_from_date(day):
    import calendar
    if isinstance(day, six.string_types):
        day = datetime.datetime.strptime(day, '%Y-%m-%d').date()
    month_code = day.strftime("%Y-%m")
    wday, monthRange = calendar.monthrange(day.year, day.month)
    month_begin = datetime.date(day.year, day.month, 1)
    month_end = datetime.date(day.year, day.month, monthRange)
    return month_code, month_begin, month_end


def week_from_date(day):
    if isinstance(day, six.string_types):
        day = datetime.datetime.strptime(day, '%Y-%m-%d').date()
    from dateutil.relativedelta import relativedelta, MO, SU
    weekbegin = day + relativedelta(weekday=MO(-1))
    weekend = day + relativedelta(weekday=SU(1))
    week_code = '%d_%d' % (day.isocalendar()[0], day.isocalendar()[1])
    return week_code, weekbegin, weekend


def fields_verify(model_admin, field_names, only_fields=False):
    model = model_admin.model
    real_field_names = []
    for field_name in field_names:
        try:
            if model._meta.get_field(field_name):
                real_field_names.append(field_name)
        except Exception:
            if not only_fields:
                if hasattr(model_admin, field_name):
                    real_field_names.append(field_name)
    return real_field_names


def get_qrimgurl_by_content(request, content, **kwargs):
    import qrcode
    import os
    from hashlib import md5
    expandpath = datetime.datetime.now().strftime("qr/%Y/%Y%m%d/")
    filename = "%s%s.png" % (expandpath, md5(content).hexdigest())
    file = os.path.join(settings.MEDIA_ROOT, filename)
    path, name = os.path.split(file)
    if not os.path.exists(path):
        os.makedirs(path)
    with open(file, 'wb') as fp:
        qrcode.make(content, **kwargs).save(fp)
    qrurl = request.build_absolute_uri('/')[:-1] + settings.MEDIA_URL + filename
    return qrurl


def check_time(time_to_check, on_time, off_time):
    if on_time > off_time:
        if time_to_check > on_time or time_to_check < off_time:
            return True
    elif on_time < off_time:
        if time_to_check > on_time and time_to_check < off_time:
            return True
    elif time_to_check == on_time:
        return True
    return False


def request_ip(request):
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    return ip


# 邮件签名, 包括IP地址,时间, 是否生产环境等
# def mail_remark():

#     remark = '<br>IP:%s <br>时间:(%s)' % (settings.SERVER_IP, datetime.datetime.now())
#     remark += '<br>调试模式：{b}'.format(b='是' if settings.DEBUG else '否')
#     remark += '<br>生产环境：{b}'.format(b='是' if config.IS_PRODUCTION else '否')

#     return remark

def decode_base64_image(base_str):
    image = None
    try:
        missing_padding = 4 - len(base_str) % 4
        if missing_padding:
            base_str += b'=' * missing_padding
        base_str = base64.b64decode(base_str)
        if len(base_str) > 0:
            image = SimpleUploadedFile(name='pic.jpg', content=base_str, content_type='image/jpeg')
            if not imghdr.what(image):
                image = None
    except Exception as e:
        logging.error(e)
        image = None
    return image
