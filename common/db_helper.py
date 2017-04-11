#!/usr/bin/env python
#coding:utf-8
__author__ = 'sws'

import pymysql
from logger import logger


class DbHelper(object):

    def __init__(self, host, user, password, db, port=3306, charset="utf8"):

        self.__host = host
        self.__user = user
        self.__password = password
        self.__db = db
        self.__port = port
        self.__charset = charset

    def __enter__(self):
        con = pymysql.connect(host=self.__host, port=self.__port,
                              user=self.__user, password=self.__password, database=self.__db,
                              charset=self.__charset)
        self.__connection = con
        logger.error('Connected to {0}'.format(self.__db))
        return self.__connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.__connection:
            logger.error('disconnect to {0}'.format(self.__db))
            self.__connection.close()

        return False
