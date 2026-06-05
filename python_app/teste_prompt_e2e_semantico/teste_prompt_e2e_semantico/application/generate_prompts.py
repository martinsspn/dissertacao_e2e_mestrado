from __future__ import annotations

from pathlib import Path

from teste_prompt_e2e_semantico.application.graph_relevance import rank_pages, rank_transitions
from teste_prompt_e2e_semantico.application.path_ranking import rank_candidate_paths
from teste_prompt_e2e_semantico.application.ports import NavigationGraphRepository, PromptWriter, SpecRepository
from teste_prompt_e2e_semantico.application.prompt_builder import build_structured_prompt
from teste_prompt_e2e_semantico.application.spec_coverage import analyze_spec_coverage
from teste_prompt_e2e_semantico.application.text_normalization import normalize_spec
from teste_prompt_e2e_semantico.domain.models import GeneratedPrompt, RelevantGraphContext


class GeneratePromptsUseCase:
    def __init__(
        self,
        spec_repository: SpecRepository,
        graph_repository: NavigationGraphRepository,
        prompt_writer: PromptWriter,
        base_url: str,
        graph_max_edges: int,
        relevant_pages_limit: int,
        relevant_transitions_limit: int,
        candidate_paths_limit: int,
        max_path_depth: int,
    ) -> None:
        self._spec_repository = spec_repository
        self._graph_repository = graph_repository
        self._prompt_writer = prompt_writer
        self._base_url = base_url
        self._graph_max_edges = graph_max_edges
        self._relevant_pages_limit = relevant_pages_limit
        self._relevant_transitions_limit = relevant_transitions_limit
        self._candidate_paths_limit = candidate_paths_limit
        self._max_path_depth = max_path_depth

    def execute(self, specs_dir: Path, output_dir: Path) -> list[dict[str, str]]:
        graph = self._graph_repository.get_navigation_graph(self._graph_max_edges)
        results: list[dict[str, str]] = []

        for spec_path in self._spec_repository.list_specs(specs_dir):
            spec = self._spec_repository.load(spec_path)
            normalized_spec = normalize_spec(spec.raw_text)
            pages = rank_pages(graph, normalized_spec, self._relevant_pages_limit)
            page_scores = {page.page.url: page.score for page in pages}
            all_transitions_for_paths = rank_transitions(
                graph,
                normalized_spec,
                page_scores,
                max(len(graph.transitions), self._relevant_transitions_limit),
            )
            transitions = all_transitions_for_paths[: self._relevant_transitions_limit]
            paths = rank_candidate_paths(
                graph,
                self._base_url,
                pages,
                all_transitions_for_paths,
                self._max_path_depth,
                self._candidate_paths_limit,
            )
            coverage = analyze_spec_coverage(spec, pages, transitions, paths)
            context = RelevantGraphContext(pages=pages, transitions=transitions, paths=paths, coverage=coverage)
            prompt = build_structured_prompt(spec, self._base_url, context)

            generated_prompt = GeneratedPrompt(
                spec=spec,
                prompt=prompt,
                graph_pages=len(graph.pages),
                graph_transitions=len(graph.transitions),
                relevant_pages=len(pages),
                relevant_transitions=len(transitions),
                candidate_paths=len(paths),
                coverage_status=coverage.overall_status,
                coverage_score=coverage.coverage_score,
            )
            output_path = self._prompt_writer.write(output_dir, generated_prompt)
            results.append(
                {
                    "spec": str(spec_path),
                    "output": str(output_path),
                    "graph_pages": str(generated_prompt.graph_pages),
                    "graph_transitions": str(generated_prompt.graph_transitions),
                    "relevant_pages": str(generated_prompt.relevant_pages),
                    "relevant_transitions": str(generated_prompt.relevant_transitions),
                    "candidate_paths": str(generated_prompt.candidate_paths),
                    "coverage_status": generated_prompt.coverage_status,
                    "coverage_score": f"{generated_prompt.coverage_score:.3f}",
                }
            )

        self._prompt_writer.write_summary(output_dir, results)
        return results
