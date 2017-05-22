#!/usr/bin/env python
#coding:utf-8
__author__ = 'sws'

from lxml import html as HTML
import urllib
import json

from celery_distribute_crawler.common.crawler import Crawler
from celery_distribute_crawler.celery0 import app
from celery_distribute_crawler.common.base_task import LaGouTask, GenerTask
from celery_distribute_crawler.common.common import get_task_id


from collections import defaultdict

from celery import uuid

URL = 'https://www.lagou.com/jobs/positionAjax.json?city={city}&needAddtionalResult=false'

REFERER_URL = 'https://www.lagou.com/jobs/list_{key_word}?labelWords=sug&fromSearch=true'

INDEX_URL = 'https://www.lagou.com/'

CITY_LIST = [
    '北京',
    '上海',
    '深圳',
    '广州',
    '杭州',
    '南京',
]


@app.task(bind=True, base=GenerTask)
def gener_list_task(self, *args, **kwargs):
    """
    生成拉钩列表页任务
    :param args:
    :param kwargs:
    :return: 拉钩列表页任务。 task_id,task, args, kwargs, 1(finished)
    """
    headers = {
    'Cookies':'index_location_city={0}'.format(urllib.quote('北京')),
    'Host':"www.lagou.com",
    }
    task_str = 'celery_distribute_crawler.spider.lagou.lagouList.crawl_list'
    finished  = 1
    # temp_kw = {
    #     'headers': {'Referer':''},
    #     'method': 'post,',
    #     'url':''
    # }
    # 拉钩限制最多只能30页
    _LA_GOU = 30

    cr = Crawler()
    cr.set_proxy('127.0.0.1:8087')
    print cr.br.proxies
    resp, error = cr.req('get', INDEX_URL, html_flag=True, headers=headers)
    print error

    if error == '':
        tree = HTML.fromstring(resp)
        key_words_list = tree.xpath('//*[@id="sidebar"]//*[@class="menu_box"]//a[@data-lg-tj-cid="idnull"]')

        task_list = []

        # post_data = {
        #     'first': '',
        #     'pn': '',
        #     'kd': ''
        # }

        for key in key_words_list:
            key_word = key.xpath('./text()')[0].encode('utf-8') #, key.xpath('./text()')[0]
            print key_word
            # break
            post_data = {}
            post_data['kd'] = key_word
            for i in xrange(1, _LA_GOU+1):

                if i == 1:
                    post_data['first'] = True
                else:
                    post_data['first'] = False

                post_data['pn'] = i

                temp_kw = {}
                temp_args = []
                url = URL.format(**{'city': urllib.quote('北京')})
                temp_kw['url'] = url
                temp_kw['method'] = 'post'
                temp_kw['headers'] = {}
                temp_kw['headers']['Referer'] = REFERER_URL.format(**{'key_word': urllib.quote(key_word)})
                temp_kw['req_param'] = post_data
                task_id = get_task_id(str((task_str, temp_args, temp_kw)))

                task_list.append((task_id, task_str, json.dumps(temp_args), json.dumps(temp_kw), finished))

        print task_list[0]
        print len(task_list)
        return task_list
    # pass

@app.task(bind=True, base=LaGouTask)
def crawl_list(self, *args, **kwargs):
    """
    抓取拉钩列表页
    :param args: url的一些参数,包括但不限于url
    :param kwargs:  其他的参数，包括但不限于header的一些参数
    :return:
    """
    try:

        try:
            if not kwargs:
                kwargs = {"url": "https://www.lagou.com/jobs/positionAjax.json?city=%E5%8C%97%E4%BA%AC&needAddtionalResult=false", "headers": {"Referer": "https://www.lagou.com/jobs/list_Java?labelWords=sug&fromSearch=true"}, "method": "post", "req_param": {"first": True, "pn": 1, "kd": "Java"}}
                args = []
        except:
            pass
        atgs = []

        list_header = {
            "Host": "www.lagou.com",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            # 'Cookie'
        }

        # cr.set_debug(True)
        url = kwargs['url']
        method = kwargs.get('method', 'get')
        referer = kwargs.get('headers', {}).get('Referer', None)

        param = kwargs.get('req_param', {})

        if referer:
            list_header['Referer'] = referer

        cr = Crawler()
        cr.set_proxy('127.0.0.1:8087')
        # cr.req('get', 'https://activity.lagou.com/activityapi/icon/showIcon.json?callback=jQuery111306045271617199887_1493362357868&type=COMPANY&_=1493362357869')
        # cr.add_referer('referer')
        resp, error = cr.req(method=method, url=url, headers=list_header, paras=param)
        # print resp
        json_data = json.loads(resp)
        results = json_data.get('content', {}).get('positionResult', {}).get('result', [])
        if not results:
            return []
        return parse_list(self.request.id, results)
    except Exception, e:
        raise self.retry(exc=e, countdown=2)

def parse_list(task_id, job_results):
    """
    为每一个职位信息加上一个task_id
    :param task_id:
    :param jon_results:
    :return:
    """

    for job in job_results:
        job['task_id'] = task_id

    return job_results


if __name__ == '__main__':

    # temp_url = 'https://www.lagou.com/zhaopin/Java/4/'
    # a = gener_list_task(temp_url, u'北京')
    kw = {"url": "https://www.lagou.com/jobs/positionAjax.json?city=%E5%8C%97%E4%BA%AC&needAddtionalResult=false", "headers": {"Referer": "https://www.lagou.com/jobs/list_Java?labelWords=sug&fromSearch=true"}, "method": "post", "req_param": {"first": True, "pn": 1, "kd": "Java"}}
    kw = {'url': 'https://www.lagou.com/jobs/positionAjax.json?city=%E5%8C%97%E4%BA%AC&needAddtionalResult=false', 'headers': {'Referer': u'https://www.lagou.com/jobs/list_%E5%BE%8B%E5%B8%88?labelWords=sug&fromSearch=true'}, 'method': 'post', 'req_param': {'kd': '\u4ea7\u54c1\u8fd0\u8425', 'pn': 5, 'first': False}}
    atgs = []
    import time
    st = time.time()
    for i in xrange(10):
        try:

            print crawl_list(*atgs, **kw)
        except:
            pass
        else:
            print time.time()-st
            break


