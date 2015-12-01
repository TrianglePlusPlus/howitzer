#!/usr/bin/env bash

# First we update all packages to make sure everything is good to go
apt-get update

# Installing apache2
echo "INSTALLING apache2..."
apt-get install -y apache2

# Installing Nginx
apt-get install nginx -y

# Installing helpers for PHP install
echo "UPDATING PHP REPOSITORY..."
apt-get install python-software-properties build-essential -y
add-apt-repository ppa:ondrej/php5 -y
apt-get update	

# Installing PHP for phpmyadmin
echo "INSTALLING PHP..."
apt-get install php5-common php5-dev php5-cli php5-fpm -y
echo "INSTALLING EXTENSIONS..."
apt-get install curl php5-curl php5-gd php5-mcrypt php5-mysql -y

# Installing debconf-utils for MySQL install
apt-get isntall debconf-utils -y

# Installing MySQL
echo "CONFIGURING MYSQL INSTALL..."
debconf-set-selections <<< "mysql-server mysql-server/root_password password S89ydkH6rnwh9GNm2Um"
debconf-set-selections <<< "mysql-server mysql-server/root_password_again password S89ydkH6rnwh9GNm2Um"
echo "INSTALLING MYSQL..."
apt-get install mysql-server -y

# Installing PHPMyAdmin
debconf-set-selections <<< "phpmyadmin phpmyadmin/dbconfig-install boolean true"
debconf-set-selections <<< "phpmyadmin phpmyadmin/app-password-confirm password bkOpQa0g7d"
debconf-set-selections <<< "phpmyadmin phpmyadmin/mysql/admin-pass password bkOpQa0g7d"
debconf-set-selections <<< "phpmyadmin phpmyadmin/mysql/app-pass password bkOpQa0g7d"
debconf-set-selections <<< "phpmyadmin phpmyadmin/reconfigure-webserver multiselect none"
apt-get install phpmyadmin -y

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
