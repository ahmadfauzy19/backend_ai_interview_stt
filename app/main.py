from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from app.routers import interview

app = FastAPI(
    title="AI Interview API",
    description="Backend API untuk AI Interview Recording dan Processing",
    version="1.0.0"
)

# CORS (WAJIB untuk React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(interview.router)

# Custom OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="AI Interview API",
        version="1.0.0",
        description="API untuk video interview recording",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.get("/", tags=["Root"])
async def root():
    """Health check endpoint"""
    return {
        "message": "AI Interview Backend API",
        "docs": "/docs",
        "redoc": "/redoc"
    }
