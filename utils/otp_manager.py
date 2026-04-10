import random
from datetime import datetime, timedelta

otp_store = {}  # email -> {"otp": str, "expires": datetime}

def generate_otp() -> str:
    return f"{random.randint(100000, 999999)}"

def store_otp(email: str, otp: str):
    otp_store[email] = {
        "otp": otp,
        "expires": datetime.utcnow() + timedelta(minutes=10)
    }

def verify_otp(email: str, user_otp: str) -> bool:
    data = otp_store.get(email)
    if not data or datetime.utcnow() > data["expires"]:
        return False
    if data["otp"] != user_otp:
        return False
    del otp_store[email]  # one-time use
    return True
