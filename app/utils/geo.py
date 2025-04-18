import httpx
from app.utils.constants import GEO_API
from app.models.schemas import Location


async def get_location_by_ip() -> Location:
    async with httpx.AsyncClient() as client:
        # Запрашиваем данные по IP
        response = await client.get(GEO_API)
        data = response.json()
        return Location(city=data["city"], latitude=data["lat"], longitude=data["lon"])
