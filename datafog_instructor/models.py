from enum import Enum
from pydantic import BaseModel
from typing import List, Optional

class EntityType(Enum):
    # Organization Information
    ORG = "Organization"
    PERSON = "Person"
    TRANSACTION_TYPE = "Transaction Type"
    DEAL_STRUCTURE = "Deal Structure"
    FINANCIAL_INFO = "Financial Information"
    PRODUCT = "Product"
    LOCATION = "Location"
    DATE = "Date"
    INDUSTRY = "Industry"
    ROLE = "Role"
    REGULATORY = "Regulatory"
    SENSITIVE_INFO = "Sensitive Information"
    CONTACT = "Contact"
    ID = "Identifier"
    STRATEGY = "Strategy"
    COMPANY = "Company"
    MONEY = "Money"

    # Personal Information
    EMAIL = "Email Address"
    PHONE = "Phone Number"
    SSN = "Social Security Number"
    CREDIT_CARD = "Credit Card Number"
    IP_ADDRESS = "IP Address"
    URL = "URL"
    AGE = "Age"
    NATIONALITY = "Nationality"
    JOB_TITLE = "Job Title"
    EDUCATION = "Educational Institution"

    # Location Information
    ADDRESS = "Address"
    CITY = "City"
    STATE = "State"
    ZIP = "Zip Code"
    COUNTRY = "Country"
    REGION = "Region"

    


class DetectedEntity(BaseModel):
    text: str
    start: Optional[int] = None
    end: Optional[int] = None
    type: EntityType

class DetectedEntities(BaseModel):
    entities: List[DetectedEntity]