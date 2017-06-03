#!/usr/bin/env bash
nohup stdbuf -oL python -m celery_distribute_crawler.flower | cronolog flower.log &
nohup stdbuf -oL python -m celery_distribute_crawler.server > /dev/null &
#nohup stdbuf -oL celery -A celery_distribute_crawler.celery0 worker -l info -P gevent -E |cronolog ~/celery_log/%Y%m%d/%Y%m%d%H/celery.log.%Y%m%d%H &
#nohup celery -A celery_distribute_crawler.celery0 beat -l info > beat.log &
