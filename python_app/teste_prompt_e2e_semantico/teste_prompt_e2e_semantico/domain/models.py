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
    observed_result: ObservedResult | None = None


@dataclass(frozen=True)
class UiElement:
    page_url: str
    kind: str
    suggested_operation: str
    element: dict[str, str]
    selectors: dict[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class ObservedResult:
    text: str
    element_id: str = ""
    role: str = ""


@dataclass(frozen=True)
class NavigationGraph:
    pages: list[PageNode]
    transitions: list[NavigationTransition]
    ui_elements: list[UiElement] = field(default_factory=list)


@dataclass(frozen=True)
class SpecPlan:
    source_path: Path
    raw_text: str
    title: str


@dataclass(frozen=True)
class SpecificationStep:
    id: str
    text: str


@dataclass(frozen=True)
class SelectorCandidate:
    kind: str
    value: str


@dataclass(frozen=True)
class ContextElement:
    page_url: str
    action: str
    interaction_kind: str
    element: dict[str, str]
    selector: SelectorCandidate | None = None
    destination_url: str = ""


@dataclass(frozen=True)
class PageEvidence:
    page_url: str
    source: str
    text: str


@dataclass(frozen=True)
class InteractionContext:
    control: ContextElement
    observed_result: ObservedResult | None = None


@dataclass(frozen=True)
class StepContext:
    requirement_id: str
    interactions: tuple[InteractionContext, ...] = ()
    page_evidence: PageEvidence | None = None

    @property
    def controls(self) -> tuple[ContextElement, ...]:
        return tuple(interaction.control for interaction in self.interactions)

    @property
    def control(self) -> ContextElement | None:
        """Compatibility accessor for consumers that only need the first control."""
        return self.interactions[0].control if self.interactions else None

    @property
    def observed_result(self) -> ObservedResult | None:
        """Return the first observed result without losing per-control association."""
        return next(
            (
                interaction.observed_result
                for interaction in self.interactions
                if interaction.observed_result is not None
            ),
            None,
        )


@dataclass(frozen=True)
class StructuredContext:
    steps: list[StepContext]

    @property
    def item_count(self) -> int:
        return sum(
            len(step.interactions)
            + sum(
                int(interaction.observed_result is not None)
                for interaction in step.interactions
            )
            + int(step.page_evidence is not None)
            for step in self.steps
        )


@dataclass(frozen=True)
class GeneratedPrompt:
    spec: SpecPlan
    approach: str
    prompt: str
    requirement_count: int
    context_item_count: int
    character_count: int
