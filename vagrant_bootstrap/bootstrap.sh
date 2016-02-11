#!/usr/bin/env bash

# First we update all packages to make sure everything is good to go
apt-get update

# Installing apache2
echo -e "************* INSTALLING APACHE2 *************"
apt-get install -y apache2

# Installing Nginx
apt-get install -y nginx

# Installing helpers for PHP install
echo -e "************* UPDATING PHP REPOSITORY *************"
apt-get install -y python-software-properties build-essential
add-apt-repository -y ppa:ondrej/php5 # This is more up to date than the ubuntu one
apt-get update	

# Installing PHP for phpmyadmin
echo -e "************* INSTALLING PHP *************"
apt-get install -y php5-common php5-dev php5-cli php5-fpm
echo -e "************* INSTALLING EXTENSIONS *************"
apt-get install -y curl php5-curl php5-gd php5-mcrypt php5-mysql

# Installing debconf-utils for MySQL install
echo -e "************* INSTALLING DEBCONF-UTILS *************"
apt-get install -y debconf-utils

# TODO
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
echo -e "************* INSTALLING PIP3 *************"
apt-get -y install python3-pip

# Setting up the virtualenv directory
if [ ! -d /vagrant/square_connect/square_connect/virt_env ]; then
	mkdir /vagrant/square_connect/square_connect/virt_env
fi

# Installing virtualenv if necessary
if ! type virtualenv >/dev/null 2>&1; then
	echo -e "************* INSTALLING VIRTUALENV *************"
	pip3 install virtualenv
	virtualenv /vagrant/square_connect/square_connect/virt_env --always-copy
fi

# Activate the virtualenv for the next couple installs
source /vagrant/square_connect/square_connect/virt_env/bin/activate

# Install django
if ! type django-admin >/dev/null 2>&1; then
	echo -e "************* INSTALLING DJANGO *************"
	pip3 install django
fi

# Install MySQL
if ! type mysql >/dev/null 2>&1; then
	echo -e "************* CONFIGURING MYSQL INSTALL *************"
	echo "mysql-server mysql-server/root_password password S89ydkH6rnwh9GNm2Um" | debconf-set-selections
	echo "mysql-server mysql-server/root_password_again password S89ydkH6rnwh9GNm2Um" | debconf-set-selections
	echo "INSTALLING MYSQL..."
	apt-get install -y mysql-server

	
	# Installing mysqlclient
	echo -e "************* INSTALLING MYSQLCLIENT HEADERS *************"
	apt-get install -y libmysqlclient-dev
	echo -e "************* INSTALLING PYTHON 3 DEV *************"
	apt-get install -y python3-dev
	echo -e "************* INSTALLING MYSQLCLIENT *************"
	pip3 install mysqlclient

	# Run the MySQL configuration script
	chmod +x /vagrant/vagrant_bootstrap/mysql_configure.sh
	/vagrant/vagrant_bootstrap/mysql_configure.sh
fi

# Virtualenv based installed finished, deactive
deactivate

# Enable apache_configure.sh to run 
chmod +x /vagrant/vagrant_bootstrap/apache_configure.sh
	
# Configure apache
echo -e "************* CONFIGURING APACHE *************"
/vagrant/vagrant_bootstrap/apache_configure.sh

# Install git for convenience
echo -e "************* INSTALLING GIT *************"
apt-get -y install git

# Apply database migrations
chmod +x /vagrant/vagrant_bootstrap/make_migrations.sh
/vagrant/vagrant_bootstrap/make_migrations.sh

# Make the half hourly cron tasks script runable
chmod +x /vagrant/square_connect/square_connect/half_hour_cron.sh

# Set the crontab for tasks that run every 30 minutes
(crontab -l 2>/dev/null; echo "*/30 * * * * /vagrant/square_connect/square_connect/half_hour_cron.sh") | crontab -

echo -e "THE SETUP PROCESS HAS COMPLETED.\nMAKE SURE TO ADDRESS ANY ERROR MESSAGES."
echo -e "\a\a\a\a"
