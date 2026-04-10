from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import razorpay
import os
import hmac
import hashlib
from ..database import get_db
from ..schemas import CreatePaymentRequest, VerifyPaymentRequest
from ..crud import update_order_paid

router = APIRouter(prefix="/payments", tags=["Payments"])

razorpay_client = razorpay.Client(auth=(
    os.getenv("RAZORPAY_KEY_ID"),
    os.getenv("RAZORPAY_KEY_SECRET")
))

@router.post("/create-payment")
async def create_payment(request: CreatePaymentRequest, db: Session = Depends(get_db)):
    # You can fetch total_amount from order here if you want
    # For simplicity we assume frontend already knows amount
    razorpay_order = razorpay_client.order.create({
        "amount": 100,                    # Replace with actual amount * 100 (paise)
        "currency": "INR",
        "receipt": request.order_id,
        "payment_capture": 1
    })
    return {
        "razorpay_order_id": razorpay_order["id"],
        "amount": razorpay_order["amount"],
        "currency": razorpay_order["currency"],
        "key_id": os.getenv("RAZORPAY_KEY_ID")
    }

@router.post("/verify-payment")
async def verify_payment(request: VerifyPaymentRequest, db: Session = Depends(get_db)):
    # Verify Razorpay signature
    generated_signature = hmac.new(
        bytes(os.getenv("RAZORPAY_KEY_SECRET"), 'utf-8'),
        bytes(f"{request.razorpay_order_id}|{request.razorpay_payment_id}", 'utf-8'),
        hashlib.sha256
    ).hexdigest()

    if generated_signature != request.razorpay_signature:
        raise HTTPException(status_code=400, detail="Payment signature verification failed")

    # Mark order as paid
    order = update_order_paid(db, request.order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return {"status": "success", "message": "Payment verified & order confirmed"}
