from typing import List
from app.utils.constants import NEWS_URL
import feedparser  # type: ignore
import logging
from app.models.schemas import NewsResponse

logger = logging.getLogger(__name__)


async def get_news_titles() -> NewsResponse:
    try:
        feed = feedparser.parse(NEWS_URL)
        titles: List[str] = [
            entry.title for entry in feed.entries[:5] if isinstance(entry.title, str)
        ]
        return NewsResponse(articles=titles)
    except Exception as e:
        logger.error(f"Ошибка при получении новостей: {e}")
        return NewsResponse(articles=[])
