#!/usr/bin/env python
#coding:utf-8
#__author__ = 'sws'

from __future__ import absolute_import
from .celery0 import app
import requests

@app.task
def add(x=0, y=0):
    return x+y
@app.task
def req(url="http://httpbin.org/ip"):
    res = requests.get(url)
    return res
    # pass
    # return x+y+z
