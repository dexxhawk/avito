from fastapi import FastAPI
from src.view import list_of_routes

# def bind_routes(app: FastAPI, )


def get_app() -> FastAPI:
    app = FastAPI()
    for route in list_of_routes:
        app.include_router(router=route, prefix="/api")
    return app


app = get_app()
