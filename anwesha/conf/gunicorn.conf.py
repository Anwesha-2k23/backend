wsgi_app = 'anwesha.wsgi'
bind = '0.0.0.0:8000'
workers = 4
loglevel = "debug"
keep_alive = 60
threads = 4
pid = './conf/gunicorn.pid'
access_logfile = './conf/gunicorn-access.log'
capture_output = True
# daemon = True
