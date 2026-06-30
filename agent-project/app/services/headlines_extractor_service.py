from __future__ import annotations

from app.errors import NetworkFetchError, ScrapingError
from app.page_objects.el_pais_home_page import ElPaisHomePage


class HeadlinesExtractorService:
    """Uses the page object to extract a deduplicated headline list."""

    def __init__(self, page: ElPaisHomePage) -> None:
        self.page = page

    def get_headlines(self, max_headlines: int = 25) -> list[str]:
        candidates: list[str] = []
        try:
            document = self.page.fetch_document()
            candidates = list(self.page.extract_candidate_texts(document))
        except NetworkFetchError:
            # If homepage fetch is blocked, fallback feed is attempted below.
            candidates = []

        if not candidates:
            candidates = [entry.title for entry in self.page.fetch_fallback_feed_entries()]

        deduplicated: list[str] = []
        seen: set[str] = set()
        for item in candidates:
            key = item.casefold()
            if key in seen:
                continue
            seen.add(key)
            deduplicated.append(item)
            if len(deduplicated) >= max_headlines:
                break

        if not deduplicated:
            raise ScrapingError(
                "No se encontraron titulares con los selectores definidos en la pagina objetivo."
            )

        return deduplicated
