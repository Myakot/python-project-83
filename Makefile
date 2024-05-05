install:
	poetry install

build:
	./build.sh

lint:
	poetry run flake8 page_analyzer

dev:
	poetry run flask --app page_analyzer:app run

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

init_postgres:
	psql -a -d $(DATABASE_URL) -f database.sql

publish:
	poetry publish --dry-run

