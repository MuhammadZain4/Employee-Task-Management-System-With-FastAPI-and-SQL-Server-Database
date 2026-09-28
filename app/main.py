import time
from app.routers import emp as e
from app.routers import task as t
from app.routers import users as u
from fastapi import FastAPI,Request
import logging
import app.config.loggers
from fastapi.middleware.cors import CORSMiddleware
logger=logging.getLogger(__name__)
app=FastAPI(
    title="Employee and Task Management System",
    version='1.0.0'
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(u.router)
app.include_router(e.router)
app.include_router(t.router)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration_ms = (time.time() - start) * 1000
    logger.info(f"{request.method} {request.url.path} -> {response.status_code} ({duration_ms:.1f}ms)")
    return response

@app.get('/')
def root():
    return{"message":"api is running"}