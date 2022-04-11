#!/bin/sh

sudo apt install vim
#sudo apt install libapache2-mod-wsgi-py3
sudo apt install python3 python3-venv python3-pip
sudo apt install nginx

python3 -m venv .venv
python3 -m pip install Django
sudo python3 -m pip install uwsgi

#export PATH=$PATH:$HOME/.local/bin

# link nginx to our racing front-end
sudo ln -s /home/pi/chrace/nginx.conf /etc/nginx/sites-enabled/chrace_nginx.conf

# link uwsgi
# create a directory for the vassals
sudo mkdir -p /etc/uwsgi/vassals
# symlink from the default config directory to your config file
sudo ln -s /home/pi/chrace/uwsgi.ini /etc/uwsgi/vassals/chrace_uwsgi.ini
# run the emperor
uwsgi --emperor /etc/uwsgi/vassals --uid www-data --gid www-data

