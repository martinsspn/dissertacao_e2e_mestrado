import tempfile
import unittest
from pathlib import Path

from avaliacao_prompts.domain.models import (
    EvaluationCase,
    EvaluationReport,
    GraphConformanceResult,
    StaticAnalysisResult,
)
from avaliacao_prompts.infrastructure.markdown_reports import MarkdownEvaluationReportWriter


class MarkdownEvaluationReportWriterTest(unittest.TestCase):
    def test_report_explains_metrics_and_exposes_evidence_in_portuguese(self) -> None:
        report = EvaluationReport(
            case=EvaluationCase(
                spec_id="checkout",
                approach="structured_context",
                test_file=Path("checkout.spec.ts"),
                base_url="https://example.test/",
            ),
            static_analysis=StaticAnalysisResult(
                has_playwright_import=True,
                has_test_block=True,
                has_expect_assertion=False,
                uses_wait_for_timeout=True,
                goto_urls=["https://example.test/invented"],
                locator_texts=["Finalizar compra"],
                locator_count=1,
                action_count=2,
                selector_risk="high",
            ),
            graph_conformance=GraphConformanceResult(
                graph_url_coverage=0.0,
                unknown_urls=["https://example.test/invented"],
                locator_text_coverage=0.0,
                unknown_locator_texts=["Finalizar compra"],
            ),
        )

        with tempfile.TemporaryDirectory() as directory:
            path = MarkdownEvaluationReportWriter().write(Path(directory) / "report.md", [report])
            content = path.read_text(encoding="utf-8")

        self.assertIn("# Relatório auxiliar de avaliação", content)
        self.assertIn("## Visão geral", content)
        self.assertIn("Como interpretar", content)
        self.assertIn("Nenhuma asserção foi identificada", content)
        self.assertIn("https://example.test/invented", content)
        self.assertIn("Rubrica para avaliação humana", content)
