#!/usr/bin/env python
#coding:utf-8
__author__ = 'sws'

import celery
from celery import uuid
from pymongo.errors import DuplicateKeyError

from celery_distribute_crawler.common.db_mysql import local_db
from celery_distribute_crawler.common.db_mongo import lagou_db

class MyTask(celery.Task):
    """
        任务反馈，failure, success
    """
    def on_failure(self, exc, task_id, args, kwargs, einfo):

        print 'on_failure....{0}, type:{1}'.format(einfo.exc_info, type(einfo))
        self._update_task(3, task_id)
        self._update_failure(task_id, str(einfo))

    def on_success(self, retval, task_id, args, kwargs):
        # print 'success...', retval
        self._update_task(4, task_id)
        # self._insert_test_table([(task_id, retval)])

    # def _insert_test_table(self, data):
    #     with local_db as conn:
    #         with conn as cursor:
    #             sql = """insert ignore into `hh` (task_id, hh) values(%s, %s)"""
    #             cursor.executemany(sql, args=data)

    # def _insert_lagou(self, data):
    #     with local_db as conn:
    #         with conn as cursor:
    #             sql = '''insert '''

    def _update_task(self, error_code, task_id):
        """
        error_code:
        0 : 无错误
        1： 有错误。 后面可以细分
        :param error_code: 后面可能会对不同的任务状态进行重试，以及其他
        :return: None
        """

        cursor = local_db.get_cursor()
        sql = """ update `task` set finished = {0} where task_id = "{1}" """.format(error_code, task_id)
        cursor.execute(sql)
        #
        # with local_db as conn:
        #     with conn as cursor:
        #         sql = """ update `task` set finished = {0} where task_id = "{1}" """.format(error_code, task_id)
        #         cursor.execute(sql)
                
    def _update_failure(self, task_id, exc):
        print 'failure...', exc

        cursor = local_db.get_cursor()
        conn = local_db.get_con()
        sql = """
                    insert into  `hh`(error_info, task_id) VALUES ("{0}", "{1}") ON Duplicate key UPDATE error_info = "{0}"
            """.format(conn.escape_string(exc), task_id)
        # sql = """update `hh` set error_info = {0} where task_id = "{1}" """.format(exc, task_id)
        cursor.execute(sql)

        # with local_db as conn:
        #     with conn as cursor:
        #         sql = """
        #             insert into  `hh`(error_info, task_id) VALUES ("{0}", "{1}") ON Duplicate key UPDATE error_info = "{0}"
        #         """.format(conn.escape_string(exc), task_id)
        #         # sql = """update `hh` set error_info = {0} where task_id = "{1}" """.format(exc, task_id)
        #         cursor.execute(sql)
        #         # sql = '''update `update_task` set error_info = {0} where task_id = {1}'''.format(task_id,exc)
        #         # cursor.execute(sql)

class GenerTask(MyTask):
    """
        执行完生成任务
    """
    def on_success(self, retval, task_id, args, kwargs):
        """
        :param retval:  任务列表，[ (task, args, kwargs), (task, args, kwargs)]
        :param task_id:
        :param args:
        :param kwargs:
        :return:
        """
        super(GenerTask, self).on_success(retval, task_id, args, kwargs)

        cursor = local_db.get_cursor()
        sql = ''' insert into `task` (task_id, task, args, kwargs, finished) values(%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE task_id = VALUES(task_id)'''
        cursor.executemany(sql, retval)

        # with local_db as conn:
        #     with conn as cursor:
        #         sql = ''' insert into `task` (task_id, task, args, kwargs, finished) values(%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE task_id = VALUES(task_id)'''
        #         cursor.executemany(sql, retval)


class LaGouTask(MyTask):

    def on_success(self, retval, task_id, args, kwargs):
        super(LaGouTask, self).on_success(retval, task_id, args, kwargs)
        print 'success...', retval
        self._insert_lagou(retval)


    def _insert_lagou(self, data):
        lagou_db['lagou_List'].insert_many(data)

# print local_db
#
# cursor = local_db.get_cursor()
# print cursor
# import time
# time.sleep(10)
# print cursor
# time.sleep(10)
# print cursor