#!/usr/bin/env python
#coding:utf-8
__author__ = 'sws'

import pymysql
import MySQLdb
from logger import logger


class DbHelper(object):

    def __init__(self, host, user, password, db, port=3306, charset="utf8"):

        self.__host = host
        self.__user = user
        self.__password = password
        self.__db = db
        self.__port = port
        self.__charset = charset
        self.__con = None
        self._connect()

    def _connect(self):
        self.__con = MySQLdb.connect(host=self.__host, port=self.__port,
                              user=self.__user, passwd=self.__password, db=self.__db,
                              charset=self.__charset)
        # return con

    def get_cursor(self):
        if self.__con:
            cursor = self.__con.cursor()
        else:
            self._connect()
            cursor = self.__con.cursor()
        return cursor

    def get_con(self):
        if self.__con:
            return self.__con
        else:
            self._connect()
            return self.__con

    #
    # def __enter__(self):
    #     con = pymysql.connect(host=self.__host, port=self.__port,
    #                           user=self.__user, password=self.__password, database=self.__db,
    #                           charset=self.__charset)
    #     self.__connection = con
    #     logger.error('Connected to {0}'.format(self.__db))
    #     return self.__connection
    #
    # def __exit__(self, exc_type, exc_val, exc_tb):
    #     if self.__connection:
    #         # 先关闭，再print
    #         try:
    #             self.__connection.close()
    #         except pymysql.Error as e:
    #             if e.message == "Already closed":
    #                 pass
    #             else:
    #                 print 'close db :: {0}, type:{1}'.format(e.message, type(e.message))
    #                 raise e
    #         finally:
    #             logger.error('disconnect to {0}'.format(self.__db))
    #
    #     return False