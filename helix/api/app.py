"""
Module: helix/api/app.py
Copyright (c) 2026 HELIX. All rights reserved.

FastAPI application skeleton with CORS and security headers.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import secrets
from helix.api.routes.files import router as files_router
from helix.api.routes.api import router as full_api_router

app = FastAPI(title="HELIX REST API", version="0.1.0")

# Generate a temporary local token for admin routes
ADMIN_TOKEN = secrets.token_hex(16)
os.environ["HELIX_ADMIN_TOKEN"] = ADMIN_TOKEN

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:7331", "http://localhost:5173"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Accept", "Authorization"],
)

@app.middleware("http")
async def security_headers(request: Request, call_next):
    # Localhost guard for admin routes
    if request.url.path.startswith("/api/v1/admin/"):
        auth_header = request.headers.get("Authorization")
        if not auth_header or auth_header != f"Bearer {ADMIN_TOKEN}":
            from fastapi.responses import JSONResponse
            return JSONResponse(status_code=401, content={"detail": "Unauthorized local access to admin route."})

    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: blob:; "
        "connect-src 'self' ws://localhost:7331 http://localhost:7331 ws://localhost:5173 http://localhost:5173; "
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
