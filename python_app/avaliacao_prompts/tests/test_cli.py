import tempfile
import unittest
from pathlib import Path

from avaliacao_prompts.presentation.cli import _prompt_file_for, _spec_file_for


class PromptFileResolutionTest(unittest.TestCase):
    def test_matches_generated_test_names_to_suite_prompt_names(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            prompt_dir = Path(directory)
            expected = prompt_dir / "suite_adicionar_wishlist.structured_context.prompt.md"
            expected.touch()
            (prompt_dir / "suite_limpar_wishlist.structured_context.prompt.md").touch()

            result = _prompt_file_for(
                prompt_dir,
                Path("teste_wishlist_estruturado.spec.ts"),
                "structured_context",
            )

        self.assertEqual(result, expected.resolve())

    def test_matches_exact_spec_name_without_suite_prefix(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            specification = root / "fluxo_computadores_desktops.txt"
            specification.write_text("scenario", encoding="utf-8")

            result = _spec_file_for(
                root,
                Path("fluxo_computadores_desktops.spec.ts"),
            )

        self.assertEqual(result, specification.resolve())
