# USE THIS FILE TO SCHEDULE TASKS THAT RUN EVERY DAY

# SPOILAGE REPORT EMAILS
# Start the virtual environment
. /home/thecorp/django/howitzer/square_connect/square_connect/virt_env/bin/activate
# Run the email command
python /home/thecorp/django/howitzer/square_connect/square_connect/manage.py send_emails
# Close the virtual environment
deactivate
