"""
Module: helix/api/app.py
Copyright (c) 2026 HELIX. All rights reserved.

FastAPI application skeleton with CORS and security headers.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from helix.api.routes.files import router as files_router
from helix.api.routes.api import router as full_api_router

app = FastAPI(title="HELIX REST API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:7331"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Accept"],
)

@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: blob:; "
        "connect-src 'self' ws://localhost:7331; "
        "font-src 'self'; "
        "object-src 'none'; "
        "base-uri 'self';"
    )
    return response

app.include_router(files_router, prefix="/api/v1")
app.include_router(full_api_router, prefix="/api/v1")

@app.get("/api/v1/status")
async def get_status():
    """Health check endpoint."""
    return {"success": True, "data": {"status": "ok"}}

# Serve frontend static files if they exist
frontend_dist = os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "dist")
if os.path.exists(frontend_dist):
    app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="frontend")
