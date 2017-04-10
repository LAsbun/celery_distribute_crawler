#!/usr/bin/env python
#coding:utf-8
#__author__ = 'sws'

from __future__ import absolute_import
from .celery0 import app
import requests

from celery.result import AsyncResult, allow_join_result

import celery


class MyTask(celery.Task):

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print exc,
        print task_id
        print args
        print kwargs
        print einfo
        print 5


from time import sleep

@app.task
def add(x=0, y=0):
    return x+y
@app.task
def req(url="http://httpbin.org/ip"):
    res = requests.get(url)
    return res
    # pass
    # return x+y+z

@app.task(bind=True, base=MyTask)
def div_error(self, a, b):
    # return a/b
    print float(a) / b
    sleep(5)
    # return self.request.id

@app.task(bind=True, ignore_result=True)
def error_handler(self, uuid):
    print self.request.id
    result = AsyncResult(uuid)

    print result.__dict__
    with allow_join_result():
        exc = result.get(propagate=False)
    print 'Task:{0} raiseed exception: {1!r}\n{2!r}'.format(uuid, exc, result.traceback)