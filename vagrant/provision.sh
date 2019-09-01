#!/usr/bin/env bash

export DEBIAN_FRONTEND="noninteractive"

apt update
apt upgrade -y

apt install python3 python3-pip python3-dev python3-venv -y

python3 -m venv /home/vagrant/env
/home/vagrant/env/bin/pip install -r /vagrant/requirements.txt
/home/vagrant/env/bin/python /vagrant/manage.py migrate
/home/vagrant/env/bin/python /vagrant/manage.py flush --no-input
/home/vagrant/env/bin/python /vagrant/manage.py loaddata /vagrant/vagrant/db.json
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', '', 'oinkoinkboom')" | /home/vagrant/env/bin/python /vagrant/manage.py shell
/home/vagrant/env/bin/python /vagrant/manage.py runserver 0.0.0.0:8080 &
