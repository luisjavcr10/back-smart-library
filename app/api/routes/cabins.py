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
    last_updated: datetime
    wifi_rssi: int

@router.get("/cabins/{cabin_id}/status", response_model=CabinStatusResponse)
def get_cabin_status(cabin_id: str, db: Session = Depends(get_db)):
    reading = db.query(CabinReading).filter(CabinReading.cabin_id == cabin_id).order_by(CabinReading.created_at.desc()).first()
    
    if not reading:
        raise HTTPException(status_code=404, detail="Cabin not found")
        
    return CabinStatusResponse(
        cabin_id=reading.cabin_id,
        is_occupied=reading.is_cabin_occupied,
        last_updated=reading.created_at,
        wifi_rssi=reading.wifi_rssi if reading.wifi_rssi else 0
    )

@router.get("/cabins/{cabin_id}/history")
def get_cabin_history(cabin_id: str, limit: int = 20, db: Session = Depends(get_db)):
    readings = db.query(CabinReading).filter(CabinReading.cabin_id == cabin_id)\
                 .order_by(CabinReading.created_at.desc())\
                 .limit(limit).all()
    return readings
