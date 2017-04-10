#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17/1/24 下午5:12
# @Author  : sws
# @Site    :
# @File    : Proxy_xici.py
# @Software: PyCharm

from lxml import html as HTML
import requests
from user_agent import generate_user_agent

from celery_distribute_crawler.common.logger import logger
from celery_distribute_crawler.celery0 import app
from celery_distribute_crawler.common.crawler import Crawler

from celery_distribute_crawler.common import insert_db
from celery_distribute_crawler.common.common import get_proxy

REDIS_SET_NAME = 'proxy'

URL1 = 'http://www.xicidaili.com/nn/'
URL2 = 'http://www.xicidaili.com/wt/'

print generate_user_agent()
hd = {
    # 'Accept-Encoding':'gzip, deflate, sdch',
    # 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    # 'Accept-Language':'zh-CN,zh;q=0.8,und;q=0.6',
    # 'Connection':'keep-alive',
    # 'Upgrade-Insecure-Requests':'1',
    # 'Upgrade-Insecure-Requests':'1',
    # '#generate_user_agent(),
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
}


@app.task
def is_Alive(proxy, https):
    try:
        proxies = {'http': proxy}
        if https:
            proxies['https'] = proxies['http']
        res = requests.head('http://www.baidu.com',
                            proxies=proxies, timeout=60)
        print res.headers
        if res.status_code == 200:
            insert_db.insert_mysql_proxy([(proxy, https)])

        else:
            raise Exception('not ok')

    except Exception, e:
        pass

    finally:
        insert_db.remove_string_from_redis(REDIS_SET_NAME, proxy)


def get_ip_ports(content):
    tree = HTML.fromstring(content)
    tr_list = tree.xpath('//tr[@class="odd"]')
    ip_port_dic = {}
    for tr in tr_list:
        try:
            td_list = tr.xpath('./td')
            ip = td_list[1].xpath('./text()')[0]
            port = td_list[2].xpath('./text()')[0]
            https = td_list[5].xpath('./text()')[0]
            proxy = ip + ':' + port
            if 'https' in https.lower():
                https = 1
            else:
                https = 0
            ip_port_dic[proxy] = https
        except Exception, e:
            pass
    print len(ip_port_dic)
    # rest_ = db_helper.check_proxy_in_proxy(ip_port_dic.keys())
    # # 检查任务队列中是不是已经有验证任务了
    # temp_list = []
    # for res in rest_:
    #     if not db_helper.check_string_in_redis(REDIS_SET_NAME, res):
    #         temp_list.append(res)

    # if not len(temp_list):
    #     return
    temp_list = ip_port_dic.keys()
    print len(temp_list), '-' * 50
    print temp_list
    insert_db.insert_list_to_redis(REDIS_SET_NAME, temp_list)
    for res in temp_list:
        is_Alive.apply_async((res, ip_port_dic[res]), priority=2)
    # print ip_port_list
    # return ip_port_list
        # print (ip, port, https)


def get_content(base_url):
    for i in xrange(2):
        url = base_url + str(i + 1)
        cr = Crawler()
        # 获取代理

        try:
            p = get_proxy()
            if p:
                cr.set_proxy(p)
        except:
            pass

        try:

            # res = requests.get(url, headers=hd)
            # content = res.content
            content, error = cr.req('get', url, html_flag=1)
        except Exception, e:
            logger.error('get_proxy:: xici  occur some error' + str(e))
            raise Exception(e)
        # # print content, len(content)
        get_ip_ports(content)
        # insert_mysql_proxy(ip_ports_list)

@app.task(bind=True, default_retry_delay=1)
def get_xiciproxy(self):
    try:
        get_content(URL1)
    except Exception, e:
        raise self.retry(exc=e, countdown=5, max_retries=3)


# @app.task(bind=True, default_retry_delay=5)
# def div(self, x, y):
#     logger.info(('Executing task id {0.id}, args: {0.args!r} '
#                  'kwargs: {0.kwargs!r}').format(self.request))
#     try:
#         result = x / y
#     except ZeroDivisionError as e:
#         raise self.retry(exc=e, countdown=5, max_retries=3)
#     return result
    # get_content(URL2)

# get_xiciproxy()
