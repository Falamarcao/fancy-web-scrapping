# pull official base image
FROM python:3.9.6-alpine

# set work directory
WORKDIR /usr/src/movie_listing

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

# Postgree CLient (only dev environment)
RUN apk add postgresql-client

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/movie_listing/entrypoint.sh
RUN chmod +x /usr/src/movie_listing/entrypoint.sh

# copy project
COPY .. .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/movie_listing/entrypoint.sh"]

RUN unset DJANGO_SUPERUSER_USERNAME && unset DJANGO_SUPERUSER_EMAIL && unset DJANGO_SUPERUSER_PASSWORD
