from fastapi import APIRouter
from app.services import weather, currency
from app.models.schemas import AggregateResponse

router = APIRouter()


@router.get("/aggregate", response_model=AggregateResponse)
async def aggregate_data():
    weather_data = await weather.get_weather()
    currency_data = await currency.get_currency()
    return {
        "weather": weather_data,
        "currency": currency_data,
    }
