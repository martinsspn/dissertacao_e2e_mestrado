from __future__ import annotations

import re

from avaliacao_prompts.domain.models import GraphConformanceResult, GraphEvidence, StaticAnalysisResult


def analyze_graph_conformance(
    static_analysis: StaticAnalysisResult,
    graph: GraphEvidence,
    base_url: str,
) -> GraphConformanceResult:
    known_urls = {_normalize_url(base_url), *(_normalize_url(url) for url in graph.urls)}
    known_urls.discard("")
    unknown_urls = [
        url
        for url in static_analysis.goto_urls
        if _normalize_goto_url(url, base_url) not in known_urls
    ]

    haystack = _normalize_text(" ".join([*graph.urls, *graph.texts]))
    unknown_locator_texts = [
        text for text in static_analysis.locator_texts if not _text_is_supported_by_graph(text, haystack)
    ]
    return GraphConformanceResult(
        graph_url_coverage=_coverage(len(static_analysis.goto_urls), len(unknown_urls)),
        unknown_urls=unknown_urls,
        locator_text_coverage=_coverage(len(static_analysis.locator_texts), len(unknown_locator_texts)),
        unknown_locator_texts=unknown_locator_texts,
    )


def _text_is_supported_by_graph(text: str, haystack: str) -> bool:
    normalized = _normalize_text(text)
    if len(normalized) < 3 or normalized in haystack:
        return True
    terms = [term for term in re.findall(r"[a-z0-9]{3,}", normalized) if term not in {"http", "https", "www"}]
    if not terms:
        return True
    return sum(1 for term in terms if term in haystack) / len(terms) >= 0.6


def _normalize_goto_url(value: str, base_url: str) -> str:
    if value.strip().startswith("/"):
        return _normalize_url(base_url) + value.strip()
    return _normalize_url(value)


def _normalize_url(value: str) -> str:
    return value.strip().rstrip("/")


def _normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip().lower()


def _coverage(total: int, misses: int) -> float:
    return 1.0 if total == 0 else round((total - misses) / total, 3)
