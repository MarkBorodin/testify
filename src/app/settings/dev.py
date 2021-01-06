from app.settings.components.base import * # noqa
from app.settings.components.database import * # noqa
from app.settings.components.dev_tools import * # noqa
from app.settings.components.email import * # noqa
from app.settings.components.celery import * # noqa
from app.settings.components.rest import * # noqa


DEBUG = True
ALLOWED_HOSTS = ['*']

STATIC_ROOT = '/var/www/testify/static'

MEDIA_ROOT = '/var/www/testify/media'
