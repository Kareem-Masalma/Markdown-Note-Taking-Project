import redis.asyncio as redis


class RedisCache:
    def __init__(self, redis_url: str = "redis://localhost:6379/0"):
        self.redis_url = redis_url
        self.redis_client = redis.Redis.from_url(self.redis_url, decode_responses=True)

    async def get(self, key: str) -> str | None:
        return await self.redis_client.get(key)

    async def set(self, key: str, value: str, expire: int = 3600):
        await self.redis_client.set(key, value, ex=expire)

    async def delete(self, key: str):
        await self.redis_client.delete(key)
