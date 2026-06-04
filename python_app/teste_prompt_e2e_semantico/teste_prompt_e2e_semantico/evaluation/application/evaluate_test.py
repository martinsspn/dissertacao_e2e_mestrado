from __future__ import annotations

from pathlib import Path

from teste_prompt_e2e_semantico.domain.models import NavigationGraph
from teste_prompt_e2e_semantico.evaluation.application.graph_conformance import analyze_graph_conformance
from teste_prompt_e2e_semantico.evaluation.application.static_analysis import analyze_static_test_source
from teste_prompt_e2e_semantico.evaluation.domain.models import EvaluationCase, EvaluationReport


def evaluate_test_file(
    case: EvaluationCase,
    graph: NavigationGraph | None = None,
) -> EvaluationReport:
    source = _read_test_source(case.test_file)
    static_analysis = analyze_static_test_source(source)
    graph_conformance = (
        analyze_graph_conformance(static_analysis, graph, case.base_url)
        if graph is not None
        else None
    )

    return EvaluationReport(
        case=case,
        static_analysis=static_analysis,
        graph_conformance=graph_conformance,
    )


def _read_test_source(path: Path) -> str:
    return path.read_text(encoding="utf-8")
