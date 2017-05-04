#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2017/4/17 下午9:09 
# @Author : sws 
# @Site :  
# @File : db_mongo.py 
# @Software: PyCharm

"""
    mongodb

"""
from urllib import quote_plus

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

from celery_distribute_crawler.celeryconfig import MONGODB_HOST, MONGODB_PORT, MONGODB_WRITER, MONGODB_WRITER_PWD, MONGODB_DB

HOST = "127.0.0.1"
PORT = 27017
uri = "mongodb://%s:%s@%s/%s" % (
                quote_plus(MONGODB_WRITER), quote_plus(MONGODB_WRITER_PWD), MONGODB_HOST, MONGODB_DB)

print uri
client = MongoClient(host=uri, port=MONGODB_PORT, connect=False)

lagou_db = client[MONGODB_DB]
print lagou_db
print lagou_db['lagou_list'].insert_many([{}, {}])