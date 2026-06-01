from datetime import datetime
from enum import Enum
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, ConfigDict

class StatusValue(str, Enum):
    CREATED = "CREATED"
    READY = "READY"
    FAILED = "FAILED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    EXPIRED = "EXPIRED"

class Amount(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    value: str = Field(..., pattern=r"^\d+\.\d{2}$")
    currency: str = Field(...)

    @property
    def float_value(self) -> float:
        return float(self.value)

class Status(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    value: StatusValue
    changedDateTime: datetime

class RecipientFields(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    account: str

class RecipientDetails(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    providerCode: str
    fields: RecipientFields

class Customer(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    account: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

class Source(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    paymentType: str
    paymentToolType: str
    paymentTerminalType: str
    paymentDate: Optional[datetime] = None
    extraCharge: Optional[Amount] = None

class BillingDetails(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    transactionId: str
    rrn: Optional[str] = None

class PaymentInfo(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    paymentId: str = Field(..., max_length=36)
    creationDateTime: datetime
    expirationDatetime: Optional[datetime] = None
    status: Status
    recipientDetails: RecipientDetails
    amount: Amount
    commission: Optional[Amount] = None
    customer: Optional[Customer] = None
    source: Source
    customFields: Optional[Dict[str, str]] = None
    callbackUrl: Optional[str] = None
    identificationType: Optional[str] = None
    billingDetails: Optional[BillingDetails] = None

class BalanceInfo(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    balance: Amount
    overdraft: Amount
    available: Amount

class CommonError(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    errorCode: str
    userMessage: str
    description: Optional[str] = None
