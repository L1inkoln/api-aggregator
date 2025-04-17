import pytest
from types import SimpleNamespace


@pytest.fixture
def mock_location():
    return SimpleNamespace(latitude=55.75, longitude=37.62, city="Москва")


@pytest.fixture
def weather_response():
    return {
        "current_weather": {"temperature": 12.3, "weathercode": 0, "windspeed": 3.5}
    }


@pytest.fixture
def currency_response():
    return {"Valute": {"USD": {"Value": 95.0}, "EUR": {"Value": 102.0}}}
