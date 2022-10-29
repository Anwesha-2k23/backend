## Steps

- create virtual env --> `virtualenv venv`
- activate venv --> `source -r venv/bin/activate`
- install requirements --> `pip install -r requirements.txt`
- install Gmail-Auth package --> `pip install ./Gmail_Auth0-0.1.tar.gz`
- cd into project directory --> `cd anwesha`
- run the server --> `python manage.py runserver`

## Some instructions to follow

- use Snake_case not CamelCase
- Use comments
- whenever you use some new dependency always add that to requirement.txt
  - use `pip freeze > requirements.txt`
