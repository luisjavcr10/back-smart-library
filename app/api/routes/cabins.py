from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.cabin import CabinReading
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

# Schema para respuesta
class CabinStatusResponse(BaseModel):
    cabin_id: str
    is_occupied: bool
    connection_status: str # "ONLINE", "OFFLINE", "NO_SIGNAL"
    last_updated: datetime | None = None
    wifi_rssi: int

@router.get(
    "/cabins/{cabin_id}/status", 
    response_model=CabinStatusResponse,
    tags=["Cabins"],
    summary="Get real-time cabin status",
    description="Returns the latest status. If no signal received yet, returns status 'NO_SIGNAL'."
)
def get_cabin_status(cabin_id: str, db: Session = Depends(get_db)):
    reading = db.query(CabinReading).filter(CabinReading.cabin_id == cabin_id).order_by(CabinReading.created_at.desc()).first()
    
    # Si no hay datos (nunca ha reportado)
    if not reading:
        return CabinStatusResponse(
            cabin_id=cabin_id,
            is_occupied=False,
            connection_status="NO_SIGNAL",
            last_updated=None,
            wifi_rssi=0
        )
    
    # Lógica de Heartbeat: Si el último dato es muy viejo (> 2 minutos), asumimos desconexión
    time_diff = datetime.now(reading.created_at.tzinfo) - reading.created_at
    if time_diff.total_seconds() > 120: # 2 minutos de tolerancia
         return CabinStatusResponse(
            cabin_id=reading.cabin_id,
            is_occupied=False, # Si no hay señal, asumimos libre o estado desconocido
            connection_status="NO_SIGNAL", # O "OFFLINE"
            last_updated=reading.created_at,
            wifi_rssi=0
        )

    return CabinStatusResponse(
        cabin_id=reading.cabin_id,
        is_occupied=reading.is_cabin_occupied,
        connection_status="ONLINE", 
        last_updated=reading.created_at,
        wifi_rssi=reading.wifi_rssi if reading.wifi_rssi else 0
    )

@router.get(
    "/cabins/{cabin_id}/history",
    response_model=List[CabinStatusResponse], # Assuming we want to return the same schema or similar
    tags=["Cabins"],
    summary="Get cabin usage history",
    description="Retrieve historical sensor readings for a cabin."
)
def get_cabin_history(cabin_id: str, limit: int = 20, db: Session = Depends(get_db)):
    readings = db.query(CabinReading).filter(CabinReading.cabin_id == cabin_id)\
                 .order_by(CabinReading.created_at.desc())\
                 .limit(limit).all()
    return readings
