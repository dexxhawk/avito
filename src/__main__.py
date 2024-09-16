import os
from fastapi import FastAPI
from src.view import list_of_routes
from src.config.settings import get_settings
import subprocess

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)


def run_migrations():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    location = os.path.join(current_dir, "db")
    result = subprocess.run(
        ["alembic", "upgrade", "head"],
        cwd=location,
        check=True,
        capture_output=True,
        text=True,
    )
    return result


def get_app() -> FastAPI:
    # run_migrations()
    app = FastAPI(
        title="Tender Management API",
        description="""API для управления тендерами и предложениями.

Основные функции API включают управление тендерами (создание, изменение, получение списка) и управление предложениями (создание, изменение, получение списка).""",
        docs_url="/api/docs",
        version="1.0",
    )
    settings = get_settings()
    app.state.settings = settings
    for route in list_of_routes:
        app.include_router(router=route, prefix="/api")
    return app


app = get_app()
