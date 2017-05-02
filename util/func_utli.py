#!/usr/bin/env python
#coding:utf-8
__author__ = 'sws'
import time

def req_wrap(func):

    def wa():
        st = time.time()
        func()
        print time.time() - st
        print '*'*10

    return wa