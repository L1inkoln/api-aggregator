import json
from functools import wraps
from typing import Callable, Optional
from redis.asyncio import Redis
import logging
from app.utils.geo import get_location_by_ip

logger = logging.getLogger(__name__)


def cache(ttl: int):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(redis: Redis, *args, **kwargs):
            cache_key = func.__name__
            cached = await redis.get(cache_key)
            if cached:
                logger.info(f"Возвращаем данные из кэша для {cache_key}")
                return json.loads(cached)

            result = await func(redis, *args, **kwargs)
            if redis:
                await redis.setex(cache_key, ttl, json.dumps(result.dict()))
            return result

        return wrapper

    return decorator


def cache_weather(ttl: int = 600):
    """
    Использует отдельный ключ для данных погоды с городом.
    """

    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            location = await get_location_by_ip()
            city = location.city.lower() if location.city else "default_city"
            cache_key = f"weather:{city}"

            redis: Optional[Redis] = kwargs.get("redis", None)
            if redis is None:
                logger.warning("Redis instance not provided.")
                return await func(*args, **kwargs)

            cached = await redis.get(cache_key)
            if cached:
                logger.info(f"Возвращаем данные из кэша для {cache_key}")
                return json.loads(cached)

            result = await func(*args, **kwargs)
            await redis.setex(cache_key, ttl, json.dumps(result.dict()))
            return result

        return wrapper

    return decorator
