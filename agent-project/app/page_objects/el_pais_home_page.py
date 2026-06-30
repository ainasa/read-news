from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable
import xml.etree.ElementTree as ET

import requests
from bs4 import BeautifulSoup, Tag

from app.errors import NetworkFetchError


@dataclass(frozen=True)
class FeedEntry:
    title: str


class ElPaisHomePage:
    """Page Object for the El Pais home page.

    Encapsulates URL loading and headline-related selectors.
    """

    HEADLINE_SELECTORS: tuple[str, ...] = (
        "h1 a",
        "h2 a",
        "h3 a",
        "article h2",
        "article h3",
        "[data-dtm-region] h2 a",
    )
    FALLBACK_FEED_URLS: tuple[str, ...] = (
        "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/portada",
    )

    def __init__(self, url: str, timeout_seconds: int = 20) -> None:
        self.url = url
        self.timeout_seconds = timeout_seconds

    def fetch_document(self) -> BeautifulSoup:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/126.0 Safari/537.36"
            )
        }
        try:
            response = requests.get(self.url, timeout=self.timeout_seconds, headers=headers)
            response.raise_for_status()
        except requests.RequestException as exc:
            raise NetworkFetchError(
                f"No se pudo acceder a la URL {self.url}: {exc}"
            ) from exc
        return BeautifulSoup(response.text, "html.parser")

    def fetch_fallback_feed_entries(self) -> list[FeedEntry]:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/126.0 Safari/537.36"
            )
        }
        for feed_url in self.FALLBACK_FEED_URLS:
            try:
                response = requests.get(feed_url, timeout=self.timeout_seconds, headers=headers)
                response.raise_for_status()
                root = ET.fromstring(response.text)
                entries: list[FeedEntry] = []
                for item in root.findall("./channel/item"):
                    title_node = item.find("title")
                    if title_node is None or title_node.text is None:
                        continue
                    title = self.normalize_text(title_node.text)
                    if title:
                        entries.append(FeedEntry(title=title))
                if entries:
                    return entries
            except (requests.RequestException, ET.ParseError):
                continue
        return []

    def find_headline_elements(self, document: BeautifulSoup) -> list[Tag]:
        elements: list[Tag] = []
        for selector in self.HEADLINE_SELECTORS:
            elements.extend(document.select(selector))
        return elements

    @staticmethod
    def normalize_text(raw_text: str) -> str:
        text = " ".join(raw_text.split())
        return text.strip()

    def extract_candidate_texts(self, document: BeautifulSoup) -> Iterable[str]:
        for element in self.find_headline_elements(document):
            text = self.normalize_text(element.get_text(" ", strip=True))
            if text and len(text) >= 20:
                yield text
