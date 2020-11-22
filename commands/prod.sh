#!/bin/bash

gunicorn -w ${WORKERS} -b 0:${PORT} app.wsgi:application --log-level=${LOG_LEVEL}
