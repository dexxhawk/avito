from enum import Enum
from typing import Literal

TenderStatus = Literal['Created', 'Published', 'Closed']
TenderServiceType = Literal['Construction', 'Delivery', 'Manufacture']
BidStatus = Literal['Created', 'Published', 'Canceled', 'Approved', 'Rejected']
BidDecision = Literal['Approved', 'Rejected']
BidAuthorType = Literal['Organization', 'User']

# class tender_status(Enum):
#     CREATED = 'Created'
#     PUBLISHED = 'Published'
#     CLOSED = 'Closed'

# class tender_service_type(Enum):
#     CONSTRUCTION = "Construction"
#     DELIVERY = "Delivery"
#     MANUFACTURE = "Manufacture"

# class bid_status(Enum):
#     CREATED = 'Created'
#     PUBLISHED = 'Published'
#     CANCELED = 'Canceled'
#     APPROVED = 'Approved'
#     REJECTED = 'Rejected'

# class bid_decision(Enum):
#     APPROVED = "Approved"
#     REJECTED = "Rejected"

# class bid_author_type(Enum):
#     ORGANIZATION = "Organization"
#     USER = "User"