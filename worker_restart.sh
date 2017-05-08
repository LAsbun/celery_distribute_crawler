#!/usr/bin/env bash
ps aux|grep "celery -A celery_distribute_crawler.celery0 worker"|grep -v grep|tee -a worker_restart.log
ps aux|grep "celery -A celery_distribute_crawler.celery0 worker"|grep -v grep|cut -c 10-15|xargs kill -9
echo "restart_all done"
cd ~/dis; . bin/activate;
sh celery_distribute_crawler/worker_start.sh