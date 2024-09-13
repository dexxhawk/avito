from fastapi import APIRouter
from fastapi.responses import PlainTextResponse


ping_router = APIRouter(tags=["ping"])


@ping_router.get("/ping", response_class=PlainTextResponse)
def ping():
    return PlainTextResponse("ok", status_code=200)
