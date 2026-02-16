"""FastAPI TODO API - Main application."""

from fastapi import FastAPI
from app.routes import router

# Create FastAPI app
app = FastAPI(
    title="TODO API",
    description="Simple TODO API built with FastAPI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Include routers
app.include_router(router)


@app.get("/", tags=["root"])
def root():
    """Root endpoint.

    Returns:
        Welcome message
    """
    return {
        "message": "Welcome to TODO API",
        "docs": "/docs",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
