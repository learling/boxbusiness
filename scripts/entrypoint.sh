#!/bin/sh

set -e

DJANGO_PORT=8000

python manage.py collectstatic --noinput

uwsgi --socket :$DJANGO_PORT --master --enable-threads --module boxbusiness.wsgi
