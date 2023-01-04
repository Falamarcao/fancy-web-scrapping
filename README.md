# Assessment: Movie Listing WebScrapping

## Getting Started

## Dependencies

* Docker
* Nginx (prod)
* Gunicorn (prod)
* PostgreSQL or possibly others SQL Databases
* Selenium Grid
* Python
* Packages:
  * **Django**
  * **Django Rest Framework**
  * More Details on [requirements.txt](movie_listing/requirements.txt)

## Installing

> Do you have [Docker Installed](https://www.docker.com/)?

## Selenium Grid

(Optional) To see what is happening inside the container, head to <http://localhost:4444/?autoconnect=1&resize=scale&password=secret>.

## NOTES About Both Enviroments - PROD & DEV

When web container start, on the first time, the follow commands are executed automatically:

```commandline
    python manage.py flush --no-input
    python manage.py makemigrations
    python manage.py migrate --noinput
    python manage.py loaddata users.json posts.json reposts.json quote-postings.json
```

Getting ready the database and loading some example data, so NO NEED TO EXECUTE the commands ABOVE.\
They are included on entrypoints scripts: [entrypoint.sh](movie_listing/entrypoint.sh) and [entrypoint.prod.sh](movie_listing/entrypoint.prod.sh).

But if wanted on your own risk it's possible to execute using:

```commandline
docker-compose -f docker-compose.prod.yml exec web python manage.py flush --noinput
docker-compose -f docker-compose.prod.yml exec web python manage.py makemigrations
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput
docker-compose -f docker-compose.prod.yml exec web python manage.py loaddata customers.json staff.json sources.json movies.json
```

**INFO: we are not putting migrations on version control because this is a fresh start project.**

## Building and Running Development environment (DEV)

* ### BUILD
  
  ````commandline  
  docker-compose build --no-cache
  ````

* ### RUN
  
  ````commandline
  docker-compose up -d
  ````

* ### STOP
  
  ````commandline
  docker-compose down -v
  ````

* ### OPEN <http://localhost:8000/>

* ### SUPER USER & DJANGO ADMIN
  
  ```comment
  username: superuser
  password: password
  
  admin url: http://localhost:8000/admin
  ```

## Building and Running production-ready environment (PROD)

* ### If you have DEV running first take it down.

  ````commandline
  docker-compose down -v
  ````

* ### And then BUILD & RUN
  
  ````commandline
  docker-compose -f docker-compose.prod.yml up -d --build
  ````

* ### FINALLY OPEN http://localhost:1337/
  
* STOP
  
  ````commandline
  docker-compose -f docker-compose.prod.yml down -v
  ````

* ### USERS & DJANGO ADMIN
  
  ```comment
  username: superuser
  password: password
  
  username: staff
  password: password
  
  admin url: http://localhost:8000/admin
  ```

## Automated Tests

On DEV Environment tests are executed on every container start see [entrypoint.sh](movie_listing/entrypoint.sh) and a [test.log](movie_listing/test.log) file is generated,\
to run on demand see the commands bellow:

* ### DEV
  
  ````commandline
  docker-compose exec web python manage.py test movie_listing.sources movie_listing.movies
  ````

* ### PROD
  
  ````commandline
  docker-compose -f docker-compose.prod.yml exec web python manage.py test movie_listing.sources movie_listing.movies
  ````

## Help: If you have any problem please e-mail me or contact me on LinkedIn.

### Common issue

```comment
Use notepad++, go to edit -> EOL conversion -> change from CRLF to LF.

update: For VScode users: you can change CRLF to LF by clicking on CRLF present on lower right side in the status bar

https://stackoverflow.com/questions/51508150/standard-init-linux-go190-exec-user-process-caused-no-such-file-or-directory
```

## Author: Marco Maschio

### [Linkedin](https://linkedin.com/in/marcoantonioms) | [Resume](https://falamarcao.github.io/resume/)

Thank you for your time, and I hope we can talk in near future.
