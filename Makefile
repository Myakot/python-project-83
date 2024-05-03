install:
	poetry install

dev:
	poetry run flask --app page_analyzer:app run

# Эта команда запускает веб-сервер по адресу *http://localhost:8000*,
# если в переменных окружения не указан порт, необходимый для деплоя
PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app