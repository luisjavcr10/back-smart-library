import os
from pydantic import field_validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "IoT Cabinas API"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")

    @field_validator("DATABASE_URL")
    def assemble_db_connection(cls, v: str | None) -> str:
        if v and v.startswith("postgresql://"):
            return v.replace("postgresql://", "postgresql+psycopg://", 1)
        return v
    
    # MQTT Config
    MQTT_BROKER: str = os.getenv("MQTT_BROKER", "broker.emqx.io")
    MQTT_PORT: int = int(os.getenv("MQTT_PORT", 1883))
    MQTT_USERNAME: str = os.getenv("MQTT_USERNAME", "")
    MQTT_PASSWORD: str = os.getenv("MQTT_PASSWORD", "")

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
