from __future__ import annotations

from collections import defaultdict, deque

from teste_prompt_e2e_semantico.domain.models import (
    NavigationGraph,
    PathCandidate,
    PathStep,
    ScoredPage,
    ScoredTransition,
)


def rank_candidate_paths(
    graph: NavigationGraph,
    base_url: str,
    pages: list[ScoredPage],
    transitions: list[ScoredTransition],
    max_depth: int,
    limit: int,
) -> list[PathCandidate]:
    if not graph.transitions:
        return []

    all_ranked_transitions = {
        (
            transition.transition.source.get("url", ""),
            transition.transition.target.get("url", ""),
            transition.transition.action,
            transition.transition.element.get("text", ""),
        ): transition
        for transition in transitions
    }

    adjacency: dict[str, list[ScoredTransition]] = defaultdict(list)
    for transition in graph.transitions:
        identity = (
            transition.source.get("url", ""),
            transition.target.get("url", ""),
            transition.action,
            transition.element.get("text", ""),
        )
        scored = all_ranked_transitions.get(identity)
        if scored is not None and _is_actionable_transition(scored):
            adjacency[transition.source.get("url", "")].append(scored)

    for source in adjacency:
        adjacency[source].sort(key=lambda item: item.score, reverse=True)

    starts = _start_urls(graph, base_url)
    targets = [
        page.page.url
        for page in pages[: max(3, min(len(pages), limit))]
        if page.page.url not in starts
    ]
    page_score_by_url = {page.page.url: page.score for page in pages}

    candidates: list[PathCandidate] = []
    seen_paths: set[tuple[str, ...]] = set()

    for start in starts:
        queue = deque([(start, [])])
        while queue and len(candidates) < limit * 8:
            current_url, path = queue.popleft()
            if len(path) >= max_depth:
                continue

            for transition in adjacency.get(current_url, [])[:12]:
                target_url = transition.transition.target.get("url", "")
                if target_url == current_url:
                    continue
                if any(step.transition.target.get("url", "") == target_url for step in path):
                    continue

                next_path = path + [transition]
                path_key = tuple(item.transition.target.get("url", "") for item in next_path)
                if path_key in seen_paths:
                    continue
                seen_paths.add(path_key)

                if target_url in targets:
                    candidates.append(_build_path_candidate(next_path, page_score_by_url, len(candidates) + 1))

                queue.append((target_url, next_path))

    candidates.sort(key=lambda item: item.score, reverse=True)
    return _diversify_by_final_target(candidates, limit)


def _start_urls(graph: NavigationGraph, base_url: str) -> list[str]:
    normalized_base = base_url.rstrip("/")
    pages_by_url = {page.url.rstrip("/"): page for page in graph.pages}
    if normalized_base in pages_by_url:
        return [pages_by_url[normalized_base].url]

    incoming: set[str] = {transition.target.get("url", "") for transition in graph.transitions}
    roots = [page.url for page in graph.pages if page.url not in incoming]
    if roots:
        return roots[:3]

    return [page.url for page in sorted(graph.pages, key=lambda page: page.state_count, reverse=True)[:3]]


def _build_path_candidate(path: list[ScoredTransition], page_score_by_url: dict[str, float], index: int) -> PathCandidate:
    final_transition = path[-1]
    final_target_score = page_score_by_url.get(final_transition.transition.target.get("url", ""), 0.0)
    average_transition_score = sum(item.score for item in path) / max(1, len(path))
    selector_score = sum(
        item.selector_candidates[0].score if item.selector_candidates else 0.0
        for item in path
    ) / max(1, len(path))
    depth_penalty = max(0, len(path) - 1) * 1.15
    score = (final_target_score * 2.0) + final_transition.score + average_transition_score + (selector_score * 0.4) - depth_penalty

    steps = [
        PathStep(
            source_url=item.transition.source.get("url", ""),
            target_url=item.transition.target.get("url", ""),
            action=item.transition.action,
            interaction_kind=item.transition.interaction_kind,
            element=item.transition.element,
            recommended_selectors=item.selector_candidates[:3],
        )
        for item in path
    ]
    return PathCandidate(id=f"path_{index:03d}", score=score, steps=steps)


def _diversify_by_final_target(candidates: list[PathCandidate], limit: int) -> list[PathCandidate]:
    selected: list[PathCandidate] = []
    used_targets: set[str] = set()

    for candidate in candidates:
        final_target = candidate.steps[-1].target_url if candidate.steps else ""
        if final_target and final_target not in used_targets:
            selected.append(candidate)
            used_targets.add(final_target)
        if len(selected) >= limit:
            return selected

    for candidate in candidates:
        if candidate not in selected:
            selected.append(candidate)
        if len(selected) >= limit:
            return selected

    return selected


def _is_actionable_transition(transition: ScoredTransition) -> bool:
    source_url = transition.transition.source.get("url", "")
    target_url = transition.transition.target.get("url", "")
    if not source_url or not target_url or source_url == target_url:
        return False
    if transition.transition.action.lower() == "reload":
        return False
    return any(candidate.score >= 0.4 for candidate in transition.selector_candidates)
