import httpx
from app.models.schemas import Location


async def get_location_by_ip() -> Location:
    async with httpx.AsyncClient() as client:
        # Запрашиваем данные по IP
        response = await client.get("http://ip-api.com/json/")
        data = response.json()
        return Location(city=data["city"], latitude=data["lat"], longitude=data["lon"])
