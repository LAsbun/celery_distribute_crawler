#!/usr/bin/env python
#coding:utf-8
from __future__ import absolute_import

__author__ = 'sws'



BROKER_URL = "amqp://guest:guest@127.0.0.1:5672//"#'redis://127.0.0.1:6379/0' #'amqp://guest@123.206.71.224//'#'amqp://dongwm:123456@localhost:5672/web_develop' # 使用RabbitMQ作为消息代理

CELERY_RESULT_BACKEND = "amqp://guest:guest@127.0.0.1:5672//" # 'redis://123.206.71.224:6379/0' #amqp://' #'redis://localhost:6379/0' # 把任务结果存在了Redis

# CELERY_RESULT_BACKEND = "amqp://guest:guest@127.0.0.1:5672//"#'redis://127.0.0.1:6379/0'

CELERY_TASK_SERIALIZER = 'json' # 任务序列化和反序列化使用msgpack方案

CELERY_RESULT_SERIALIZER = 'json' # 读取任务结果一般性能要求不高，所以使用了可读性更好的JSON

CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24 # 任务过期时间，不建议直接写86400，应该让这样的magic数字表述更明显

CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'msgpack', 'yaml'] # 指定接受的内容类型

CELERY_IGNORE_RESULT = True  # 这个会忽略掉所有的结果，导致不能够获取到运行错误时的错误信息

CELERYD_MAX_TASKS_PER_CHILD = 200 # 每个worker执行了多少任务就会死掉，我建议数量可以大一些，比如200

CELERYD_CONCURRENCY = 10 # celery worker的并发数 也是命令行-c指定的数目,事实上实践发现并不是worker也多越好,保证任务不堆积,加上一定新增任务的预留就可以

CELERY_ENABLE_UTC = True

CELERY_TIMEZONE = 'Asia/Shanghai'
# 配置定时任务

result_backend = 'rpc://'

result_persistent = False
from datetime import timedelta

CELERYBEAT_SCHEDULE = {
    'add-every-30-seconds': {
        'task': 'celery_distribute_crawler.spider.proxy.proxy_xici.get_xiciproxy',
        'schedule': timedelta(seconds=600),
        'options':{
        	'priority':3,
        }
        # 'args': (16, 16)
    },
}

# redis 相关
REDIS_DB = '0'
REDIS_HOST = '127.0.0.1'
