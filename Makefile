install:
	poetry install

build:
	poetry build

lint:
	poetry run flake8 page-analyzer

dev:
	poetry run flask --app page-analyzer:app run

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page-analyzer:app

init_postgres:
	psql -a -d $(DATABASE_URL) -f database.sql

publish:
	poetry publish --dry-run

