from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.sql import func
from app.db.session import Base

class CabinReading(Base):
    __tablename__ = "cabin_readings"

    id = Column(Integer, primary_key=True, index=True)
    cabin_id = Column(String(50), nullable=False)
    
    distance_cm = Column(Float)
    is_table_occupied = Column(Boolean, default=False)
    
    fsr1 = Column(Integer)
    fsr2 = Column(Integer)
    fsr3 = Column(Integer)
    fsr4 = Column(Integer)
    fsr_average = Column(Float)
    
    is_seat_occupied = Column(Boolean, default=False)
    is_cabin_occupied = Column(Boolean, default=False)
    
    wifi_rssi = Column(Integer)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
