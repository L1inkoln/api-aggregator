import pytest
import respx
from httpx import Response
from app.services.currency import get_currency
from app.models.schemas import CurrencyResponse


@pytest.mark.asyncio
@respx.mock
async def test_get_currency_success(currency_response):
    respx.get("https://www.cbr-xml-daily.ru/daily_json.js").mock(
        return_value=Response(200, json=currency_response)
    )
    result = await get_currency()
    expected = CurrencyResponse(usd=95.0, eur=102.0)
    assert result == expected


@pytest.mark.asyncio
@respx.mock
async def test_get_currency_fallback():
    respx.get("https://www.cbr-xml-daily.ru/daily_json.js").mock(
        return_value=Response(500)
    )
    result = await get_currency()
    expected = CurrencyResponse(usd=90.0, eur=98.5)
    assert result == expected
