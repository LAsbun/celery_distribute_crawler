#!/usr/bin/env python
#coding:utf-8
__author__ = 'sws'

from db_helper import DbHelper

# todo 动态设置数据库

from celery_distribute_crawler.celeryconfig import MYSQLDB_DB, MONGODB_HOST, MYSQLDB_PWD, MYSQLDB_USER

local_db = DbHelper(host=MONGODB_HOST, user=MYSQLDB_USER, password=MYSQLDB_PWD, db=MYSQLDB_DB)
