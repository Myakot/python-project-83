from page_analyzer.app import app # noqa F401
from page_analyzer.validator import url_validator, url_normalize


__all__ = (
    'app',
    'url_validator',
    'url_normalize'
)
