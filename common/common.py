#!/usr/bin/env python
#coding:utf-8
__author__ = 'sws'

import hashlib

import db_mysql

def get_proxy():
#      sql = '''
#     SELECT concat(ip,":",port) as proxy, *
#     FROM proxy t1
#     ORDER BY t1.proxy_speed, t1.id  LIMIT 2;
# '''


    sql = '''SELECT concat(ip,":",port) as proxy
    FROM proxy AS t1 JOIN (SELECT ROUND(RAND() * ((SELECT MAX(id) FROM proxy)-(SELECT MIN(id) FROM proxy))+(SELECT MIN(id) FROM proxy)) AS id) AS t2
    WHERE t1.id >= t2.id
    ORDER BY t1.verify_pass, t1.id  LIMIT 1
'''
    res = db_mysql.QueryBySQL(sql)
    print res
    if len(res) == 0:
        return None
    return res[0]['proxy']


def get_verify_proxies():
    sql = '''
    SELECT concat(ip,":",port) as proxy
    FROM proxy AS t1 JOIN (SELECT ROUND(RAND() * ((SELECT MAX(id) FROM proxy)-(SELECT MIN(id) FROM proxy))+(SELECT MIN(id) FROM proxy)) AS id) AS t2
    WHERE t1.id >= t2.id
    ORDER BY t1.verify_pass, t1.id  LIMIT 10;
''' 
    return db_mysql.QueryBySQL(sql)

def get_task_id(str):
    """
    :param args: 一个str  str((task, args, kwargs)) 需要进行md5加密的数据，按理说应该是一个不可变对象
    :return: task_id  7104ace2-dd2b-36ac-84de-56f3ed37e3ad
    """
    # hex = '%032x' % self.int
    print str
    hex = hashlib.md5(str).hexdigest()
    return '%s-%s-%s-%s-%s' % (
        hex[:8], hex[8:12], hex[12:16], hex[16:20], hex[20:])

if __name__ == '__main__':
    a = {'a':5}
    b = [1, 2]
    print get_task_id(str(("2",a,b)))
    # print get_proxy()

# sudo ssserver -s 139.162.53.11 -p 60648 -k feTT5tmuzh6g