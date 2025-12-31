# pull the official base image
FROM python:3.8.13-slim-buster

# set work directory
WORKDIR /usr/src/backend

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip 
COPY ./requirements.txt /usr/src/backend
RUN pip install -r requirements.txt

# copy project
COPY . /usr/src/backend/

EXPOSE 8080

WORKDIR /usr/src/backend/anwesha

# Run migrations, collect static files, then start gunicorn (for Cloud Run)
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn anwesha.wsgi:application --bind 0.0.0.0:8080 --workers 4"]

