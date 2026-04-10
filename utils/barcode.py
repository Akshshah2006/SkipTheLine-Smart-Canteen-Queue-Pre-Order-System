import qrcode
import os
from datetime import datetime

os.makedirs("static/barcodes", exist_ok=True)

def generate_barcode(order_id: str) -> str:
    """Generate QR code and return public URL"""
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(order_id)
    qr.make(fit=True)

    img = qr.make_image(fill_color="#4F46E5", back_color="white")
    filename = f"{order_id}.png"
    path = f"static/barcodes/{filename}"
    img.save(path)
    return f"/static/barcodes/{filename}"
