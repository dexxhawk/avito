from typing import Literal

TenderStatus = Literal["Created", "Published", "Closed"]
TenderServiceType = Literal["Construction", "Delivery", "Manufacture"]
BidStatus = Literal["Created", "Published", "Canceled", "Approved", "Rejected"]
BidDecision = Literal["Approved", "Rejected"]
BidAuthorType = Literal["Organization", "User"]
