from src.view import ping, tender

list_of_routes = [
    ping.ping_router,
    tender.tender_router
]

__all__ = [
    "list_of_routes"
]