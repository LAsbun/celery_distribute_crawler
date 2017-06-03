#!/usr/bin/env bash
ps aux|grep "celery -A celery_distribute_crawler.celery0 beat -l info"|grep -v grep
ps aux|grep "celery -A celery_distribute_crawler.celery0 beat -l info"|grep -v grep|cut -c 10-15|xargs kill -9