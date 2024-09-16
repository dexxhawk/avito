from enum import Enum
from typing import Literal

TenderStatus = Literal["Created", "Published", "Closed"]
TenderServiceType = Literal["Construction", "Delivery", "Manufacture"]
BidStatus = Literal["Created", "Published", "Canceled", "Approved", "Rejected"]
BidDecision = Literal["Approved", "Rejected"]
BidAuthorType = Literal["Organization", "User"]


# class TenderStatus(Enum):
#     Created = 'Created'
#     Published = 'Published'
#     Closed = 'Closed'

# class TenderServiceType(Enum):
#     Construction = 'Construction'
#     Delivery = 'Delivery'
#     Manufacture = 'Manufacture'

# class BidStatus(Enum):
#     Created = 'Created'
#     Published = 'Published'
#     Canceled = 'Canceled'


# class BidDecision(Enum):
#     Approved = 'Approved'
#     Rejected = 'Rejected'

# class BidAuthorType(Enum):
#     Organization = 'Organization'
#     User = 'User'
