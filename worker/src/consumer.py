import asyncio
import json
import aio_pika
import logging
import sys
import os
import sys
# Ensure backend package importable when running as `python -m src.main`
# In worker image: /app/src/*.py lives next to /app/app (backend package)
BACKEND_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # /app/src -> /app
# We need /app/app on sys.path so `import app.core...` resolves
# /app/app contains the python package `app/`
APP_PARENT = BACKEND_ROOT
if APP_PARENT not in sys.path:
    sys.path.insert(0, APP_PARENT)
from app.core.config import settings
from .handlers import handle_incident_created

async def on_message(message: aio_pika.IncomingMessage):
    async with message.process():
        try:
            body = json.loads(message.body.decode())
            event_type = body.get("event")
            if event_type == "incident.created":
                await handle_incident_created(body["payload"])
        except Exception as e:
            logging.exception("Error processing message")
            try:
                logging.error(f"Raw body: {message.body!r}")
            except Exception:
                pass


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