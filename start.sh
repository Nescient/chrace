#!/bin/sh

# add me to /etc/rc.local

/usr/local/bin/uwsgi --emperor /etc/uwsgi/vassals --uid www-data --gid www-data --daemonize /var/log/uwsgi-emperor.log

# python3 manage.py runserver 0:8081

