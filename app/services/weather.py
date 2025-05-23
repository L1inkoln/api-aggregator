import logging
from httpx import RequestError
from redis.asyncio import Redis
from app.utils.cache import cache_weather
from app.utils.client import client
from app.utils.geo import get_location_by_ip
from app.models.schemas import WeatherResponse
from app.utils.constants import WEATHER_CONDITIONS

logger = logging.getLogger(__name__)


@cache_weather(ttl=1200)
async def get_weather(redis: Redis) -> WeatherResponse:
    location = await get_location_by_ip()
    try:
        data = await _fetch_weather_data(location.latitude, location.longitude)
        return _parse_weather(data, city=location.city)
    except RequestError as e:
        logger.error(f"Ошибка при запросе погоды: {e}")
    except Exception as e:
        logger.error(f"Ошибка обработки данных погоды: {e}")

    return WeatherResponse(
        city=location.city, temp=0.0, condition="Неизвестно", wind_speed=0.0
    )


async def _fetch_weather_data(latitude: float, longitude: float) -> dict:
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}&longitude={longitude}&current_weather=true"
    )
    response = await client.get(url)
    response.raise_for_status()
    return response.json()


def _parse_weather(data: dict, city: str) -> WeatherResponse:
    current = data.get("current_weather", {})
    weather_code = current.get("weathercode")
    return WeatherResponse(
        city=city,
        temp=current.get("temperature", 0.0),
        condition=WEATHER_CONDITIONS.get(weather_code, "Неизвестно"),
        wind_speed=current.get("windspeed", 0.0),
    )
