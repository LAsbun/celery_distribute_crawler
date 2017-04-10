#!/usr/bin/env python
#coding:utf-8
__author__ = 'sws'

from celery_distribute_crawler.common.crawler import Crawler
from celery_distribute_crawler.celery0 import app

from lxml import html as HTML

URL = 'https://www.lagou.com/zhaopin/{key_word}/?labelWords=label'

INDEX_URL = 'https://www.lagou.com/'

headers = {
    'Cookies':''
}
@app.task(bind=True)
def get_key_word(self, *args, **kwargs):
    cr = Crawler()
    cr.set_debug(True)
    resp, error = cr.req('get', INDEX_URL, html_flag=True)
    print error
    if error == '':
        tree = HTML.fromstring(resp)
        key_words_list = tree.xpath('//*[@id="sidebar"]//a[@data-lg-tj-cid="idnull"]')

        for key in key_words_list:
            print key.xpath('./@href'), key.xpath('./text()')[0]
            break