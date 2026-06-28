from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from db import get_db, init_db, engine
from models import Base, User, Model, Image, Prediction, Feedback, TrashLabel
import uvicorn
import os

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    """Initialize database on startup"""
    try:
        init_db()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Warning: Database initialization failed - {str(e)}")
        print("The server will run but database operations may fail until connection is established")
    # Print an explicit, friendly URL using configured host/port (helps when CLI shows 0.0.0.0)
    api_host = os.getenv("API_HOST", "localhost")
    api_port = os.getenv("API_PORT", "8000")
    if api_host in ("0.0.0.0", "::", ""):
        display_host = "localhost"
    else:
        display_host = api_host

    print(f"App available at: http://{display_host}:{api_port}")


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Trash Classifier API", "version": "0.1.0"}





if __name__ == "__main__":
    api_host = os.getenv("API_HOST", "127.0.0.1")
    api_port = int(os.getenv("API_PORT", "8000"))
    uvicorn.run(app, host=api_host, port=api_port, reload=True)
