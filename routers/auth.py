from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import LoginRequest, VerifyOTPRequest
from ..utils.otp_manager import generate_otp, store_otp, verify_otp
from ..utils.email_sender import send_otp_email
from ..crud import create_or_verify_user

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    if not request.email.endswith("@karnavatiuniversity.edu.in"):
        raise HTTPException(status_code=400, detail="Only Karnavati University emails allowed")
    
    otp = generate_otp()
    store_otp(request.email, otp)
    
    if send_otp_email(request.email, otp):
        return {"message": "OTP sent successfully", "email": request.email}
    else:
        raise HTTPException(status_code=500, detail="Failed to send OTP")

@router.post("/verify-otp")
async def verify_otp_endpoint(request: VerifyOTPRequest, db: Session = Depends(get_db)):
    if not verify_otp(request.email, request.otp):
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")
    
    create_or_verify_user(db, request.email)
    return {"status": "verified", "message": "Login successful"}
