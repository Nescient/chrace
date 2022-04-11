#!/bin/sh

sudo apt install vim
#sudo apt install libapache2-mod-wsgi-py3
sudo apt install python3 python3-venv python3-pip
sudo apt install nginx

python3 -m venv .venv
python3 -m pip install Django
python3 -m pip install uwsgi

#export PATH=$PATH:$HOME/.local/bin

# link nginx to our racing front-end
sudo ln -s /home/pi/chrace/racing/racing_nginx.conf /etc/nginx/sites-enabled/racing_nginx.conf

# link uwsgi
# create a directory for the vassals
sudo mkdir -p /etc/uwsgi/vassals
# symlink from the default config directory to your config file
sudo ln -s /home/pi/chrace/racing/racing_uwsgi.ini /etc/uwsgi/vassals/
# run the emperor
uwsgi --emperor /etc/uwsgi/vassals --uid www-data --gid www-data

