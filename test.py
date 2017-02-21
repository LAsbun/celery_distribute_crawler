#!/usr/bin/env python
#coding:utf-8
__author__ = 'sws'

from celery_distribute_crawler.uctxt_crawler.list import get_list
# from celery_distribute_crawler.uctxt_crawler.detail import get_detail

if __name__ =="__main__":
    book_url = 'http://www.uctxt.com/book/1/1269/'
    a = get_list.delay(book_url)
    print a.result
