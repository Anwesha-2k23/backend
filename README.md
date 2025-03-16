## Issues to be addressed
1. Adding Rate Limiter and concurrent request limiter  
2. Improving Documentation  
3. Faculty register endpoints  
4. Alumini Register endpoints  
5. Bulk mail feature to all users in admin panel  
6. Improve mail format and optimize mail sending  
7. Implement Tests using pytest  
8. Implement OAuth for google and microsoft login  


## What is this Application ? 🤔
This Application is an online registration, user-data management and QR entry framework created for IIT Patna's annual cultural Festival [Awesha](https://anwesha.live/). The primary objective is to provide an easily deployable and highly scalable framework for online registration that anyone can set up easily. It is built on Django and offers a comprehensive set of REST APIs for registration, user data management, entry management and more.

The framework is designed to be flexible and compatible with various client applications. We have successfully used it during our university's annual festival in 2023, serving over 3000 users simultaneously through a web frontend and Android app.

Currently, the framework is compatible with AWS S3, utilising SQL databases.But cloud storage is not compulsory to use ,it can use local storage as well.


## Steps for running 💻
❗ application requires some initial configurations so please read configuration related [files](./anwesha/README.md) first.
- create virtual env --> `virtualenv venv`
- activate venv --> `source -r venv/bin/activate`
- install requirements --> `pip install -r requirements.txt`
- cd into project directory --> `cd anwesha`
- create a .env file in anwesha folder
- add the an .env file in [anwesha/anwesha](./anwesha/anwesha/) to learn more about .env file and configuration read [here](./anwesha/anwesha/README.md).
- run the server --> `python manage.py runserver`

## Host using Docker 🐳

- use docker build command to build the image ( ❗ please note that you should run this command in 📁 root directory where docker file is present ) )
```
docker build --tag <image_name>:latest .
```
- run the image either from docker dashboard or using cli
```
docker run --name <image_name> -d -p 8000:8000 <imagge_name>:latest

```

## File structure 🗄️

- [anwesha](./anwesha/) :- This is the source code for all the apis and configurations required for backend.
- [Dockerfile](./Dockerfile) :- file containing instructions to build Docker Images.
- [docker-compose.yml](./docker-compose.yml) :- configuration file for running multiple containers at once, it will be useful in hosting multiple docker containers with backend on server.
- [requirements.txt](./requirements.txt) :- it contains all the pacakges required by the project. ❗**Whenever a new library is added in the project please update the requirement.txt file.**
