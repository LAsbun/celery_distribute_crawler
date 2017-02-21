#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/2/21 下午6:48
# @Author  : sws
# @Site    : 
# @File    : sync_git.py
# @Software: PyCharm

import os

pwd_path = os.getcwd()

git_list = [
    'git@localhost:/srv/celery_distribute_crawler.git',
]

for git in git_list:
    os.system(
        'cd {0}; git clone {1}'.format(pwd_path, git)
    )