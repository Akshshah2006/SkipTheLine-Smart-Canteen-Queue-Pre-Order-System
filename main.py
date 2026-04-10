from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .routers import auth, orders, payments
from dotenv import load_dotenv
import uvicorn

load_dotenv()

app = FastAPI(title="SkipTheLine - Smart Canteen Backend")

# CORS - allows your frontend (running on any port) to call this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # Change to your domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static folder for QR codes
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth.router)
app.include_router(orders.router)
app.include_router(payments.router)

@app.get("/")
async def root():
    return {"message": "🚀 SkipTheLine Backend is running!"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
