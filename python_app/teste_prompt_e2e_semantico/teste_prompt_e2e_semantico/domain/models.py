from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class PageNode:
    id: str
    url: str
    title: str
    state_count: int = 1
    h1: str = ""
    visible_text_excerpt: str = ""
    interactive_count: int = 0
    screenshot_path: str = ""


@dataclass(frozen=True)
class NavigationTransition:
    source: dict[str, str]
    target: dict[str, str]
    action: str
    interaction_kind: str
    element: dict[str, str]
    selectors: dict[str, object] = field(default_factory=dict)
    selector_scores: dict[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class NavigationGraph:
    pages: list[PageNode]
    transitions: list[NavigationTransition]


@dataclass(frozen=True)
class SpecPlan:
    source_path: Path
    raw_text: str
    title: str


@dataclass(frozen=True)
class NormalizedSpec:
    raw_text: str
    terms: list[str]
    phrases: list[str]


@dataclass(frozen=True)
class SelectorCandidate:
    kind: str
    value: str
    score: float
    strength: str
    reason: str


@dataclass(frozen=True)
class ScoredPage:
    page: PageNode
    score: float
    matched_terms: list[str]


@dataclass(frozen=True)
class ScoredTransition:
    transition: NavigationTransition
    score: float
    matched_terms: list[str]
    selector_candidates: list[SelectorCandidate]


@dataclass(frozen=True)
class PathStep:
    source_url: str
    target_url: str
    action: str
    interaction_kind: str
    element: dict[str, str]
    recommended_selectors: list[SelectorCandidate]


@dataclass(frozen=True)
class PathCandidate:
    id: str
    score: float
    steps: list[PathStep]


@dataclass(frozen=True)
class RelevantGraphContext:
    pages: list[ScoredPage]
    transitions: list[ScoredTransition]
    paths: list[PathCandidate]


@dataclass(frozen=True)
class GeneratedPrompt:
    spec: SpecPlan
    prompt: str
    graph_pages: int
    graph_transitions: int
    relevant_pages: int
    relevant_transitions: int
    candidate_paths: int
