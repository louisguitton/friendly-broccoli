from celery.schedules import crontab


CELERY_IMPORTS = ('app.upload.tasks.test')
CELERY_TASK_RESULT_EXPIRES = 30
CELERY_TIMEZONE = 'UTC'

CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERYBEAT_SCHEDULE = {
    'test-celery': {
        'task': 'app.upload.tasks.test.print_hello',
        # Every minute
        'schedule': crontab(minute="*"),
    }
}