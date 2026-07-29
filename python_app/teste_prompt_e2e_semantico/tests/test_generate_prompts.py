import tempfile
import unittest
from pathlib import Path

from teste_prompt_e2e_semantico.application.generate_prompts import GeneratePromptsUseCase
from teste_prompt_e2e_semantico.domain.models import NavigationGraph, SpecPlan
from teste_prompt_e2e_semantico.infrastructure.filesystem_prompts import FileSystemPromptWriter


class _SpecRepository:
    def list_specs(self, specs_dir: Path) -> list[Path]:
        return [specs_dir / "contact.txt"]

    def load(self, path: Path) -> SpecPlan:
        return SpecPlan(path, "Acessar Contact Us.", "contact")


class _GraphRepository:
    def get_navigation_graph(self) -> NavigationGraph:
        return NavigationGraph([], [])

    def close(self) -> None:
        pass


class GeneratePromptsTest(unittest.TestCase):
    def test_generates_only_structured_context_prompt(self) -> None:
        use_case = GeneratePromptsUseCase(
            spec_repository=_SpecRepository(),
            graph_repository=_GraphRepository(),
            prompt_writer=FileSystemPromptWriter(),
            base_url="https://example.test/",
        )

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "output"
            output.mkdir()
            stale = output / "removed.structured_context.prompt.md"
            stale.write_text("old", encoding="utf-8")
            baseline = output / "removed.prompt.md"
            baseline.write_text("baseline", encoding="utf-8")
            results = use_case.execute(root, output)
            generated_files = sorted(output.glob("*.prompt.md"))

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["approach"], "structured_context")
        self.assertEqual(
            [path.name for path in generated_files],
            ["contact.structured_context.prompt.md", "removed.prompt.md"],
        )
