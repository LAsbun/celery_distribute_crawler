#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17/2/15 下午7:51
# @Author  : sws
# @Site    : 
# @File    : db_redis.py
# @Software: PyCharm
from celery_distribute_crawler.celeryconfig import REDIS_DB, REDIS_HOST

import redis

# def insert_
# r = redis.Redis(host='localhost',port=6379, db=0)

R = lambda : redis.Redis(host=REDIS_HOST,db=REDIS_DB)

def insert_string_to_redis(set_name, *args):
    '''
        将字符串插入到redis数据库中
    :param set_name
    :param args: list
    :return: 插入成功的数目
    '''
    r = R()
    return r.sadd(set_name, *args)


def check_string_in_redis(set_name, string):
    '''
    检查ip_list 是不是存在redis中
    :param args:
    :return: True
    '''
    r = R()
    return r.sismember(set_name, string)

def remove_string_from_redis(set_name, string):
    '''
    移除redis中的任务串
    :param string:
    :return: True
    '''
    r = R()
    return r.srem(set_name, string)