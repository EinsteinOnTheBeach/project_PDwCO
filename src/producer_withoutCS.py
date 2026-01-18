import asyncio
import json
import random
from datetime import datetime
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData


CONNECTION_STR = ""
EVENTHUB_NAME = "inputstream" 

# lista stref do symulacji
ZONES = ["Centrum", "Kazimierz", "Podgorze", "Nowa-Huta", "Bronowice", "Debniki"]

async def generate_traffic_event():
    vehicle_id = f"KR-{random.randint(10000, 99999)}"
    
    from_zone = random.choice(ZONES)
    to_zone = random.choice([z for z in ZONES if z != from_zone])
    
    speed = random.randint(10, 80)
    
    event_body = {
        "plate_number": vehicle_id,
        "from_zone": from_zone,
        "to_zone": to_zone,
        "speed": speed,
        "timestamp": datetime.now().isoformat()
    }
    return event_body

async def run():
    producer = EventHubProducerClient.from_connection_string(
        conn_str=CONNECTION_STR, 
        eventhub_name=EVENTHUB_NAME
    )
    
    print(f"Generator Traffic Flow uruchomiony. Wysyłanie danych do {EVENTHUB_NAME}...")
    
    async with producer:
        while True:
            event_data_batch = await producer.create_batch()
            
            for _ in range(3):
                event = await generate_traffic_event()
                event_data_batch.add(EventData(json.dumps(event)))
            
            await producer.send_batch(event_data_batch)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Wysłano paczkę zdarzeń.")
            
            await asyncio.sleep(1)

if __name__ == "__main__":
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        print("\nZatrzymano generator.")
