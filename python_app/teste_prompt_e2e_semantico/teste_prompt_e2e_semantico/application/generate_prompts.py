from __future__ import annotations

from pathlib import Path

from teste_prompt_e2e_semantico.application.context_selection import select_structured_context
from teste_prompt_e2e_semantico.application.ports import NavigationGraphRepository, PromptWriter, SpecRepository
from teste_prompt_e2e_semantico.application.prompt_builder import build_structured_prompt
from teste_prompt_e2e_semantico.application.spec_segmentation import segment_specification
from teste_prompt_e2e_semantico.domain.models import GeneratedPrompt


class GeneratePromptsUseCase:
    def __init__(
        self,
        spec_repository: SpecRepository,
        graph_repository: NavigationGraphRepository,
        prompt_writer: PromptWriter,
        base_url: str,
    ) -> None:
        self._spec_repository = spec_repository
        self._graph_repository = graph_repository
        self._prompt_writer = prompt_writer
        self._base_url = base_url

    def execute(self, specs_dir: Path, output_dir: Path) -> list[dict[str, str]]:
        graph = self._graph_repository.get_navigation_graph()
        results: list[dict[str, str]] = []
        spec_paths = self._spec_repository.list_specs(specs_dir)
        self._prompt_writer.prune_stale(output_dir, {path.stem for path in spec_paths})

        for spec_path in spec_paths:
            spec = self._spec_repository.load(spec_path)
            requirements = segment_specification(spec.raw_text)
            context = select_structured_context(graph, self._base_url, requirements)
            prompt = build_structured_prompt(spec, self._base_url, requirements, context)
            generated = GeneratedPrompt(
                spec=spec,
                approach="structured_context",
                prompt=prompt,
                requirement_count=len(requirements),
                context_item_count=context.item_count,
                character_count=len(prompt),
            )
            output_path = self._prompt_writer.write(output_dir, generated)
            results.append(
                {
                    "spec": str(spec_path),
                    "approach": generated.approach,
                    "output": str(output_path),
                    "requirements": str(generated.requirement_count),
                    "context_items": str(generated.context_item_count),
                    "characters": str(generated.character_count),
                }
            )

        self._prompt_writer.write_summary(output_dir, results)
        return results
