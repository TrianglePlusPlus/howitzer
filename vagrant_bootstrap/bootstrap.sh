#!/usr/bin/env bash

# First we update all packages to make sure everything is good to go
apt-get update

apt-get install -y apache2

if ! [ -L /var/www ]; then
	rm -rf /var/www
	ln -s /vagrant /var/www
fi

apt-get -y install python3-pip

# Setting up the virtualenv with Django
if [ ! -d /vagrant/square_connect/square_connect/virt_env ]; then
	pip3 install virtualenv
	mkdir /vagrant/square_connect/square_connect/virt_env
	virtualenv /vagrant/square_connect/square_connect/virt_env --always-copy
	source /vagrant/square_connect/square_connect/virt_env/bin/activate
	pip install django
	deactivate
fi

chmod +x /vagrant/vagrant_bootstrap/apache_configure.sh
	
# Configure apache so it doesn't freak out
/vagrant/vagrant_bootstrap/apache_configure.sh

# Install git for convenience
apt-get -y install git
