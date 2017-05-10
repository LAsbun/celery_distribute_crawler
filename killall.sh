#!/usr/bin/env bash
ps aux|grep "python -m flower"|grep -v grep|tee -a worker_restart.log
ps aux|grep "python -m flower"|grep -v grep|cut -c 10-15|xargs kill -9
ps aux|grep "python -m celery_distribute_crawler.server"|grep -v grep|tee -a worker_restart.log
ps aux|grep "python -m celery_distribute_crawler.server"|grep -v grep|cut -c 10-15|xargs kill -9
pkill -9 celery
echo "restart_all done"