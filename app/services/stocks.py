import logging
import yfinance as yf  # type: ignore
from redis.asyncio import Redis
from app.models.schemas import StockResponse
from typing import Dict, Optional
from app.utils.cache import cache
from app.utils.constants import SYMBOLS

logger = logging.getLogger(__name__)


@cache(ttl=1800)
async def get_stock_indexes(redis: Redis) -> StockResponse:
    results: Dict[str, Optional[float]] = {}
    for name, symbol in SYMBOLS.items():
        results[name] = await fetch_latest_close_price(symbol)
    return StockResponse(**results)


async def fetch_latest_close_price(symbol: str) -> Optional[float]:
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period="5d")
        if df.empty or "Close" not in df:
            logger.warning(f"No data returned for {symbol}")
            return None
        price = df["Close"].dropna().iloc[-1]
        return round(price, 2)
    except Exception as e:
        logger.error(f"Error fetching data for {symbol}: {e}")
        return None
