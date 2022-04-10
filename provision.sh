#!/bin/sh

sudo apt install vim
#sudo apt install libapache2-mod-wsgi-py3
sudo apt install python3 python3-venv python3-pip
sudo apt install nginx

python3 -m venv .venv
python3 -m pip install Django
python3 -m pip install uwsgi
