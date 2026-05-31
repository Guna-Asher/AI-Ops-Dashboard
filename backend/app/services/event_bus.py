import json
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.queue import rabbitmq_client

class EventBus:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def publish_incident_created(self, incident_id: int) -> None:
        message = {
            "event": "incident.created",
            "payload": {"incident_id": incident_id}
        }
        await rabbitmq_client.publish("incidents.events", json.dumps(message))