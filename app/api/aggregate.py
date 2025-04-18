from fastapi import APIRouter
from app.services import weather, currency, crypto, stocks, news
from app.models.schemas import AggregateResponse


router = APIRouter()


@router.get("/aggregate", response_model=AggregateResponse)
async def aggregate_data():
    weather_data = await weather.get_weather()
    currency_data = await currency.get_currency()
    crypto_data = await crypto.get_crypto()
    indexes = await stocks.get_stock_indexes()
    news_articles = await news.get_news_titles()
    return {
        "weather": weather_data,
        "currency": currency_data,
        "crypto": crypto_data,
        "indexes": indexes,
        "articles": news_articles,
    }
