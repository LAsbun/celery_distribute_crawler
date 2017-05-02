#!/usr/bin/env python
#coding:utf-8
__author__ = 'sws'

import requests
import time

proxies = {
    'http':'http://127.0.0.1:8087',
    'https':'https://127.0.0.1:8087',
}

# url = 'http://httpbin.org/ip'
# for i in xrange(10):
#     print i, '*'*10, "\n"
#
#     res = requests.get(url, proxies=proxies)
#     print res.text

def req_wrap(func):

    def wa():
        st = time.time()
        func()
        print time.time() - st
        print '*'*10

    return wa

@req_wrap
def req():
    url = 'http://httpbin.org/ip'
    url = 'http://www.lagou.com'
    res = requests.get(url, proxies=proxies, verify=False)
    print res.text
    print res.status_code

for i in xrange(10):
    req()