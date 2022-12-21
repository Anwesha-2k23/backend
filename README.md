## Steps

- create virtual env --> `virtualenv venv`
- activate venv --> `source -r venv/bin/activate`
- install requirements --> `pip install -r requirements.txt`
- install Gmail-Auth package --> `pip install ./Gmail_Auth0-0.1.tar.gz`
- cd into project directory --> `cd anwesha`
- create a .env file in anwesha folder 
- add the following to .env file
```
  SECRET_KEY='django-insecure-fp*7b=2$ei(yig67kp1q6wgr+wsk45nx_218x7)n!$l)gba*ox'
  DEBUG=TRUE
```
- run the server --> `python manage.py runserver`

## Some instructions to follow

- use Snake_case not CamelCase
- Use comments
- whenever you use some new dependency always add that to requirement.txt
  - use `pip freeze > requirements.txt`
