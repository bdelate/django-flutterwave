dup:
	@docker-compose up -d

build:
	@docker-compose build

migrations:
	@docker-compose run django poetry run ./manage.py makemigrations

migrate:
	@docker-compose run django poetry run ./manage.py migrate

bash:
	@docker-compose run django bash

down:
	@docker-compose down

shell:
	@docker-compose run django poetry run ./manage.py shell

test:
	@docker-compose run django poetry run ./manage.py test djangoflutterwave

test_cov:
	@docker-compose run django poetry run coverage run --source=djangoflutterwave ./manage.py test djangoflutterwave
	@docker-compose run django poetry run coverage html
	@open example/htmlcov/index.html

logs:
	@docker-compose logs -tf django

notebook:
	@docker-compose run -p 8888:8888 django poetry run ./manage.py shell_plus --notebook

import:
	@docker-compose run django poetry run ./manage.py import