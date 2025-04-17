import pytest
import respx
from httpx import Response
from app.services.weather import get_weather
from app.models.schemas import WeatherResponse


@pytest.mark.asyncio
@respx.mock
async def test_get_weather(monkeypatch, mock_location, weather_response):
    async def fake_location():
        return mock_location

    monkeypatch.setattr("app.services.weather.get_location_by_ip", fake_location)
    respx.get(
        "https://api.open-meteo.com/v1/forecast?latitude=55.75&longitude=37.62&current_weather=true"
    ).mock(return_value=Response(200, json=weather_response))
    result = await get_weather()
    expected = WeatherResponse(
        city="Москва",
        temp=12.3,
        condition="Ясно",
        wind_speed=3.5,
    )
    assert result == expected
