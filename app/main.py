from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio
from app.core.config import settings
from app.api.routes import cabins
from app.services.mqtt_service import mqtt_loop
from app.db.session import engine, Base
# Importar modelos para que SQLAlchemy los registre antes de crear las tablas
from app.models import cabin

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Crear tablas en BD si no existen
    Base.metadata.create_all(bind=engine)
    
    # Start MQTT loop in background
    task = asyncio.create_task(mqtt_loop())
    yield
    # Clean up (optional)
    task.cancel()


tags_metadata = [
    {
        "name": "Cabins",
        "description": "Operations with IoT Cabins (status, history, etc.)",
    },
    {
        "name": "Health",
        "description": "API Health check",
    },
]

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API for managing and monitoring IoT Cabins. Real-time status updates via MQTT and historical data access.",
    version="1.0.0",
    openapi_tags=tags_metadata,
    lifespan=lifespan
)


app.include_router(cabins.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to IoT Cabinas API"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
