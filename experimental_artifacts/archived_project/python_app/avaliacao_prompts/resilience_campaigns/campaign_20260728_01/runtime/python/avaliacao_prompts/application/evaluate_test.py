from __future__ import annotations

from pathlib import Path

from avaliacao_prompts.application.graph_conformance import analyze_graph_conformance
from avaliacao_prompts.application.static_analysis import analyze_static_test_source
from avaliacao_prompts.domain.models import EvaluationCase, EvaluationReport, GraphEvidence, PromptMetrics


def evaluate_test_file(case: EvaluationCase, graph: GraphEvidence | None = None) -> EvaluationReport:
    static_analysis = analyze_static_test_source(_read_test_source(case.test_file))
    graph_conformance = (
        analyze_graph_conformance(static_analysis, graph, case.base_url)
        if graph is not None
        else None
    )
    return EvaluationReport(
        case=case,
        static_analysis=static_analysis,
        prompt_metrics=_prompt_metrics(case.prompt_file),
        graph_conformance=graph_conformance,
    )


def _read_test_source(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _prompt_metrics(path: Path | None) -> PromptMetrics | None:
    if path is None or not path.exists():
        return None
    prompt = path.read_text(encoding="utf-8")
    return PromptMetrics(character_count=len(prompt), line_count=len(prompt.splitlines()))
