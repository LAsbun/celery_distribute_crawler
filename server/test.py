#!/usr/bin/env python
#coding:utf-8
__author__ = 'sws'

import os.path

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=18889, help="run on the given port", type=int)

from bson import Binary, Code

from celery_distribute_crawler.common.db_mongo import lagou_db

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

class PoemPageHandler(tornado.web.RequestHandler):
    def post(self):
        noun1 = self.get_argument('noun1')
        noun2 = self.get_argument('noun2')
        verb = self.get_argument('verb')
        noun3 = self.get_argument('noun3')
        self.render('poem.html', roads=noun1, wood=noun2, made=verb,
                difference=noun3)

class Flip(tornado.web.RequestHandler):

    def get(self, index=1):
        index = int(index)
        total_count = lagou_db['lagou_List'].count()
        total_pages = total_count/10 + 1 if total_count % 10 else 0
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
        self.render('pagin.html', **context)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[(r'/', IndexHandler), (r'/poem', PoemPageHandler), (r'/page/(\d+)', Flip)],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "statics"),
        debug=True
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()