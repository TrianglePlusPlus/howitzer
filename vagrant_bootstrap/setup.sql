/*
	This file is a place to add users and configure privileges
	Additionally universal setup actions can be placed here
*/
CREATE USER 'django'@'localhost' IDENTIFIED BY '19djangomysqlpassword72';
GRANT ALL PRIVILEGES ON square.* TO django@localhost IDENTIFIED BY '19djangomysqlpassword72';
FLUSH PRIVILEGES;