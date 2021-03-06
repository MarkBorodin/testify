import os # noqa

from app.settings.components.base import * # noqa
from app.settings.components.database import * # noqa
from app.settings.components.email import * # noqa
from app.settings.components.celery import * # noqa
from app.settings.components.rest import * # noqa


DEBUG = False

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(':')

STATIC_ROOT = '/var/www/testify/static'

MEDIA_ROOT = '/var/www/testify/media'
