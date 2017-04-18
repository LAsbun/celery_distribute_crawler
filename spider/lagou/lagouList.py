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

from celery import uuid

URL = 'https://www.lagou.com/zhaopin/{key_word}/?labelWords=label'

INDEX_URL = 'https://www.lagou.com/'

CITY='北京'

headers = {
    'Cookies':'index_location_city={0}'.format(urllib.quote(CITY)),
    'Host':"www.lagou.com",

}
@app.task(bind=True, base=GenerTask)
def get_key_word(self, *args, **kwargs):

    """
    :param args:
    :param kwargs:
    :return: 拉钩列表页任务。 task_id,task, args, kwargs, 1(finished)
    """
    task_str = 'celery_distribute_crawler.spider.lagou.lagouList'
    finished  = 1
    temp_kw = {'city':CITY}
    # 拉钩限制最多只能30页
    _LA_GOU = 30


    cr = Crawler()
    cr.set_debug(True)
    resp, error = cr.req('get', INDEX_URL, html_flag=True)
    print error



    if error == '':
        tree = HTML.fromstring(resp)
        key_words_list = tree.xpath('//*[@id="sidebar"]//*[@class="menu_box"]//a[@data-lg-tj-cid="idnull"]')

        task_list = []

        for key in key_words_list[:1]:
            bas_url = key.xpath('./@href')[0] #, key.xpath('./text()')[0]
            # break

            for i in xrange(5):
                url = bas_url+str(i)
                temp_args = [url]
                task_id = get_task_id(str((task_str, temp_args, temp_kw)))

                task_list.append((task_id, task_str, json.dumps(temp_args), json.dumps(temp_kw), 1))
        print len(task_list)
        print task_list
        return task_list





@app.task(bind=True, base=LaGouTask)
def get_list(self, *args, **kwargs):
    """
    :param args: url的一些参数,包括但不限于url
    :param kwargs:  其他的参数，包括但不限于header的一些参数
    :return:
    """
    url = args[0]
    city = args[1]
    headers['Cookies'] = urllib.quote(city)
    cr = Crawler()
    cr.set_debug(True)
    cr.add_header(headers)
    resp, error = cr.req('get', url)
    # print resp, error
    return parse_list(resp, city)

def parse_list(data, city):

    job_results = []

    tree = HTML.fromstring(data)
    job_list = tree.xpath('//*[@class="con_list_item default_list"]')
    for job in job_list:
        _dic = {}
        try:
            _dic['position_id'] = str(job.xpath('./@data-positionid')[0].encode('utf-8'))
        except Exception, e:
            print e
            pass
        try:
            _dic['salary'] = str(job.xpath('./@data-salary')[0].encode('utf-8'))
        except:
            pass
        try:
            _dic['company'] = str(job.xpath('./@data-company')[0].encode('utf-8'))
        except Exception, e:
            print e
            pass
        try:
            _dic['companyid'] = str(job.xpath('./@data-companyid')[0].encode('utf-8'))
        except:
            pass
        try:
            add_re = ''.join( ee.strip() for ee in job.xpath('.//*[@class="add"]//text()')).encode('utf-8')

            _dic['add'] = ','.join([city,add_re]).encode('utf-8')
        except:
            pass
        try:

            temp_str = ''.join([ee for ee in job.xpath('.//*[@class="position"]//*[@class="li_b_l"]/text()') if ee.strip()]).strip()
            _dic['experience'] = temp_str.split('/')[0].strip().encode('utf-8')
            _dic['bach'] = temp_str.split('/')[-1].strip().encode('utf-8') #学位
        except Exception, e:
            print e
            pass
        try:
            _dic['industry'] = str(job.xpath('.//*[@class="industry"]/text()')[0].strip()).encode('utf-8')
        except:
            pass
        try:
            _dic['tags'] = [ee.strip().encode('utf-8') for ee in job.xpath('.//*[@class="list_item_bot"]/*[@class="li_b_l"]//text()') if ee.strip()]
        except:
            pass
        # print _dic['company'], _dic['bach'], _dic
        job_results.append(_dic)
    return job_results

if __name__ == '__main__':

    # temp_url = 'https://www.lagou.com/zhaopin/Python/2/'
    # get_list(temp_url, '北京')
    get_key_word()



