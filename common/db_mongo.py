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

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

HOST = "127.0.0.1"
PORT = 27017
client = MongoClient(host=HOST, port=PORT)

lagou_db = client.lagou
