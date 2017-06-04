#!/usr/bin/env bash
nohup stdbuf -oL celery -A celery_distribute_crawler.celery0 worker -l info -P eventlet |cronolog ~/celery_log/%Y%m%d/%Y%m%d%H/celery.log.%Y%m%d%H &
