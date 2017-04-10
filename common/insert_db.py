#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17/1/23 下午6:33
# @Author  : sws
# @Site    : 
# @File    : insert_db.py
# @Software: PyCharm

# import pymongo
import redis
import time

from celery_distribute_crawler.common import db_mysql
from celery_distribute_crawler.common.logger import logger
from celery_distribute_crawler.celeryconfig import REDIS_DB, REDIS_HOST


def insert_mysql_proxy(args):
    '''
    插入数据库
    :param args:
    :return:
    '''

    sql = '''insert ignore into proxy (proxy, https) values (%s, %s)'''
    count = db_mysql.ExecuteSQLs(sql, args)
    logger.error('insert into proxy success ' + str(count))


def update_proxy_all(args):
    '''
    更新代理
    :param args 代理
    '''
    t_time = int(time.time())
    sql = """update proxy_all20170329  """


def check_proxy_in_proxy(args):
    '''
    检查ip+端口是不是在数据库中,如果是就不用验证了。
    :param args:
    :return: 不在数据库中的ip_port  一个列表
    '''

    sql = ''' select proxy from proxy where proxy in ({0}) '''.format(str(args)[1:-1])
    print sql
    res = db_mysql.QueryBySQL(sql)
    set_a = set(args)
    set_b = set([pr['proxy'] for pr in res])
    return list(set_a-set_b)



R = lambda : redis.Redis(host=REDIS_HOST,db=REDIS_DB)


def insert_list_to_redis(set_name, args):
    '''
        将字符串插入到redis数据库中
    :param set_name
    :param args: list
    :return: 插入成功的数目
    '''
    r = R()
    count = r.sadd(set_name, *args)
    logger.error('insert into redis  success: {0}'.format(str(count)))


def check_string_in_redis(set_name, string):
    '''
    检查string 是不是存在redis中
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
    
    cou = r.srem(set_name, string)
    logger.error("remove from redis {0} is {1}".format(string, cou))
    return cou