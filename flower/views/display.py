#!/usr/bin/env python
#coding:utf-8
__author__ = 'sws'

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from celery_distribute_crawler.common.db_mongo import lagou_db
from celery_distribute_crawler.celeryconfig import MONGODB_COLLECTION

from ..views import BaseHandler

class IndexHandler(BaseHandler):
    def get(self, *args, **kwargs):
        print args
        print kwargs
        print self.get_argument("index")
        task_id = self.get_argument("task_id")
        print type(task_id), task_id, type(self.get_argument("index"))
        self.render('index.html')

class PoemPageHandler(BaseHandler):
    def get(self):
        a = [{
            'name':'asa',
            'url':'xx',
            "submenu":["xx", "ss", {"rr":"ee", "00":[1, 2, 3]}],

        }]
        import json
        self.render('poem.html', xx=json.dumps(a))

class DisplayView(BaseHandler):

    def get(self):
        index = int(self.get_argument('index', 1))
        task_id = self.get_argument('task_id', None)
        if task_id:
            total_count = lagou_db[MONGODB_COLLECTION].count({"task_id":task_id})
            total_pages = total_count/10 + (1 if total_count % 10 else 0)
            skip_num = (int(index)-1)*10
            skip_num = skip_num if skip_num > 0 else 0

            res = list(lagou_db[MONGODB_COLLECTION].find(dict(task_id=task_id), skip=skip_num, limit=10))
            # uu_url_pre = "/display?"
        else:

            print index
            total_count = lagou_db[MONGODB_COLLECTION].count()
            total_pages = total_count/10 + (1 if total_count % 10 else 0)
            skip_num = (int(index)-1)*10
            skip_num = skip_num if skip_num > 0 else 0
            res = list(lagou_db[MONGODB_COLLECTION].find(skip=skip_num, limit=10))
            # uu_url_pre = "/display?index="
            # task_id = None
        print len(res)
        right = (index-1)*10+1
        left = (index-1)*10+len(res)
        if len(res) == 0:
            self.render("display2.html", task_id=task_id)
            if task_id:
                self.redirect('/display?index=1&task_id={0}'.format(task_id))
            else:
                self.redirect('/display?index=1')
            right = left = 0
        context = {
            "lines": res,
            "total_pages": total_pages,
            "index": index,
            "pre_five": index-5 if index - 5 > 0 else 1,  # 该页的前5页，如果index小于5，从一开始
            "last_five": index+5 if index + 5 <= total_pages else total_pages, # 该页的后5页，如果大于最大页数，到最大页数
            "right":right,
            "left":left,
            "total_count":total_count,
            "task_id":task_id
        }
        # print context
        self.render('display1.html', **context)

class GetDataByTaskId(BaseHandler):

    def get(self,*args, **kwargs):
        task_id = self.get_argument('task_id')
        index = int(self.get_argument('index'))
        total_count = lagou_db[MONGODB_COLLECTION].count({"task_id":task_id})
        total_pages = total_count/10 + (1 if total_count % 10 else 0)
        skip_num = (int(index)-1)*10
        skip_num = skip_num if skip_num > 0 else 0

        res = list(lagou_db[MONGODB_COLLECTION].find(dict(task_id=task_id), skip=skip_num, limit=10))
        print res
        context = {
            "lines": res,
            "total_pages": total_pages,
            "index": index,
            "pre_five": index-5 if index - 5 > 0 else 1,  # 该页的前5页，如果index小于5，从一开始
            "last_five": index+5 if index + 5 <= total_pages else total_pages, # 该页的后5页，如果大于最大页数，到最大页数
            "right":(index-1)*10+1,
            "left":(index-1)*10+len(res),
            "total_count":total_count,
            "task_id":task_id
        }
        print context
        self.render('display2.html', **context)