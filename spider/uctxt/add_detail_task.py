#!/usr/bin/env python
#coding:utf-8
__author__ = 'sws'
import json
from common.logger import logger

'''
    装饰器
'''

from .detail import get_detail

def add_detail_into_task(chap_list=[]):
    temp = []
    for cha in chap_list:
        chap_url = cha[1]
        a = get_detail.delay(chap_url)
        temp.append(a)
    return json.dumps(temp)

def add_detail_task(func, *ar, **kw):

    def wrap(*ar, **kw):
        try:
            chap_list = func(*ar, **kw)
        except Exception, e:
            logger.error("add_detail_task occur some error" + str(e))
        try:
            return json.dumps(add_detail_into_task(chap_list[:10]))
        except Exception, e:
            logger.error("add_detail_into_task occur some error" + str(e))
        # return res
    return wrap


def insert_detail_task(func, *args, **kw):

    def wrap(*args, **kw):
        print args
        res = func(*args, **kw)
        print res

    return wrap


def hh(*ar, **kw):
    print ar
    def qq(func, *ar, **kw):

        def pp(*ar, **kw):
            print func(*ar, **kw)
            print 'pp'
        print 'qq'
        return pp

    return qq
# @insert_detail_task
@hh('dshjdshadsajsdjhdasj')
def add(a=1, b=2):
    return a+b

# add(2, 2)
# b = insert_detail_task(add)
# b(3, 4)
add(2, 4)