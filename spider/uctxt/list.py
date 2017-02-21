#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17/1/7 下午4:02
# @Author  : sws
# @Site    : 
# @File    : list.py
# @Software: PyCharm

'''
    list.py 给定一本书的网址解析出所有的章节,然后交给detail.py 下载具体的章节内容。
'''
from __future__ import absolute_import
import urllib
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from lxml.html import fromstring

from celery_distribute_crawler.common.logger import logger
from celery_distribute_crawler.common.crawler import Crawler
from celery_distribute_crawler.celery0 import app
from .add_detail_task import add_detail_task

def parse_list(page, url):
    '''
    :param page: list page
    :param url: list url
    :return: chap_list
    '''
    chap_list = []
    try:
        root = fromstring(page)
        chas = root.xpath("//dl[@class='chapter-list clrfix']/dd")
        for cha in chas:
            cha_url = url+cha.xpath('./a/@href')[0]
            cha_name = cha.xpath('./a/text()')[0]
            chap_list.append((cha_name,cha_url))
    except Exception, e:
        import traceback
        traceback.print_exc(e)
        logger.error("parse page occur some error" + str(e))
        raise Exception(e)

    return chap_list

# def is_has_novel(cr, book_name):
#     '''
#     对书名就行筛选
#     :param cr: 框架对象
#     :param book_name: 书名
#     :return:
#     '''
#
#     book_url_list = []  # 有些同名的书籍,碰到这种情况就把所有的同名的或者相关的小说全部下载下来
#
#     sear_url = 'http://www.uctxt.com/modules/article/search.php?searchkey=' + urllib.quote(book_name)
#
#     res, error = cr.req('get', sear_url, html_flag=True)
#     if error != '':
#         raise Exception(error)
#     if 'http://www.uctxt.com/modules/article/search.php?searchkey=' in cr.get_url_of_response():
#         logger.error("has same name book")

@app.task
@add_detail_task
def get_list(url):
    '''
    :param url:  书的链接
    :return:
    '''

    cr = Crawler()
    cr.set_debug(True)
    page, error = cr.req('get', url, html_flag=True)

    if error != '':
        logger.error('list:: occur some error'+str(error))
        raise Exception(error)
    try:
        chap_list = parse_list(page=page, url=url)
        # print chap_list
        return chap_list
    except Exception, e:
        print e

if __name__ == "__main__":
    book_url = "http://www.uctxt.com/book/1/1269/"
    get_list(book_url)
