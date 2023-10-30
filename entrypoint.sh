#!/bin/sh

mkdir /var/log/interview
chmod 777 /var/log/interview


gunicorn interview.wsgi -b 0.0.0.0:8000 -e PROJECT_ENV="$PROJECT_ENV" --timeout=90 --workers=2 --worker-class=gevent