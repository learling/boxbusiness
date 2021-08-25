#!/bin/sh

set -e

python manage.py collectstatic --noinput

uwsgi --socket :8000 --master --enable-threads --module boxbusiness.wsgi

# https://www.youtube.com/watch?v=nh1ynJGJuT8

# sudo docker-compose -f docker-compose-deploy.yml up --build
# before that I had to run:
# sudo aa-remove-unknown