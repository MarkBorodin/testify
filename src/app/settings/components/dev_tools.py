from app.settings.components.base import INSTALLED_APPS, MIDDLEWARE

INSTALLED_APPS += [
    'debug_toolbar',
    'django_extensions',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]


INTERNAL_IPS = [
    # ...
    '127.0.0.1',
    # ...
]
