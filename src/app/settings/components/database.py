import os


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DB_NAME'],
        'HOST': os.environ['DB_HOST'],
        'USER': os.environ['DB_USER'],
        'PORT': os.environ['DB_PORT'],
        'PASSWORD': os.environ['DB_PASSWORD'],
    }
}
