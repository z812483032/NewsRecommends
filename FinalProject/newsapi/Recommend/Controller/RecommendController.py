
from apscheduler.schedulers.blocking import BlockingScheduler
from Recommend.NewsRecommendByCity import beginrecommendbycity
from Recommend.NewsRecommendByHotValue import beginrecommendbyhotvalue
from Recommend.NewsRecommendByTags import beginNewsRecommendByTags
from Recommend.NewsKeyWordsSelect import beginSelectKeyWord
from Recommend.NewsHotValueCal import beginCalHotValue
from Recommend.NewsCorrelationCalculation import beginCorrelation
from Recommend.HotWordLibrary import beginHotWordLibrary

sched = BlockingScheduler()
sched2 = BlockingScheduler()


def beginRecommendSystem(time):
    '''
        @Description：推荐系统启动管理器（基于城市推荐、基于热度推荐、基于新闻标签推荐）
        @:param time --> 时间间隔
    '''
    sched.add_job(func=beginrecommendbycity, trigger='interval', max_instances=1, seconds=int(time),
                  id='NewsRecommendByCity',
                  kwargs={})
    sched.add_job(beginrecommendbyhotvalue, 'interval', max_instances=1, seconds=int(time),
                  id='NewsRecommendByHotValue',
                  kwargs={})
    sched.add_job(beginNewsRecommendByTags, 'interval', max_instances=1, seconds=int(time), id='NewsRecommendByTags',
                  kwargs={})
    sched.start()


def stopRecommendSystem():
    '''
        @Description：推荐系统关闭管理器
        @:param None
    '''
    sched.remove_job('NewsRecommendByCity')
    sched.remove_job('NewsRecommendByHotValue')
    sched.remove_job('NewsRecommendByTags')


def beginAnalysisSystem(time):
    '''
        @Description：数据分析系统启动管理器（关键词分析、热词分析、新闻相似度分析、热词统计）
        @:param time --> 时间间隔
    '''
    sched2.add_job(beginSelectKeyWord, trigger='interval', max_instances=1, seconds=int(time),
                  id='beginSelectKeyWord',
                  kwargs={"_type": 2})
    sched2.add_job(beginCalHotValue, 'interval', max_instances=1, seconds=int(time),
                  id='beginCalHotValue',
                  kwargs={})
    sched2.add_job(beginCorrelation, 'interval', max_instances=1, seconds=int(time), id='beginCorrelation',
                  kwargs={})
    sched2.add_job(beginHotWordLibrary, 'interval', max_instances=1, seconds=int(time), id='beginHotWordLibrary',
                  kwargs={})
    sched2.start()

def stopAnalysisSystem():
    '''
        @Description：数据分析系统关闭管理器
        @:param None
    '''
    sched2.remove_job('beginSelectKeyWord')
    sched2.remove_job('beginCalHotValue')
    sched2.remove_job('beginCorrelation')
    sched2.remove_job('beginHotWordLibrary')
    sched2.shutdown()
