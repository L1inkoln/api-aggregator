from app.utils.constants import COINS, CURRENCY
from app.utils.client import client
from app.models.schemas import CryptoResponse
import logging

logger = logging.getLogger(__name__)


async def get_crypto() -> CryptoResponse:
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={COINS}&vs_currencies={CURRENCY}"
    try:
        response = await client.get(url)
        response.raise_for_status()
        data = response.json()
        return CryptoResponse(
            btc=data["bitcoin"]["rub"],
            eth=data["ethereum"]["rub"],
            usdt=data["tether"]["rub"],
        )
    except Exception as e:
        logger.error(f"Ошибка при получении курса криптовалют: {e}")
        return CryptoResponse(btc=0.0, eth=0.0, usdt=0.0)
