#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2017/4/17 下午8:18 
# @Author : sws 
# @Site :  
# @File : mongo_test.py 
# @Software: PyCharm

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

HOST = "127.0.0.1"
PORT = 27017
client = MongoClient(host=HOST, port=PORT)



test = client.mongo_test

collection = test.collection_test

data = [{
    '_id':'x',
    'text':"啦啦啦",
    'args':[1, 2, 3],
    'kw':{'x':1,'v':2}
},
    {
        '_id':'xx',
        'text':4545,
    }]
try:
    task_id = collection.insert_many(data)
except DuplicateKeyError, e:
    print 55
    import traceback
    print traceback.format_exc(e)
except Exception, e:
    import traceback
    print traceback.format_exc(e)
# print task_id._id