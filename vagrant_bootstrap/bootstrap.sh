#!/usr/bin/env bash

apt-get update
apt-get install -y apache2

if ! [ -L /var/www ]; then
	rm -rf /var/www
	ln -s /vagrant /var/www
fi

/vagrant/vagrant_bootstrap/apache_configure.sh
