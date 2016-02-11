# Start the virtual environment if it is not active
if ! type djangoadmin >/dev/null 2>&1; then
	source /vagrant/square_connect/square_connect/virt_env/bin/activate
fi
echo -e "\n************** Preparing migrations **************\n"
python /vagrant/square_connect/square_connect/manage.py makemigrations
echo -e "\n************** Performing migrations **************\n"
python /vagrant/square_connect/square_connect/manage.py migrate
