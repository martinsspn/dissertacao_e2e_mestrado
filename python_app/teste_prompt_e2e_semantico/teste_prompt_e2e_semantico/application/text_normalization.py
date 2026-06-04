from __future__ import annotations

import re
import unicodedata

from teste_prompt_e2e_semantico.domain.models import NormalizedSpec


_STOPWORDS = {
    "a",
    "ao",
    "aos",
    "as",
    "com",
    "como",
    "da",
    "das",
    "de",
    "deve",
    "do",
    "dos",
    "e",
    "em",
    "essa",
    "esse",
    "esta",
    "este",
    "isso",
    "na",
    "nas",
    "no",
    "nos",
    "o",
    "os",
    "ou",
    "para",
    "pela",
    "pelo",
    "que",
    "se",
    "ser",
    "sua",
    "suas",
    "seu",
    "seus",
    "um",
    "uma",
    "usuario",
    "usuaria",
    "user",
    "the",
    "and",
    "or",
    "to",
    "of",
    "in",
    "on",
    "for",
    "with",
    "should",
    "must",
}


def normalize_spec(text: str) -> NormalizedSpec:
    terms = unique_terms(tokenize(text))
    return NormalizedSpec(raw_text=text, terms=terms, phrases=_phrases(terms))


def normalize_text(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text or "")
    without_marks = "".join(char for char in normalized if not unicodedata.combining(char))
    return without_marks.lower()


def tokenize(text: str) -> list[str]:
    normalized = normalize_text(text)
    raw_terms = re.findall(r"[a-z0-9][a-z0-9_-]{1,}", normalized)
    return [term for term in raw_terms if term not in _STOPWORDS and len(term) > 1]


def unique_terms(terms: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for term in terms:
        if term not in seen:
            seen.add(term)
            result.append(term)
    return result


def matching_terms(query_terms: list[str], text: str) -> list[str]:
    text_terms = set(tokenize(text))
    normalized_text = normalize_text(text)
    matches: list[str] = []
    for term in query_terms:
        if term in text_terms or (len(term) >= 4 and term in normalized_text):
            matches.append(term)
    return matches


def text_relevance_score(query_terms: list[str], text: str, weight: float = 1.0) -> tuple[float, list[str]]:
    matches = matching_terms(query_terms, text)
    if not query_terms:
        return 0.0, []
    coverage = len(matches) / max(1, len(query_terms))
    density = len(matches) / max(1, len(tokenize(text)))
    return weight * ((coverage * 0.7) + (density * 0.3)), matches


def _phrases(terms: list[str]) -> list[str]:
    phrases: list[str] = []
    for size in (3, 2):
        for index in range(0, max(0, len(terms) - size + 1)):
            phrases.append(" ".join(terms[index : index + size]))
    return phrases[:20]
