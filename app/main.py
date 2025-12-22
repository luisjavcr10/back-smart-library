from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio
from app.core.config import settings
from app.api.routes import cabins
from app.services.mqtt_service import mqtt_loop

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start MQTT loop in background
    task = asyncio.create_task(mqtt_loop())
    yield
    # Clean up (optional)
    task.cancel()

app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

app.include_router(cabins.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to IoT Cabinas API"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
