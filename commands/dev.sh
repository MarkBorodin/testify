#!/bin/bash

python manage.py runserver 0:${PORT} --settings="app.settings.${RUN_MODE}"
