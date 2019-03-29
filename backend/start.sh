#!/usr/bin/env bash
sed -i -e 's/$PORT/'"$PORT"'/g' /etc/nginx/conf.d/default.conf && service nginx start
uwsgi --ini uwsgi.ini