#!/usr/bin/env bash

# First we update all packages to make sure everything is good to go
apt-get update

# Installing apache2
echo "INSTALLING apache2..."
apt-get install -y apache2

# Installing Nginx
apt-get install -y nginx

# Installing helpers for PHP install
echo "UPDATING PHP REPOSITORY..."
apt-get install -y python-software-properties build-essential
add-apt-repository -y ppa:ondrej/php5
apt-get update	

# Installing PHP for phpmyadmin
echo "INSTALLING PHP..."
apt-get install -y php5-common php5-dev php5-cli php5-fpm
echo "INSTALLING EXTENSIONS..."
apt-get install -y curl php5-curl php5-gd php5-mcrypt php5-mysql

# Installing debconf-utils for MySQL install
apt-get install -y debconf-utils

# Installing MySQL
echo "CONFIGURING MYSQL INSTALL..."
echo "mysql-server mysql-server/root_password password S89ydkH6rnwh9GNm2Um" | debconf-set-selections
echo "mysql-server mysql-server/root_password_again password S89ydkH6rnwh9GNm2Um" | debconf-set-selections
echo "INSTALLING MYSQL..."
apt-get install -y mysql-server


# THIS DOESN'T WORK CORRECTLY, TODO
# Installing PHPMyAdmin
#echo "phpmyadmin phpmyadmin/dbconfig-install boolean true" | debconf-set-selections
#echo "phpmyadmin phpmyadmin/app-password-confirm password bkOpQa0g7d" | debconf-set-selections
#echo "phpmyadmin phpmyadmin/mysql/admin-pass password bkOpQa0g7d" | debconf-set-selections
#echo "phpmyadmin phpmyadmin/mysql/app-pass password bkOpQa0g7d" | debconf-set-selections
#echo "phpmyadmin phpmyadmin/reconfigure-webserver multiselect none" | debconf-set-selections
#apt-get install -y phpmyadmin


# Restructuring for serving web content

if ! [ -L /var/www ]; then
	rm -rf /var/www
	ln -s /vagrant /var/www
fi

# Installing pip
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
