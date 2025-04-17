import httpx

client = httpx.AsyncClient(timeout=10.0)


async def close_client():
    await client.aclose()
