from typing import List, Optional
from pydantic import BaseModel


class WeatherResponse(BaseModel):
    city: str
    temp: float
    condition: str
    wind_speed: float


class Location(BaseModel):
    city: str
    latitude: float
    longitude: float


class CurrencyResponse(BaseModel):
    usd: float
    eur: float


class CryptoResponse(BaseModel):
    btc: float
    eth: float
    usdt: float


class StockResponse(BaseModel):
    sp500: Optional[float] = None
    nasdq: Optional[float] = None


class Article(BaseModel):
    title: str
    link: str


class NewsResponse(BaseModel):
    articles: List[Article]


class AggregateResponse(BaseModel):
    weather: WeatherResponse
    currency: CurrencyResponse
    crypto: CryptoResponse
    indexes: StockResponse
    articles: NewsResponse
