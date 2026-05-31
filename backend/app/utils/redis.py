from redis.asyncio import Redis
from app.core.config import settings

class RedisClient:
    def __init__(self):
        self.redis = Redis.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)

    async def ping(self):
        await self.redis.ping()

    async def get(self, key: str) -> str:
        return await self.redis.get(key)

    async def set(self, key: str, value: str, ex: int = None):
        await self.redis.set(key, value, ex=ex)

    async def delete(self, key: str):
        await self.redis.delete(key)

    async def close(self):
        await self.redis.close()

redis_client = RedisClient()