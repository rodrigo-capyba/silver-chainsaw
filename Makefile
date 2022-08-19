ARG := $(wordlist 2, $(words $(MAKECMDGOALS)), $(MAKECMDGOALS))
$(eval $(ARG):;@true)

perms:
	sudo chown -hR ${USER}:${USER} .

build:
	docker-compose build

up:
	docker-compose up

enter:
	docker-compose exec $(ARG) bash

setup_install:
	bash scripts/setup-install.sh

setup_venv:
	bash scripts/setup-venv.sh

startapp:
	bash scripts/start-app.sh $(ARG)

run:
	bash scripts/docker-run.sh $(ARG)

migrations:
	bash scripts/docker-run.sh python manage.py makemigrations $(ARG)

migrate:
	bash scripts/docker-run.sh python manage.py migrate

seed:
	bash scripts/docker-run.sh python manage.py runscript seed

reset_schema:
	bash scripts/docker-run.sh python manage.py reset_schema

shell:
	bash scripts/docker-run.sh python manage.py shell_plus

collectstatic:
	bash scripts/docker-run.sh python manage.py collectstatic

messages:
	bash scripts/docker-run.sh django-admin makemessages -l pt_BR --ignore venv

compilemessages:
	bash scripts/docker-run.sh django-admin compilemessages -l pt_BR

generate_schema:
	mkdir -p tmp/docs
	bash scripts/docker-run.sh python manage.py generateschema --format openapi-json > docs/openapi.json

test:
	bash scripts/docker-run.sh pytest -n 4

test_create_db:
	bash scripts/docker-run.sh pytest -n 4 --create-db

coverage:
	bash scripts/docker-run.sh pytest -n 4 --cov=apps

coverage_html:
	bash scripts/docker-run.sh pytest -n 4 --cov=apps --cov-report html
	google-chrome htmlcov/index.html

total_reset: reset_schema migrate seed
