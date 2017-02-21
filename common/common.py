#!/usr/bin/env python
#coding:utf-8
__author__ = 'sws'

import db_mysql

def get_proxy():

    sql = '''
    SELECT proxy
    FROM proxy AS t1 JOIN (SELECT ROUND(RAND() * ((SELECT MAX(id) FROM proxy)-(SELECT MIN(id) FROM proxy))+(SELECT MIN(id) FROM proxy)) AS id) AS t2
    WHERE t1.id >= t2.id
    ORDER BY t1.id LIMIT 1;
'''
    res = db_mysql.QueryBySQL(sql)
    if len(res) == 0:
        return None
    return res[0]['proxy']




