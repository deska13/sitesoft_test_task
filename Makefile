install:
	poetry install

install-hooks:
	poetry run pre-commit install

format-lint:
	poetry run pre-commit run --all-files

version:
	@poetry version $(v)
	@git add pyproject.toml
	@git commit -m "v$$(poetry version -s)"
	@git tag v$$(poetry version -s)
	@git push
	@git push --tags
	@poetry version

build:
	docker build . -f docker/dockerfile -t habr-parser

env:
	cp config/.env.template .env

up-dev:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d

up-prod:
	docker compose -f docker-compose.yml up -d

stop:
	docker compose -f docker-compose.yml stop

# migrations

makemigration-docker:
	docker compose exec parser_api bash -c 'python manage.py makemigrations'

migrate-docker:
	docker compose exec parser_api bash -c 'python manage.py migrate'
