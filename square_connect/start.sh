#!/bin/bash
cd /home/thecorp/django/howitzer/square_connect/square_connect/

virt_env/bin/gunicorn -w 8 -b 127.0.0.1:9051 --log-file /tmp/howitzerlog -D square_connect.wsgi:application

