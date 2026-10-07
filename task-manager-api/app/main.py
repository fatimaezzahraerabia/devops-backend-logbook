import structlog
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from app.api.v1.router import api_router
from app.core.config import settings
from app.services.middleware import CorrelationIdMiddleware

logger = structlog.get_logger()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url="/api/v1/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Custom Middleware
app.add_middleware(CorrelationIdMiddleware)

# Routeur API V1
app.include_router(api_router, prefix="/api/v1")

# Prometheus Metrics Instrumentator
Instrumentator().instrument(app).expose(app, endpoint="/metrics")


@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "environment": settings.ENVIRONMENT
    }
