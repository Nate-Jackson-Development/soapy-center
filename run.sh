sudo gunicorn -t 60 --threads 2 -w 4 -b 0.0.0.0:443 --certfile=/var/local/SSL/naed3r.xyz.pem --keyfile=/var/local/SSL/naed3r.xyz.key api:app
