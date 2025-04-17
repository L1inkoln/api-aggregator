import logging
import httpx
from app.utils.client import client
from app.utils.geo import get_location_by_ip
from app.models.schemas import WeatherResponse

logger = logging.getLogger(__name__)

# Маппинг погоды
weather_conditions = {
    0: "Ясно",
    1: "Преимущественно ясно",
    2: "Переменная облачность",
    3: "Пасмурно",
    45: "Туман",
    48: "Иней",
}


async def get_weather() -> WeatherResponse:
    location = await get_location_by_ip()
    try:
        response = await client.get(
            f"https://api.open-meteo.com/v1/forecast?latitude={location.latitude}&longitude={location.longitude}&current_weather=true"
        )
        response.raise_for_status()
        data = response.json()
        weather_code = data["current_weather"].get("weathercode")
        return WeatherResponse(
            city=location.city,
            temp=data["current_weather"]["temperature"],
            condition=weather_conditions.get(weather_code, "Неизвестно"),
            wind_speed=data["current_weather"]["windspeed"],
        )
    except httpx.RequestError as e:
        logger.error(f"Ошибка при запросе погоды: {e}")
        return WeatherResponse(
            city=location.city, temp=0.0, condition="Неизвестно", wind_speed=0.0
        )
    except Exception as e:
        logger.error(f"Ошибка обработки данных погоды: {e}")
        return WeatherResponse(
            city=location.city, temp=0.0, condition="Неизвестно", wind_speed=0.0
        )
