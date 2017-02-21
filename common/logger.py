#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17/1/7 下午5:03
# @Author  : sws
# @Site    : 
# @File    : logger.py
# @Software: PyCharm

import logging
import logging.config

#配置日志
FORMAT = "%(asctime)-15s %(threadName)s %(filename)s:%(lineno)d %(levelname)s %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)

logger = logging.getLogger('crawlLog')
logger.setLevel(logging.NOTSET)