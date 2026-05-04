from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class PageNode:
    id: str
    url: str
    title: str
    state_count: int = 1


@dataclass(frozen=True)
class NavigationTransition:
    source: dict[str, str]
    target: dict[str, str]
    action: str
    interaction_kind: str
    element: dict[str, str]
    selectors: dict[str, Any] = field(default_factory=dict)
    selector_scores: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class NavigationGraph:
    pages: list[PageNode]
    transitions: list[NavigationTransition]

    def to_prompt_context(self) -> dict[str, Any]:
        return {
            "pages": [page.__dict__ for page in self.pages],
            "transitions": [
                {
                    "source": transition.source,
                    "target": transition.target,
                    "action": transition.action,
                    "interaction_kind": transition.interaction_kind,
                    "element": transition.element,
                    "selectors": transition.selectors,
                    "selector_scores": transition.selector_scores,
                }
                for transition in self.transitions
            ],
        }


@dataclass(frozen=True)
class SpecPlan:
    source_path: Path
    raw_text: str
    title: str


@dataclass(frozen=True)
class GeneratedTest:
    spec: SpecPlan
    code: str
    model: str
    graph_pages: int
    graph_transitions: int
