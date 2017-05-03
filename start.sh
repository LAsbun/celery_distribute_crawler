celery flower --config celery_distribute_crawler/celeryconfig.py &
sleep 5;
nohup celery -A celery_distribute_crawler.celery0 worker -l info > celery.log &
sleep 5;
nohup celery -A celery_distribute_crawler.celery0 beat -l info > beat.log &