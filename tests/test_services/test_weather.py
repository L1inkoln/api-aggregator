import pytest

from app.services import weather


@pytest.mark.asyncio
async def test_weather_service():
    result = await weather.get_weather()
    assert isinstance(result["city"], str)
    assert isinstance(result["temp"], (int, float))
