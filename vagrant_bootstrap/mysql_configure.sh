# Call .sql scripts from here
# Login to MySQL as root and create the database to use
mysql --user=root --password=S89ydkH6rnwh9GNm2Um --execute="CREATE DATABASE square CHARACTER SET utf8"

# Run the sql setup commands
mysql --user=root --password=S89ydkH6rnwh9GNm2Um "square" < "/vagrant/vagrant_bootstrap/setup.sql" 