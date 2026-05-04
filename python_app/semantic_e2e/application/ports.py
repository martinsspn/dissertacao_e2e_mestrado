from __future__ import annotations

from pathlib import Path
from typing import Protocol

from semantic_e2e.domain.models import GeneratedTest, NavigationGraph, SpecPlan


class SpecRepository(Protocol):
    def list_specs(self, specs_dir: Path) -> list[Path]:
        ...

    def load(self, path: Path) -> SpecPlan:
        ...


class NavigationGraphRepository(Protocol):
    def get_navigation_graph(self, max_edges: int) -> NavigationGraph:
        ...

    def close(self) -> None:
        ...


class TestGenerator(Protocol):
    @property
    def model(self) -> str:
        ...

    def generate(self, spec: SpecPlan, graph: NavigationGraph) -> str:
        ...


class GeneratedTestWriter(Protocol):
    def write(self, output_dir: Path, generated_test: GeneratedTest) -> Path:
        ...

    def write_summary(self, output_dir: Path, results: list[dict[str, str]]) -> Path:
        ...
