import asyncio
import json
import aio_pika
from app.core.config import settings
from handlers import handle_incident_created

async def on_message(message: aio_pika.IncomingMessage):
    async with message.process():
        try:
            body = json.loads(message.body.decode())
            event_type = body.get("event")
            if event_type == "incident.created":
                await handle_incident_created(body["payload"])
        except Exception as e:
            logging.error(f"Error processing message: {e}")

async def start_consumer():
    connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
    channel = await connection.channel()
    queue = await channel.declare_queue("incidents.events", durable=True)
    await queue.consume(on_message)
    logging.info("Worker listening for incidents.events...")
    try:
        await asyncio.Future()  # run forever
    finally:
        await connection.close()