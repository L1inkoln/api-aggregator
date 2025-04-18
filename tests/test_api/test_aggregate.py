import pytest


@pytest.mark.anyio
async def test_health_check(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.anyio
async def test_aggregate_endpoint(client):
    response = await client.get("/api/aggregate?city=Moscow")
    assert response.status_code == 200
    data = response.json()
    assert "weather" in data
    assert "currency" in data
    assert isinstance(data["weather"]["temp"], (int, float))
    assert isinstance(data["currency"]["usd"], (int, float))
