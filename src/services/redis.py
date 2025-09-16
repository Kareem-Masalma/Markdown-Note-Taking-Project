import redis.asyncio as redis


class RedisCache:
    """This module is used to cache data to redis."""

    def __init__(self, redis_url: str = "redis://localhost:6379/0"):
        self.redis_url = redis_url
        self.redis_client = redis.Redis.from_url(self.redis_url, decode_responses=True)

    async def get(self, key: str) -> str | None:
        """This method to get data from cache"""
        return await self.redis_client.get(key)

    async def set(self, key: str, value: str, expire: int = 3600):
        """This method to set new data to the cache"""
        await self.redis_client.set(key, value, ex=expire)

    async def delete(self, key: str):
        """This method to delete cached value"""
        await self.redis_client.delete(key)
