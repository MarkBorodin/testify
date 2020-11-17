from celery.schedules import crontab

CELERY_BROKER_URL = 'amqp://rabbitmq'

CELERY_BEAT_SCHEDULE = {
    'parse': {
        'task': 'testsuite.tasks.cleanup_outdated_testruns',
        'schedule': crontab(minute='*/1'),
    },
}
