#!/usr/bin/env bash
nohup celery -A celery_distribute_crawler.celery0 beat -l info > beat.log &