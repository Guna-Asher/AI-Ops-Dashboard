import asyncio
import logging
from .consumer import start_consumer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Starting worker...")
    asyncio.run(start_consumer())