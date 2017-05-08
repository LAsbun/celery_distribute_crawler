#!/usr/bin/env bash
cd celery_distribute_crawler; nohup python -m flower > /dev/null &
cd ..;
nohup stdbuf -oL celery -A celery_distribute_crawler.celery0 worker -l info -P gevent -c 500 |cronolog ~/celery_log/%Y%m%d/%Y%m%d%H/celery.log.%Y%m%d%H &
nohup celery -A celery_distribute_crawler.celery0 beat -l info > beat.log &
