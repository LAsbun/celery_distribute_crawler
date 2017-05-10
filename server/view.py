#!/usr/bin/env python
#coding:utf-8
__author__ = 'sws'

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from celery_distribute_crawler.common.db_mongo import lagou_db

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

class PoemPageHandler(tornado.web.RequestHandler):
    def get(self):
        a = [{
            'name':'asa',
            'url':'xx',
            "submenu":["xx", "ss", {"rr":"ee", "00":[1, 2, 3]}],

        }]
        import json
        self.render('poem.html', xx=json.dumps(a))

class FlipHandler(tornado.web.RequestHandler):

    def get(self, index=1):
        print index
        index = int(index)
        total_count = lagou_db['lagou_List'].count()
        total_pages = total_count/10 + (1 if total_count % 10 else 0)
        skip_num = (int(index)-1)*10
        skip_num = skip_num if skip_num > 0 else 0
        res = lagou_db['lagou_List'].find(skip=skip_num, limit=10)
        print type(res[0])
        context = {
            "lines": res,
            "total_pages": total_pages,
            "index": index,
            "pre_five": index-5 if index - 5 > 0 else 1,  # 该页的前5页，如果index小于5，从一开始
            "last_five": index+5 if index + 5 <= total_pages else total_pages # 该页的后5页，如果大于最大页数，到最大页数
        }
        print context
        self.render('pagin.html', **context)