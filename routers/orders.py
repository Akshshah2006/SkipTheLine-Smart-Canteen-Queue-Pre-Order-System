from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from ..database import get_db
from ..schemas import PlaceOrderRequest, OrderResponse
from ..crud import create_order, get_user_orders, get_queue_status
from ..utils.barcode import generate_barcode

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/place-order", response_model=OrderResponse)
async def place_order(request: PlaceOrderRequest, db: Session = Depends(get_db)):
    # Time validation - minimum 30 minutes gap
    now = datetime.now()
    try:
        pickup_hour, pickup_min = map(int, request.pickup_time.split(":"))
        pickup_dt = now.replace(hour=pickup_hour, minute=pickup_min, second=0, microsecond=0)
        if pickup_dt < now:
            pickup_dt = pickup_dt.replace(day=pickup_dt.day + 1)
    except:
        raise HTTPException(status_code=400, detail="Invalid pickup_time format")

    min_pickup = now + timedelta(minutes=30)
    if pickup_dt < min_pickup:
        raise HTTPException(
            status_code=400,
            detail="Pickup time must be at least 30 minutes after current time"
        )

    order = create_order(db, request.email, request.items, request.pickup_time, request.total_amount)
    
    # Generate QR barcode
    barcode_url = generate_barcode(order.order_id)
    order.barcode_path = barcode_url
    db.commit()

    return {
        "order_id": order.order_id,
        "token": order.token,
        "items": request.items,
        "pickup_time": order.pickup_time,
        "status": order.status,
        "payment_status": order.payment_status,
        "barcode_url": barcode_url,
        "total_amount": order.total_amount
    }

@router.get("/user/{email}")
async def get_orders(email: str, db: Session = Depends(get_db)):
    return get_user_orders(db, email)

@router.get("/queue-status")
async def queue_status(db: Session = Depends(get_db)):
    return get_queue_status(db)
