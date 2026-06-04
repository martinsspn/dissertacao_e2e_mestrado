from __future__ import annotations

import re

from teste_prompt_e2e_semantico.domain.models import NavigationGraph
from teste_prompt_e2e_semantico.evaluation.domain.models import GraphConformanceResult, StaticAnalysisResult


def analyze_graph_conformance(
    static_analysis: StaticAnalysisResult,
    graph: NavigationGraph,
    base_url: str,
) -> GraphConformanceResult:
    known_urls = _known_urls(graph, base_url)
    unknown_urls = []
    for url in static_analysis.goto_urls:
        normalized_url = _normalize_goto_url(url, base_url)
        if normalized_url not in known_urls and not _is_same_origin(normalized_url, base_url):
            unknown_urls.append(url)
    graph_url_coverage = _coverage(total=len(static_analysis.goto_urls), misses=len(unknown_urls))

    haystack = _graph_text_haystack(graph)
    unknown_locator_texts = [
        text for text in static_analysis.locator_texts if not _text_is_supported_by_graph(text, haystack)
    ]
    locator_text_coverage = _coverage(total=len(static_analysis.locator_texts), misses=len(unknown_locator_texts))

    return GraphConformanceResult(
        graph_url_coverage=graph_url_coverage,
        unknown_urls=unknown_urls,
        locator_text_coverage=locator_text_coverage,
        unknown_locator_texts=unknown_locator_texts,
    )


def _known_urls(graph: NavigationGraph, base_url: str) -> set[str]:
    urls = {_normalize_url(base_url)}
    for page in graph.pages:
        urls.add(_normalize_url(page.url))
    for transition in graph.transitions:
        urls.add(_normalize_url(transition.source.get("url", "")))
        urls.add(_normalize_url(transition.target.get("url", "")))
    return {url for url in urls if url}


def _graph_text_haystack(graph: NavigationGraph) -> str:
    fragments: list[str] = []
    for page in graph.pages:
        fragments.extend([page.url, page.title, page.h1, page.visible_text_excerpt])
    for transition in graph.transitions:
        fragments.extend(transition.source.values())
        fragments.extend(transition.target.values())
        fragments.extend(str(value) for value in transition.element.values())
        fragments.extend(str(value) for value in transition.selectors.values())
    return _normalize_text(" ".join(fragments))


def _text_is_supported_by_graph(text: str, haystack: str) -> bool:
    normalized = _normalize_text(text)
    if len(normalized) < 3:
        return True
    if normalized in haystack:
        return True
    terms = [term for term in re.findall(r"[a-z0-9]{3,}", normalized) if term not in {"http", "https", "www"}]
    if not terms:
        return True
    matched = sum(1 for term in terms if term in haystack)
    return matched / len(terms) >= 0.6


def _is_same_origin(url: str, base_url: str) -> bool:
    normalized_url = _normalize_url(url)
    normalized_base = _normalize_url(base_url)
    return bool(normalized_url and normalized_base and normalized_url.startswith(normalized_base + "/"))


def _normalize_goto_url(value: str, base_url: str) -> str:
    text = value.strip()
    if text.startswith("/"):
        return _normalize_url(base_url) + text
    return _normalize_url(text)


def _normalize_url(value: str) -> str:
    return value.strip().rstrip("/")


def _normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip().lower()


def _coverage(total: int, misses: int) -> float:
    if total == 0:
        return 1.0
    return round((total - misses) / total, 3)
