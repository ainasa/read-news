from __future__ import annotations

from deep_translator import GoogleTranslator

from app.errors import TranslationError


class HeadlineTranslatorService:
    """Translates headline lists to a target language."""

    def __init__(self, target_language: str = "es") -> None:
        self.target_language = target_language

    def translate_many(self, headlines: list[str]) -> list[str]:
        if not headlines:
            return []

        translator = GoogleTranslator(source="auto", target=self.target_language)
        translated: list[str] = []
        for headline in headlines:
            try:
                translated_text = translator.translate(headline)
            except Exception as exc:
                raise TranslationError(
                    f"No se pudo traducir el titular '{headline[:60]}...': {exc}"
                ) from exc
            translated.append((translated_text or "").strip() or headline)

        return translated
