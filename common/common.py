#!/usr/bin/env python
#coding:utf-8
__author__ = 'sws'

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

# print get_proxy()

# sudo ssserver -s 139.162.53.11 -p 60648 -k feTT5tmuzh6g