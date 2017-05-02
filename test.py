#!/usr/bin/env python
#coding:utf-8
__author__ = 'sws'

from celery_distribute_crawler.common.base_task import GenerTask
from celery_distribute_crawler.spider.lagou.lagouList import gener_list_task
# from celery_distribute_crawler.uctxt_crawler.detail import get_detail

from celery_distribute_crawler.celery0 import app



if __name__ =="__main__":
    print '*'*100