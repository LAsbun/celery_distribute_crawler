#!/usr/bin/env python
#coding:utf-8
__author__ = 'sws'

import celery
from celery import uuid
from pymongo.errors import DuplicateKeyError

from celery_distribute_crawler.common.db_mysql import local_db
from celery_distribute_crawler.common.db_mongo import lagou_db
from celery_distribute_crawler.celeryconfig import MONGODB_COLLECTION

class MyTask(celery.Task):
    """
        任务反馈，failure, success,retry
    """
    def on_failure(self, exc, task_id, args, kwargs, einfo):

        self._update_task(3, task_id)
        self._update_failure(task_id, str(einfo))

    def on_success(self, retval, task_id, args, kwargs):
        self._update_task(4, task_id)

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        '''
        更新retry的次数
        :param exc:
        :param task_id:
        :param args:
        :param kwargs:
        :param einfo:
        :return:
        '''
        with local_db as conn:
            with conn as cursor:
                sql = """ update `task` set retry=retry+1 where task_id = "{0}" """.format(task_id)
                cursor.execute(sql)
                conn.commit()
        # conn = local_db.get_con()
        # cursor = conn.cursor()
        # sql = """ update `task` set retry=retry+1 where task_id = "{0}" """.format(task_id)
        # cursor.execute(sql)
        # conn.commit()

    def _update_task(self, error_code, task_id):
        """
        error_code:
        0 : 无错误
        1： 有错误。 后面可以细分
        :param error_code: 后面可能会对不同的任务状态进行重试，以及其他
        :return: None
        """

        with local_db as conn:
            with conn as cursor:
                sql = """ update `task` set finished = {0} where task_id = "{1}" """.format(error_code, task_id)
                cursor.execute(sql)
                conn.commit()

        # conn = local_db.get_con()
        # cursor = conn.cursor()
        # sql = """ update `task` set finished = {0} where task_id = "{1}" """.format(error_code, task_id)
        # cursor.execute(sql)
        # conn.commit()
                
    def _update_failure(self, task_id, exc):
        print 'failure...', exc

        with local_db as conn:
            with conn as cursor:
                sql = """
                  insert into  `update_task`(error_info, task_id) VALUES ("{0}", "{1}")
                  ON Duplicate key UPDATE error_info = "{0}"
                """.format(conn.escape_string(exc), task_id)
                cursor.execute(sql)
                conn.commit()

        # conn = local_db.get_con()
        # cursor = conn.cursor()
        # sql = """
        #             insert into  `update_task`(error_info, task_id) VALUES ("{0}", "{1}")
        #             ON Duplicate key UPDATE error_info = "{0}"
        #     """.format(conn.escape_string(exc), task_id)
        # cursor.execute(sql)
        # conn.commit()

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

        with local_db as conn:
            with conn as cursor:
                sql = ''' insert into `task` (task_id, task, args, kwargs, finished) values(%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE task_id = VALUES(task_id)'''
                cursor.execute(sql)
                conn.commit()
        # con = local_db.get_con()
        # cursor = con.cursor()
        # sql = ''' insert into `task` (task_id, task, args, kwargs, finished) values(%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE task_id = VALUES(task_id)'''
        # cursor.executemany(sql, retval)
        # con.commit()

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
        lagou_db[MONGODB_COLLECTION].insert_many(data)

# print local_db
#
# cursor = local_db.get_cursor()
# print cursor
# import time
# time.sleep(10)
# print cursor
# time.sleep(10)
# print cursor