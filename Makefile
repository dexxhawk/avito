run:
	poetry run uvicorn src.__main__:app --host 0.0.0.0 --port 8080 --reload
db:
	docker compose up -d && make migrate
models:
	sqlacodegen_v2 postgresql://postgres:postgres@localhost/tender --outfile models.py
insert:
	poetry run python src/db/insert.py
migrate:
	cd src/db && poetry run alembic upgrade head