from sqlalchemy.orm import Session
from .models import User, Order
from uuid import uuid4
import json
from datetime import datetime

def create_or_verify_user(db: Session, email: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(email=email, verified=True, course="B.Tech", year=3)
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        user.verified = True
        db.commit()
    return user

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_order(db: Session, email: str, items: list, pickup_time: str, total_amount: int):
    # Only verified users
    user = get_user_by_email(db, email)
    if not user or not user.verified:
        raise ValueError("User not verified")

    # Token = next number
    last_token = db.query(Order).order_by(Order.token.desc()).first()
    token = (last_token.token + 1) if last_token else 1001

    order_id = str(uuid4())
    new_order = Order(
        order_id=order_id,
        email=email,
        items=json.dumps(items),
        pickup_time=pickup_time,
        token=token,
        total_amount=total_amount,
        status="waiting",
        payment_status="pending"
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

def update_order_paid(db: Session, order_id: str):
    order = db.query(Order).filter(Order.order_id == order_id).first()
    if order:
        order.payment_status = "paid"
        db.commit()
        db.refresh(order)
    return order

def get_user_orders(db: Session, email: str):
    orders = db.query(Order).filter(Order.email == email).all()
    for o in orders:
        o.items = json.loads(o.items) if o.items else []
    return orders

def get_queue_status(db: Session):
    waiting = db.query(Order).filter(Order.status == "waiting", Order.payment_status == "paid").count()
    return {
        "current_queue_length": waiting,
        "estimated_wait_minutes": waiting * 6,   # avg 6 min per order
        "next_token": 1001 + db.query(Order).count()
    }
