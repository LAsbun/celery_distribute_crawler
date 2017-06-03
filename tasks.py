#!/usr/bin/env python
#coding:utf-8
#__author__ = 'sws'

from __future__ import absolute_import
from .celery0 import app
import requests

from celery.result import AsyncResult, allow_join_result
from celery.signals import after_task_publish, task_prerun, before_task_publish


from celery_distribute_crawler.common.base_task import MyTask


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
    try:
        return a/b
    except Exception, e:
        self.retry(exc=e, countdown=1)

    # return self.request.id

@app.task(bind=True, ignore_result=True, base=MyTask)
def error_handler(self, uuid):
    print self.request.id
    result = AsyncResult(uuid)

    print result.__dict__
    with allow_join_result():
        exc = result.get(propagate=False)
    print 'Task:{0} raiseed exception: {1!r}\n{2!r}'.format(uuid, exc, result.traceback)

from celery_distribute_crawler.common.db_mysql import local_db
from collections import defaultdict
import json

@app.task(bind=True, ignore_result=True)
def get_task(self):
    res = defaultdict(list)
    conn = local_db.get_con()
    cursor = conn.cursor()
    sql = 'select task_id, task, args, kwargs from `task` where retry < 3 and finished != 4 order by priority desc limit 200'
    cursor.execute(sql)
    conn.commit()
    res = cursor.fetchall()
    # with local_db as con:
    #     with con as cursor:
    #         sql = 'select task_id, task, args, kwargs from `task` where finished in (1, 3) limit 50'
    #         cursor.execute(sql)
    #         res = cursor.fetchall()
    print
    if res:
        print res
        for ee in res:
            func = self.app.tasks[ee[1]]
            try:
                args = json.loads(ee[2]) or []
            except:
                args = []
            try:
                kwargs = json.loads(ee[3]) or {}
            except:
                kwargs = {}
            print func
            print type(args)
            print type(kwargs)
            print type(ee[0])
            func.apply_async(args=args, kwargs=kwargs, task_id=ee[0], priority=3, retry=True)


@after_task_publish.connect
def update_task(sender, headers, **kwargs):
    """
    kwargs => {
body ==> ((), {}, {u'chord': None, u'callbacks': None, u'errbacks': None, u'chain': None}), type(v) => <type 'tuple'>
sender ==> celery_distribute_crawler.tasks.get_task, type(v) => <type 'unicode'>
exchange ==> , type(v) => <type 'unicode'>
signal ==> <Signal: Signal>, type(v) => <class 'celery.utils.dispatch.signal.Signal'>
routing_key ==> celery, type(v) => <type 'unicode'>
headers ==> {u'origin': u'gen9374@sws-pc', u'root_id': '3cdbe96a-8d52-408a-a27f-c6e53ac280de', u'expires': None, u'id': '3cdbe96a-8d52-408a-a27f-c6e53ac280de', u'kwargsrepr': u'{}', u'lang': u'py', u'retries': 0, u'task': u'celery_distribute_crawler.tasks.get_task', u'group': None, u'timelimit': [None, None], u'parent_id': None, u'argsrepr': u'()', u'eta': None}, type(v) => <type 'dict'>

}
    """
    # if
    if "celery_distribute_crawler.tasks.get_task" == sender:
        # 如果是分发任务的函数不需要更新数据库任务
        return
    conn = local_db.get_con()
    cursor = conn.cursor()
    sql = """ update `task` set finished = {0} where task_id = "{1}" """.format(2, headers['id'])
    cursor.execute(sql)
    conn.commit()

    # for k, v in kwargs.iteritems():
    #     print "{0} ==> {1}, type(v) => {2}".format(k, v, type(v))
    #
    # print '*'*100


# from celery import signals
#
# def update_task(sender=None, **kwargs):
#     print sender, kwargs
#     print '*'*100
#
# @signals.worker_process_init
# def on_work_init(sender, **kwargs):
#     signals.before_task_publish.connect(update_task, sender=sender.app.tasks[get_task.func_name])
@app.task(bind=True)
def test_one_case(self, task_id=None):
    """
    查异常原因
    :param task_id: 任务唯一ID
    :return:
    """
    if task_id is not None:
        conn = local_db.get_con()
        cursor = conn.cursor()
        sql = """ select * from `task` where task_id = "{0}" """.format(task_id)
        cursor.execute(sql)
        conn.commit()
        res =  cursor.fetchall()
    else:
        conn = local_db.get_con()
        cursor = conn.cursor()
        sql = """ select * from `task` where finished = 3 limit 1 """
        cursor.execute(sql)
        conn.commit()
        res =  cursor.fetchall()

    if res:
        print res
        for ee in res:
            func = self.app.tasks[ee[1]]
            try:
                args = json.loads(ee[2]) or []
            except:
                args = []
            try:
                kwargs = json.loads(ee[3]) or {}
            except:
                kwargs = {}
            print func
            print type(args)
            print type(kwargs)
            print type(ee[0])
            print func.apply_async(args=args, kwargs=kwargs, task_id=ee[0], priority=3, retry=True)