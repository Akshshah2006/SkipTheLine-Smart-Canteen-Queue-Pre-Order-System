from pydantic import BaseModel, EmailStr, field_validator
from typing import List, Optional
from datetime import datetime

class LoginRequest(BaseModel):
    email: EmailStr

class VerifyOTPRequest(BaseModel):
    email: EmailStr
    otp: str

class PlaceOrderRequest(BaseModel):
    email: EmailStr
    items: List[str]
    pickup_time: str   # Must be in "HH:MM" format
    total_amount: int = 0

    @field_validator("pickup_time")
    @classmethod
    def validate_pickup_time(cls, v: str):
        if not v or len(v) != 5 or v[2] != ":":
            raise ValueError("pickup_time must be in HH:MM format (e.g. 13:30)")
        return v

class CreatePaymentRequest(BaseModel):
    order_id: str

class VerifyPaymentRequest(BaseModel):
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str
    order_id: str

class OrderResponse(BaseModel):
    order_id: str
    token: int
    items: List[str]
    pickup_time: str
    status: str
    payment_status: str
    barcode_url: Optional[str] = None
    total_amount: int
