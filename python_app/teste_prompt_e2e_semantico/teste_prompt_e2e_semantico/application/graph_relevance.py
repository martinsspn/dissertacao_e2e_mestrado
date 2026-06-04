from __future__ import annotations

from teste_prompt_e2e_semantico.application.selector_policy import selector_candidates_for, selector_quality_score
from teste_prompt_e2e_semantico.application.text_normalization import matching_terms, text_relevance_score
from teste_prompt_e2e_semantico.domain.models import (
    NavigationGraph,
    NavigationTransition,
    NormalizedSpec,
    ScoredPage,
    ScoredTransition,
)


def rank_pages(graph: NavigationGraph, spec: NormalizedSpec, limit: int) -> list[ScoredPage]:
    scored = [_score_page(page, spec) for page in graph.pages]
    scored.sort(key=lambda item: (item.score, item.page.state_count), reverse=True)
    return [item for item in scored if item.score > 0][:limit] or scored[: min(limit, len(scored))]


def rank_transitions(
    graph: NavigationGraph,
    spec: NormalizedSpec,
    page_scores: dict[str, float],
    limit: int,
) -> list[ScoredTransition]:
    scored = [_score_transition(transition, spec, page_scores) for transition in graph.transitions]
    scored.sort(key=lambda item: item.score, reverse=True)
    return [item for item in scored if item.score > 0][:limit] or scored[: min(limit, len(scored))]


def _score_page(page, spec: NormalizedSpec) -> ScoredPage:
    fields = [
        (page.title, 3.0),
        (page.h1, 3.0),
        (page.url, 2.0),
        (page.visible_text_excerpt, 1.5),
    ]
    score = 0.0
    terms: set[str] = set()
    for text, weight in fields:
        field_score, matches = text_relevance_score(spec.terms, text, weight)
        score += field_score
        terms.update(matches)

    score += min(page.state_count, 10) * 0.01
    score += min(page.interactive_count, 20) * 0.005
    return ScoredPage(page=page, score=score, matched_terms=sorted(terms))


def _score_transition(
    transition: NavigationTransition,
    spec: NormalizedSpec,
    page_scores: dict[str, float],
) -> ScoredTransition:
    element = transition.element
    fields = [
        (element.get("text", ""), 4.0),
        (element.get("aria_label", ""), 4.0),
        (element.get("name", ""), 2.5),
        (element.get("role", ""), 2.0),
        (element.get("href", ""), 2.0),
        (transition.action, 1.5),
        (transition.interaction_kind, 1.0),
        (transition.target.get("title", ""), 2.5),
        (transition.target.get("url", ""), 1.5),
    ]

    score = 0.0
    terms: set[str] = set()
    for text, weight in fields:
        field_score, matches = text_relevance_score(spec.terms, text, weight)
        score += field_score
        terms.update(matches)

    phrase_bonus = _phrase_bonus(spec.phrases, transition)
    target_score = page_scores.get(transition.target.get("url", ""), 0.0)
    source_score = page_scores.get(transition.source.get("url", ""), 0.0)
    quality = selector_quality_score(transition)
    score += phrase_bonus + (target_score * 0.35) + (source_score * 0.15) + (quality * 0.4)
    if transition.action.lower() == "reload":
        score -= 0.8

    candidates = selector_candidates_for(transition)
    return ScoredTransition(
        transition=transition,
        score=score,
        matched_terms=sorted(terms),
        selector_candidates=candidates,
    )


def _phrase_bonus(phrases: list[str], transition: NavigationTransition) -> float:
    haystack = " ".join(
        [
            transition.element.get("text", ""),
            transition.element.get("aria_label", ""),
            transition.element.get("href", ""),
            transition.target.get("title", ""),
            transition.target.get("url", ""),
        ]
    )
    matches = matching_terms([phrase.replace(" ", "") for phrase in phrases], haystack.replace(" ", ""))
    return min(len(matches) * 0.2, 1.0)
