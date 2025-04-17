import logging
import httpx
from app.utils.client import client
from app.models.schemas import CurrencyResponse

logger = logging.getLogger(__name__)


async def get_currency() -> CurrencyResponse:
    try:
        response = await client.get(
            "https://www.cbr-xml-daily.ru/daily_json.js",
            timeout=5.0,
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
