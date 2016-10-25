# USE THIS FILE TO SCHEDULE TASKS THAT RUN EVERY 30 MINUTES

# REPORT DATA PULLS
# Start the virtual environment
. /vagrant/square_connect/square_connect/virt_env/bin/activate
# Run the pull command
python /vagrant/square_connect/square_connect/manage.py get_recent_transactions All
# Close the virtual environment
deactivate
