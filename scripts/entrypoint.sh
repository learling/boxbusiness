#!/bin/sh

set -e

DJANGO_PORT=8000

#TODO: Get testing work inside of docker
##This is not working:
#GV=v0.29.1
#wget "https://github.com/mozilla/geckodriver/releases/download/$GV/geckodriver-$GV-linux64.tar.gz"
#tar xvzf geckodriver-$GV-linux64.tar.gz
#chmod +x geckodriver
#sudo cp geckodriver /usr/local/bin/

python manage.py collectstatic --noinput
uwsgi --socket :$DJANGO_PORT --master --enable-threads --module boxbusiness.wsgi
