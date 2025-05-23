import logging
import httpx
from redis.asyncio import Redis
from app.utils.cache import cache
from app.utils.constants import CBR_API
from app.utils.client import client
from app.models.schemas import CurrencyResponse

logger = logging.getLogger(__name__)


@cache(ttl=1800)
async def get_currency(redis: Redis) -> CurrencyResponse:
    try:
        response = await client.get(
            CBR_API,
        )
        response.raise_for_status()
        data = response.json()

        return CurrencyResponse(
            usd=data["Valute"]["USD"]["Value"], eur=data["Valute"]["EUR"]["Value"]
        )
    except httpx.RequestError as e:
        logger.error(f"Ошибка при запросе курса валют: {e}")
        return CurrencyResponse(usd=90.0, eur=98.5)
    except Exception as e:
        logger.error(f"Ошибка обработки данных курса валют: {e}")
        return CurrencyResponse(usd=90.0, eur=98.5)
