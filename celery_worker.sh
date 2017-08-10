#celery worker -l INFO -c 100 -A celery_worker.celery
#celery beat -l INFO -c 100 -A celery_worker.celery
#celery -A tasks worker --loglevel=info --beat

celery worker -l INFO -c 100 -A celery_worker.celery --beat

