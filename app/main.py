"""
AI Interview Backend API
Main FastAPI application entry point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from app.config import (
    API_TITLE,
    API_DESCRIPTION,
    API_VERSION,
    CORS_CONFIG,
)
from app.routers import interview
from app.logger import setup_logger

logger = setup_logger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    **CORS_CONFIG,
)

# Include routers
app.include_router(interview.router)


# Custom OpenAPI schema
def custom_openapi():
    """Customize OpenAPI documentation"""
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=API_TITLE,
        version=API_VERSION,
        description=API_DESCRIPTION,
        routes=app.routes,
    )
    
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """
    Health check endpoint
    
    Returns basic API information and documentation links.
    """
    return {
        "message": "AI Interview Backend API",
        "version": API_VERSION,
        "docs": "/docs",
        "redoc": "/redoc"
    }
