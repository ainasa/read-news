class FeatureError(Exception):
    """Base exception for the feature workflow."""


class NetworkFetchError(FeatureError):
    """Raised when the target page cannot be fetched."""


class ScrapingError(FeatureError):
    """Raised when expected headlines are not found."""


class PdfGenerationError(FeatureError):
    """Raised when PDF generation fails."""


class TranslationError(FeatureError):
    """Raised when headline translation fails."""
