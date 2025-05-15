APP_NAME=library

build:
	docker compose build --no-cache

start:
	docker compose up -d

restart:
	docker compose restart

stop:
	docker compose down

down:
	docker compose down

prune:
	docker image prune -f

logs:
	docker compose logs -f

upgrade:
	poetry run alembic upgrade head

downgrade:
	poetry run alembic downgrade -1

migrate:
	@read -p "Enter migration message: " msg; \
	poetry run alembic revision --autogenerate -m "$$msg"
