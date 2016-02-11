#!/usr/bin/env bash

# Configure apache properly to the /vagrant directory and restart
sudo cp /vagrant/vagrant_bootstrap/apache-000-default.conf /etc/apache2/sites-enabled/000-default.conf
sudo service apache2 restart
