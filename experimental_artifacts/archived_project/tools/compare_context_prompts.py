#!/usr/bin/env python3
"""Compare which specification steps received context in two prompt directories."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


STEP = re.compile(r"^(\d+)\. ", re.MULTILINE)
CONTEXT_STEP = re.compile(r"^Etapa (\d+) \(R\d+\):", re.MULTILINE)
SUFFIX = ".structured_context.prompt.md"


@dataclass(frozen=True)
class PromptSummary:
    total_steps: int
    context_steps: frozenset[int]


def read_directory(directory: Path) -> dict[str, PromptSummary]:
    summaries: dict[str, PromptSummary] = {}
    for path in sorted(directory.glob(f"*{SUFFIX}")):
        content = path.read_text(encoding="utf-8")
        summaries[path.name.removesuffix(SUFFIX)] = PromptSummary(
            total_steps=len(STEP.findall(content)),
            context_steps=frozenset(int(value) for value in CONTEXT_STEP.findall(content)),
        )
    return summaries


def format_steps(steps: set[int] | frozenset[int]) -> str:
    return ",".join(str(step) for step in sorted(steps)) or "-"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("before", type=Path)
    parser.add_argument("after", type=Path)
    args = parser.parse_args()

    before = read_directory(args.before)
    after = read_directory(args.after)
    scenarios = sorted(set(before) | set(after))

    print("| Cenario | Etapas | Antes | Depois | Adicionadas | Removidas |")
    print("|---|---:|---:|---:|---|---|")
    for scenario in scenarios:
        old = before.get(scenario, PromptSummary(0, frozenset()))
        new = after.get(scenario, PromptSummary(0, frozenset()))
        print(
            f"| {scenario} | {new.total_steps or old.total_steps} "
            f"| {len(old.context_steps)} | {len(new.context_steps)} "
            f"| {format_steps(new.context_steps - old.context_steps)} "
            f"| {format_steps(old.context_steps - new.context_steps)} |"
        )

    old_total = sum(len(item.context_steps) for item in before.values())
    new_total = sum(len(item.context_steps) for item in after.values())
    step_total = sum(item.total_steps for item in after.values())
    print()
    print(f"Etapas totais: {step_total}")
    print(f"Etapas com contexto antes: {old_total}")
    print(f"Etapas com contexto depois: {new_total}")
    print(f"Diferenca nominal: {new_total - old_total:+d}")


if __name__ == "__main__":
    main()
