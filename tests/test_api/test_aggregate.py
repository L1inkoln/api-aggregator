from fastapi.testclient import TestClient
from app.main import app
from app.models.schemas import WeatherResponse, CurrencyResponse, AggregateResponse


def test_aggregate_endpoint(monkeypatch):
    async def mock_weather():
        return WeatherResponse(
            city="Москва", temp=20.0, condition="Ясно", wind_speed=3.0
        )

    async def mock_currency():
        return CurrencyResponse(usd=95.0, eur=101.0)

    monkeypatch.setattr("app.services.weather.get_weather", mock_weather)
    monkeypatch.setattr("app.services.currency.get_currency", mock_currency)

    with TestClient(app) as client:
        response = client.get("/api/aggregate")
        assert response.status_code == 200

        json_data = response.json()

        expected = AggregateResponse(
            weather=WeatherResponse(
                city="Москва", temp=20.0, condition="Ясно", wind_speed=3.0
            ),
            currency=CurrencyResponse(usd=95.0, eur=101.0),
        )

        assert json_data == expected.model_dump()
