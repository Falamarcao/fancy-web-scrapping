# DEVELOPMENT ENVIRONMENT

create-conda-env: # (optional) helps code autocomplete. Conda allows to use specific python version.
	conda env create --prefix=./.env --file environment.dev.yml

build-dev:
	docker-compose build --no-cache

up-dev: # [build-dev] must be executed before
	docker-compose up -d

run-dev:
	make build-dev && make up-dev && open-tabs-dev

test-dev: # [up-dev or run-dev] must be executed before.
	docker-compose exec django python manage.py test fancy_web_scrapping.webscraper.spiders.navigator

stop-dev: # (optional) you can manage using the Docker Desktop GUI
	docker-compose down -v

open-tabs-dev: # (optional) runs on the browser Django, Celery Flower, and Selenium Grid
	python -m webbrowser http://localhost:8000/
	python -m webbrowser http://localhost:5555/tasks
	python -m webbrowser http://localhost:4444/

# PRODUCTION-LIKE ENVIRONMENT

run-prod:
	docker-compose -f docker-compose.prod.yml up -d --build && open-tabs-prod

stop-prod:
	docker-compose -f docker-compose.prod.yml down -v

open-tabs-prod: # (optional) runs on the browser Django, Celery Flower, and Selenium Grid
	python -m webbrowser http://localhost:1337/
	python -m webbrowser http://localhost:5555/tasks
	python -m webbrowser http://localhost:4444/
