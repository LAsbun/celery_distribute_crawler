#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17/1/7 下午6:31
# @Author  : sws
# @Site    :
# @File    : detail.py
# @Software: PyCharm
from __future__ import absolute_import
import sys
import json
reload(sys)
sys.setdefaultencoding('utf-8')

from lxml.html import fromstring
import chardet

from celery_distribute_crawler.common.logger import logger
from celery_distribute_crawler.common.crawler import Crawler

from celery_distribute_crawler.celery0 import app

'''
    detail.py 负责解析章节详细内容
'''


def parse_detail(page=''):
    '''
    :param page: detail page
    :return: chap_content
    '''
    # page = open('page.html', 'r').read()
    print chardet.detect(page)
    try:
        page = page.decode('GB2312', 'ignore')
        # page = unicode(page, encoding='gbk').encode('utf-8')#.decode('gbk').encode('utf-8')
        root = fromstring(page)
        chas = root.xpath('//div[@id="content"]//text()')
        chap_content = '\n'.join(chas)
    except Exception, e:
        import traceback
        traceback.print_exc(e)
        logger.error("parse page occur some error" + str(e))
        raise Exception(e)
    # print chap_content
    return chap_content.encode('utf-8')

@app.task
def get_detail(url):
    '''
    :param url:  章节的链接
    :return:  章节的具题内容
    '''

    cr = Crawler()
    cr.set_debug(True)
    page, error = cr.req('get', url, html_flag=True)

    if error != '':
        logger.error('detail:: occur some error'+str(error))
        raise Exception(error)
    try:
        chap_content= parse_detail(page=page)
        chardet.detect(chap_content)
        # open('ss.txt', 'wb').write(chap_content)
        return json.dumps(chap_content)
    except Exception, e:
        logger.error("detail:: get_detail occur some error"+str(e))
        print e

if __name__ == "__main__":
    book_cha_url = "http://www.uctxt.com/book/6/6640/8164197.html"
    get_detail(book_cha_url)
    # parse_detail()
