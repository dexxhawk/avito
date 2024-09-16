from enum import Enum


class TenderStatus(str, Enum):
    Created = "Created"
    Published = "Published"
    Closed = "Closed"


class TenderServiceType(str, Enum):
    Construction = "Construction"
    Delivery = "Delivery"
    Manufacture = "Manufacture"


class BidStatus(str, Enum):
    Created = "Created"
    Published = "Published"
    Canceled = "Canceled"


class BidDecision(str, Enum):
    Approved = "Approved"
    Rejected = "Rejected"


class BidAuthorType(str, Enum):
    Organization = "Organization"
    User = "User"
