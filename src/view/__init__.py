from src.view import ping, tender, bid

list_of_routes = [ping.ping_router, tender.tender_router, bid.bid_router]

__all__ = ["list_of_routes"]
