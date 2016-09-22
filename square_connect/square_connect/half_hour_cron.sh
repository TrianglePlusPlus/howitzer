#!/bin/bash
# USE THIS FILE TO SCHEDULE TASKS THAT RUN EVERY 30 MINUTES

# SPOILAGE DATA PULLS
# Start the virtual environment
source /home/thecorp/django/howitzer/square_connect/square_connect/virt_env/bin/activate
# Run the pull command
python /home/thecorp/django/howitzer/square_connect/square_connect/manage.py get_recent_spoilage_transactions
# Close the virtual environment
deactivate
