import feedparser
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)

class MediumRSSExtractor:
    def __init__(self, base_rss: str, tags: list[str]):
        self.base_rss = base_rss
        self.tags = tags
        if not base_rss.startswith("http"):
            raise ValueError("base_rss debe ser una URL válida.")

    def fetch(self) -> list[dict]:

        """
        Extrae artículos desde feeds RSS de Medium.

        Returns
        -------
        list[dict]
            Lista de artículos con metadata normalizada.
        """

        rows = []

        for feed_tag in self.tags:
            try:
                feed = feedparser.parse(self.base_rss + feed_tag)

            except Exception as e:
                logger.error(f"Error al procesar feed: {feed_tag} - {e}")
                continue

            if feed.bozo:
                logger.warning(f"Feed con advertencia: {feed_tag} - {feed.bozo_exception}")

            for entry in feed.entries:
                rows.append({
                    "title": getattr(entry, "title", None),
                    "link": getattr(entry, "link", None),
                    "published": getattr(entry, "published", None),
                    "feed_tag": feed_tag,
                    "article_tags": [t.term for t in getattr(entry, "tags", [])],
                    "source": "medium",
                    "ingestion_date": datetime.now(timezone.utc).date().isoformat()
                })

        return rows