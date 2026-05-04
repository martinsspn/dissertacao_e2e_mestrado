from __future__ import annotations

from pathlib import Path

from semantic_e2e.application.ports import (
    GeneratedTestWriter,
    NavigationGraphRepository,
    SpecRepository,
    TestGenerator,
)
from semantic_e2e.domain.models import GeneratedTest


class GenerateTestsUseCase:
    def __init__(
        self,
        spec_repository: SpecRepository,
        graph_repository: NavigationGraphRepository,
        test_generator: TestGenerator,
        test_writer: GeneratedTestWriter,
        graph_max_edges: int,
    ) -> None:
        self._spec_repository = spec_repository
        self._graph_repository = graph_repository
        self._test_generator = test_generator
        self._test_writer = test_writer
        self._graph_max_edges = graph_max_edges

    def execute(self, specs_dir: Path, output_dir: Path) -> list[dict[str, str]]:
        graph = self._graph_repository.get_navigation_graph(self._graph_max_edges)
        results: list[dict[str, str]] = []

        for spec_path in self._spec_repository.list_specs(specs_dir):
            spec = self._spec_repository.load(spec_path)
            code = self._test_generator.generate(spec, graph)
            generated_test = GeneratedTest(
                spec=spec,
                code=code,
                model=self._test_generator.model,
                graph_pages=len(graph.pages),
                graph_transitions=len(graph.transitions),
            )
            output_path = self._test_writer.write(output_dir, generated_test)

            results.append(
                {
                    "spec": str(spec_path),
                    "output": str(output_path),
                    "model": generated_test.model,
                    "graph_pages": str(generated_test.graph_pages),
                    "graph_transitions": str(generated_test.graph_transitions),
                }
            )

        self._test_writer.write_summary(output_dir, results)
        return results
