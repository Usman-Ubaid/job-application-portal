run:
	python manage.py runserver

migrate:
	python manage.py makemigrations
	python manage.py migrate

superuser:
	python manage.py createsuperuser

shell:
	python manage.py shell

install:
	poetry install

black:
	black .

start-db:
	docker start job-portal_db

test:
	poetry run pytest

test-users:
	poetry run pytest users/tests/

test-jobs:
	poetry run pytest jobs/tests/

test-companies:
	poetry run pytest companies/tests/
