#!/bin/sh

cd /home/nathan/soapy-center/
sudo gunicorn -t 60 --threads 2 -w 4 -b 0.0.0.0:9999 --certfile=/var/local/SSL/naed3r.xyz.pem --keyfile=/var/local/SSL/naed3r.xyz.key api:app
