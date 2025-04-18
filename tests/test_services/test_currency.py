import pytest
from app.services import weather, currency


@pytest.mark.anyio
async def test_weather_service():
    result = await weather.get_weather("Moscow")
    assert isinstance(result["city"], str)
    assert isinstance(result["temp"], (int, float))


@pytest.mark.anyio
async def test_currency_service():
    result = await currency.get_currency()
    assert isinstance(result["usd"], (int, float))
    assert isinstance(result["eur"], (int, float))
