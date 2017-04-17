#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17/1/7 下午5:02
# @Author  : sws
# @Site    :
# @File    : Crawler.py
# @Software: PyCharm

# coding=utf8
import urllib
import json
import httplib
import requests
from user_agent import generate_user_agent as GetUserAgent
from logger import logger


class Crawler(object):

    def __init__(self, referer='', headers={},  md5='', qid='', p='', **kw):

        self.proxy = p
        self.headers = headers
        self.br = requests.session()
        self.br.keep_alive = False
        self.Userproxy = False
        headers['User-Agent'] = GetUserAgent()
        self.br.headers.update(headers)
        self.resp = ''
        if p:
            self.set_proxy(p)

    def set_debug(self, flag=True):
        if flag:
            httplib.HTTPConnection.debuglevel = 1
            httplib.HTTPSConnection.debuglevel = 1

    def req(self, mechod, url, paras={}, paras_type=1, html_flag=True, time_out=(60, 180), **kw):

        html, error = '', ''
        try:
            if mechod.lower() == 'get':
                url = url + urllib.urlencode(paras)
                self.resp = self.br.get(url, timeout=time_out, **kw)
            else:
                if paras_type == 0:
                    self.resp = self.br.post(
                        url, json=paras, timeout=time_out, **kw)
                elif paras_type == 1:
                    paras = json.dumps(paras)
                    self.resp = self.br.post(
                        url, data=paras, timeout=time_out, **kw)
                else:
                    self.resp = self.br.post(
                        url, data=paras, timeout=time_out, **kw)

            if html_flag:
                # self.resp.encoding = 'utf-8'
                html = self.resp.content
        except Exception, e:
            logger.error(e)
            error = str(e)
            # print error
            #error = 'Crawl Error With Proxy'

        return html, error

    def set_proxy(self, p, https=False):
        self.br.proxies = {
            'https': 'http://' + p,
            'http': 'http://' + p,
        }

    def get_url_of_response(self):
        return self.resp.url

    def get_cookie_str(self):
        return self.resp.cookies

    def add_cookie(self, cookie={}):
        self.br.cookies.update(cookie)

    def get_response(self):
        self.resp.code = self.resp.status_code
        return self.resp

    def add_referer(self, url):
        self.br.headers.update({'Referer': url})

    def add_header(self, headers={}):
        return self.br.headers.update(headers)

    def get_cookie_handle(self):
        pass

    def get_cookie(self, method, url_base, paras={}, paras_type=1, **kw):
        page, _ = self.req(method, url_base, paras={}, paras_type=1, **kw)
        dcookie = requests.utils.dict_from_cookiejar(self.resp.cookies)
        return dcookie, _

    def get_url(self, method, url_base, paras={}, paras_type=1, **kw):
        page, _error = self.req(method, url_base, paras={}, paras_type=1, **kw)

        return self.get_url_of_response(), _error

# cr = Crawler()

if __name__ == '__main__':
    cr = Crawler()
    cr.set_debug(True)
    print cr.get_cookie('get', 'http://www.uctxt.com')
