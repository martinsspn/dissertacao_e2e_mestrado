import unittest

from avaliacao_prompts.application.graph_conformance import analyze_graph_conformance
from avaliacao_prompts.domain.models import GraphEvidence, StaticAnalysisResult


class GraphConformanceTest(unittest.TestCase):
    def test_same_origin_route_absent_from_graph_is_unknown(self) -> None:
        graph = GraphEvidence(urls=["https://example.test/"], texts=["Home"])
        analysis = StaticAnalysisResult(
            has_playwright_import=True,
            has_test_block=True,
            has_expect_assertion=True,
            uses_wait_for_timeout=False,
            goto_urls=["https://example.test/invented"],
        )

        result = analyze_graph_conformance(analysis, graph, "https://example.test/")

        self.assertEqual(result.unknown_urls, ["https://example.test/invented"])
        self.assertEqual(result.graph_url_coverage, 0.0)
