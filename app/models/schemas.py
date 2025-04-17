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


class AggregateResponse(BaseModel):
    weather: WeatherResponse
    currency: CurrencyResponse
