#!/usr/bin/env python
#coding:utf-8
#__author__ = 'sws'

from __future__ import absolute_import

# from gevent import monkey
# monkey.patch_all()

from celery import Celery
import celery

from celery_distribute_crawler.common.db_mysql import local_db

app = Celery('celery_distribute_crawler',
             include=[
                 'celery_distribute_crawler.tasks',
                 'celery_distribute_crawler.spider.uctxt.list',  # 要把任务所属.py注册,不然会报错,不要把task函数也给注册。
                 'celery_distribute_crawler.spider.uctxt.detail',
                 'celery_distribute_crawler.spider.proxy.proxy_xici',
                 'celery_distribute_crawler.spider.lagou.lagouList',
             ]
             )

app.config_from_object('celery_distribute_crawler.celeryconfig')




if __name__ == "__main__":
    app.start()
    from celery_distribute_crawler.tasks import add, div_error, error_handler
    from celery import uuid
    for i in xrange(2):
        div_error.apply_async((1, 0), task_id = uuid(), link_error=error_handler.s(), base=MyTask)