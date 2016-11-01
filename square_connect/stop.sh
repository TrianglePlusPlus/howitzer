#!/bin/bash
kill -9 `ps -aux | grep gunicorn | grep square_connect.wsgi:application | awk '{ print $2 }'` 
