from typing import List
from redis.asyncio import Redis
from app.utils.cache import cache
from app.utils.constants import NEWS_URL
import feedparser  # type: ignore
import logging
from app.models.schemas import Article, NewsResponse

logger = logging.getLogger(__name__)


@cache(ttl=600)
async def get_news_titles(redis: Redis) -> NewsResponse:
    try:
        feed = feedparser.parse(NEWS_URL)
        articles: List[Article] = []
        for entry in feed.entries[:5]:
            if not isinstance(entry.title, str):
                continue
            link = getattr(entry, "link", "")
            if isinstance(link, list):
                link = link[0] if link else ""
            elif not isinstance(link, str):
                link = str(link)

            articles.append(Article(title=entry.title, link=link))
        return NewsResponse(articles=articles)
    except Exception as e:
        logger.error(f"Ошибка при получении новостей: {e}")
        return NewsResponse(articles=[])
