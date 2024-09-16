run:
	make migrate && poetry run uvicorn src.__main__:app --host 0.0.0.0 --port 8080 --reload
db:
	docker compose up -d --build --remove-orphans db
up_locally:
	docker compose up -d --build --remove-orphans
build_backend:
	docker build -t app .
models:
	sqlacodegen_v2 postgresql://postgres:postgres@localhost/tender --outfile models.py
format:
	ruff format src/
lint:
	ruff check src/ --fix
insert: ##Insert exmaple users and organizations
	poetry run python src/db/insert.py
migrate: ##Insert exmaple users and organizations
	poetry run sh -c "cd src/db && alembic upgrade head"