dup:
	@docker-compose up -d

build:
	@docker-compose build

migrations:
	@docker-compose run django poetry run ./example/manage.py makemigrations

migrate:
	@docker-compose run django poetry run ./example/manage.py migrate

bash:
	@docker-compose run django bash

down:
	@docker-compose down

shell:
	@docker-compose run django poetry run ./example/manage.py shell

notebook:
	@docker-compose run -p 8888:8888 django poetry run ./example/manage.py shell_plus --notebook

test:
	@docker-compose run django poetry run ./example/manage.py test

test_cov:
	@docker-compose run django poetry run coverage run --source='.' example/manage.py test
	@docker-compose run django poetry run coverage html
	@open djangorave/htmlcov/index.html

compress:
	@docker-compose run django poetry run ./example/manage.py compress

logs:
	@docker-compose logs -tf django