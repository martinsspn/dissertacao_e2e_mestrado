from __future__ import annotations

from pathlib import Path
from typing import Protocol

from teste_prompt_e2e_semantico.domain.models import GeneratedPrompt, NavigationGraph, SpecPlan


class SpecRepository(Protocol):
    def list_specs(self, specs_dir: Path) -> list[Path]:
        ...

    def load(self, path: Path) -> SpecPlan:
        ...


class NavigationGraphRepository(Protocol):
    def get_navigation_graph(self) -> NavigationGraph:
        ...

    def close(self) -> None:
        ...


class PromptWriter(Protocol):
    def prune_stale(self, output_dir: Path, active_spec_ids: set[str]) -> int:
        ...

    def write(self, output_dir: Path, generated_prompt: GeneratedPrompt) -> Path:
        ...

    def write_summary(self, output_dir: Path, results: list[dict[str, str]]) -> Path:
        ...
