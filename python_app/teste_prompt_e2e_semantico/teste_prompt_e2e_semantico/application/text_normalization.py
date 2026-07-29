from __future__ import annotations

import re
import unicodedata


_STOPWORDS = {
    "a", "ao", "aos", "as", "com", "como", "da", "das", "de", "deve", "do", "dos", "e",
    "em", "essa", "esse", "esta", "este", "isso", "na", "nas", "no", "nos", "o", "os", "ou",
    "para", "pela", "pelo", "que", "se", "ser", "sua", "suas", "seu", "seus", "um", "uma",
    "usuario", "usuaria", "user", "the", "and", "or", "to", "of", "in", "on", "for", "with",
    "should", "must",
}


def normalize_text(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text or "")
    without_marks = "".join(char for char in normalized if not unicodedata.combining(char))
    return without_marks.lower()


def tokenize(text: str) -> list[str]:
    normalized = normalize_text(text)
    raw_terms = re.findall(r"[a-z0-9][a-z0-9_-]{1,}", normalized)
    return [term for term in raw_terms if term not in _STOPWORDS and len(term) > 1]


def matching_terms(query_terms: list[str], text: str) -> list[str]:
    text_terms = set(tokenize(text))
    return [term for term in query_terms if term in text_terms]
