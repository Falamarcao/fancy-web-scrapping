# Web-Scrapping Tool

VIDEO: <https://loom.com/share/f2733285d0fe49ecad06a923072a30ef>

The project focus on scrapping data from any website using a cluster of headful or headless browsers by using Docker containers running Celery, Redis, Selenium Grid, PostgreSQL and Django Rest Framework.

As a starting point, this project focused on handling web scrapping on <https://www.ingresso.com/> for getting movie theatres (DONE) and movie sessions (not reached yet).

After that initial test and implementation phase, I'm expanding the natural modularity of the project to scrape Twitter's data as <https://twitter.com/search?q=.eth&src=typed_query&f=user>, focusing on extracting accounts with names ending with .eth, and for each Twitter account, recording their full name, username, their bio, followers count and following count.

Easy to adapt on docker-compose file to handle more sessions and browser nodes using Chrome or other available selenium grid browsers. Also, this project can act as a framework for testing websites when configuring the right tasks and database models. As is, I'm also changing the project name and set up to become more generic as a web-scrapping tool.

## Getting Started

## Dependencies

* Docker
* Nginx (only prod)
* Gunicorn (only prod)
* Celery - worker and flower dashboard
* Redis as a broker and result backend for Celery and cache for Django
* Selenium Grid - Hub and Chrome Node
* PostgreSQL or possibly others SQL Databases
* Python
* Packages:
  * **Django**
  * **Django Rest Framework**
  * More Details on [requirements.txt](fancy_web_scrapping/requirements.txt)

## Installing

> Do you have [Docker Installed](https://www.docker.com/)?

For every command you can check the makefile or follow the instructions below:

## Building and Running Development environment (DEV)

* ### BUILD
  
  ````commandline  
  docker-compose build --no-cache
  ````

* ### RUN
  
  ````commandline
  docker-compose up -d
  ````

* ### Django rest framework
  <http://localhost:8000/>
  
  To trigger a web scrapping task OPEN <http://localhost:8000/api/v1/webscraper/1/>

* ### Selenium Grid

  (Optional) To see what is happening inside the container, head to <http://localhost:4444/>.
  The default password for the VNC is "secret".

* ### Celery Flower (Tasks Dashboard)
  
  <http://localhost:5555/>\
  Tasks Dashboard: <http://localhost:5555/tasks>

* ### STOP
  
  ````commandline
  docker-compose down -v
  ````

* ### SUPER USER & DJANGO ADMIN
  
  ```comment
  username: superuser
  password: password
  
  admin url: <http://localhost:8000/admin>
  ```

<!-- ## Building and Running production-ready environment (PROD)

* ### If you have DEV running first take it down

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
  ``` -->

## Help: If you have any problem please e-mail me or contact me on LinkedIn

## Author: Marco Maschio

### [Linkedin](https://linkedin.com/in/marcoantonioms) | [Resume](https://falamarcao.github.io/resume/)

Thank you for your time, and I hope we can talk in near future.

### Common issue with Docker and Windows

```comment
https://stackoverflow.com/questions/51508150/standard-init-linux-go190-exec-user-process-caused-no-such-file-or-directory

Use notepad++, go to edit -> EOL conversion -> change from CRLF to LF.

update: For VScode users: you can change CRLF to LF by clicking on CRLF present on lower right side in the status bar
```
