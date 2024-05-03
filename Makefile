PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page-analyzer:app

install:
	poetry install

build:
	poetry build

dev:
	poetry run flask --app page_analyzer:app run

package-install:
	python3 -m pip install --user dist/*.whl

lint:
	poetry run flake8 page_analyzer

check:
	poetry check

init_postgres:
	psql -a -d $(DATABASE_URL) -f database.sql

publish:
	poetry publish --dry-run

