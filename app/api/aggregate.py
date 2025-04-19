from fastapi import APIRouter, Depends
from redis.asyncio import Redis
from app.services import weather, currency, crypto, stocks, news
from app.models.schemas import AggregateResponse
from app.utils.redis import get_redis

router = APIRouter()


@router.get("/aggregate", response_model=AggregateResponse)
async def aggregate_data(redis: Redis = Depends(get_redis)):
    weather_data = await weather.get_weather(redis=redis)
    currency_data = await currency.get_currency(redis=redis)
    crypto_data = await crypto.get_crypto(redis=redis)
    indexes = await stocks.get_stock_indexes(redis=redis)
    news_articles = await news.get_news_titles(redis=redis)

    return AggregateResponse(
        weather=weather_data,
        currency=currency_data,
        crypto=crypto_data,
        indexes=indexes,
        articles=news_articles,
    )
