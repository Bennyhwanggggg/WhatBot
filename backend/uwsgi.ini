[uwsgi]
module = app:app
uid = www-data
gid = www-data
master = true
processes = 4
http-socket = :$(PORT)
socket = /tmp/uwsgi.socket
chmod-sock = 664
vacuum = true
die-on-term = true