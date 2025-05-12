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

logs:
	docker compose logs -f

create-db:
	poetry run ./scripts/create_db.py
