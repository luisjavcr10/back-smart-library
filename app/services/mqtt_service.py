import asyncio
import json
from asyncio_mqtt import Client, MqttError
from app.core.config import settings
from app.db.session import SessionLocal
from app.models.cabin import CabinReading

async def process_message(payload: str):
    try:
        data = json.loads(payload)
        db = SessionLocal()
        
        # Crear nuevo registro
        reading = CabinReading(
            cabin_id=data.get('cabina_id', 'unknown'),
            distance_cm=data.get('distancia_cm'),
            is_table_occupied=data.get('mesa_ocupada', False),
            fsr1=data.get('fsr', {}).get('pata1'),
            fsr2=data.get('fsr', {}).get('pata2'),
            fsr3=data.get('fsr', {}).get('pata3'),
            fsr4=data.get('fsr', {}).get('pata4'),
            fsr_average=data.get('fsr', {}).get('promedio'),
            is_seat_occupied=data.get('estado', {}).get('asiento_ocupado', False),
            is_cabin_occupied=data.get('estado', {}).get('cabina_ocupada', False),
            wifi_rssi=data.get('wifi_rssi')
        )
        
        db.add(reading)
        db.commit()
        db.close()
        print(f"✅ Data processed for {data.get('cabina_id')}")
        
    except Exception as e:
        print(f"❌ Error processing message: {e}")

async def mqtt_loop():
    while True:
        try:
            print(f"🔌 Connecting to MQTT Broker: {settings.MQTT_BROKER}:{settings.MQTT_PORT}")
            
            # Configurar TLS si es puerto seguro (8883)
            tls_context = None
            if settings.MQTT_PORT == 8883:
                import ssl
                tls_context = ssl.create_default_context()
            
            async with Client(
                hostname=settings.MQTT_BROKER, 
                port=settings.MQTT_PORT, 
                username=settings.MQTT_USERNAME, 
                password=settings.MQTT_PASSWORD,
                tls_context=tls_context
            ) as client:
                
                async with client.messages() as messages:
                    await client.subscribe("cabina/+/sensors")
                    print("✅ Subscribed to cabina/+/sensors")
                    
                    async for message in messages:
                        payload = message.payload.decode()
                        await process_message(payload)
                        
        except MqttError as e:
            print(f"❌ MQTT Connection Error: {e}. Retrying in 5s...")
            await asyncio.sleep(5)
        except Exception as e:
            print(f"❌ Critical MQTT Error: {e}. Retrying in 5s...")
            await asyncio.sleep(5)
