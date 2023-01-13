#!/bin/sh

# Wait for Postgres to start running
if [ "$DATABASE" = "postgres" ]; then
  echo "Waiting for postgres..."

  while ! nc -z $SQL_HOST $SQL_PORT; do
    sleep 0.1
  done

  echo "PostgreSQL started"
fi

if [ "$SERVICE_NAME" = "django" ]; then
  echo "DJANGO OPERATIONS STARTED"
  python manage.py flush --no-input
  python manage.py makemigrations
  python manage.py migrate --noinput

  # CREATE GROUPS
  # python manage.py create_groups

  # ADD DATA - fixtures
  python manage.py loaddata sources.json

  # RUN TESTS EVERYTIME
  # python manage.py test fancy_web_scrapping.sources fancy_web_scrapping.movies &> test.log

  # CREATE SUPER USER
  echo "Creating Super User..."
  python manage.py createsuperuser --noinput --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL
fi

history -c

exec "$@"
