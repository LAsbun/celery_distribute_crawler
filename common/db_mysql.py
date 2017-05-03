#!/usr/bin/env python
#coding:utf-8
__author__ = 'sws'

from db_helper import DbHelper

# todo 动态设置数据库

from celery_distribute_crawler.celeryconfig import MYSQLDB_DB, MONGODB_HOST, MYSQLDB_PWD_WRITER, MYSQLDB_USER_WRITER

local_db = DbHelper(host=MONGODB_HOST, user=MYSQLDB_USER_WRITER, password=MYSQLDB_PWD_WRITER, db=MYSQLDB_DB)
