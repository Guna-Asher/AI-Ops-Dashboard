import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models.incident import Incident
from app.models.log import LogEntry
from ai_client import AIClient

logger = logging.getLogger(__name__)

engine = create_async_engine(settings.DATABASE_URL, echo=False)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def handle_incident_created(payload: dict):
    incident_id = payload["incident_id"]
    logger.info(f"Processing incident {incident_id}")
    async with async_session() as session:
        incident = await session.get(Incident, incident_id)
        if not incident:
            logger.error(f"Incident {incident_id} not found")
            return
        # fetch recent logs for that incident
        logs = await session.execute(
            LogEntry.__table__.select().where(LogEntry.incident_id == incident_id).limit(50)
        )
        log_text = "\n".join([f"{l.timestamp} [{l.level}] {l.message}" for l in logs])
        analysis = await AIClient().analyze_incident(
            {"title": incident.title, "description": incident.description, "status": incident.status, "severity": incident.severity},
            log_text
        )
        logger.info(f"AI analysis for incident {incident_id}: {analysis}")
        # store analysis somewhere (e.g., update incident description or add a comment)
        # For simplicity, we'll append to description
        incident.description = (incident.description or "") + f"\n\n[AI Analysis]\n{analysis}"
        await session.commit()