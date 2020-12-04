from celery.schedules import crontab

# CELERY_BROKER_URL = 'amqp://rabbitmq'

CELERY_BROKER_URL = 'redis://redis:6379'
CELERY_RESULT_BACKEND = 'redis://redis:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'

CELERY_BEAT_SCHEDULE = {

    'motivation_letter': {
        'task': 'testify.tasks.motivation_letter',
        'schedule': crontab(minute='0', hour='9'),
    },
}
