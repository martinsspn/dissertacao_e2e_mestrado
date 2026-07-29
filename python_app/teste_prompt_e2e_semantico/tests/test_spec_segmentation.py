import unittest

from teste_prompt_e2e_semantico.application.spec_segmentation import segment_specification


class SpecSegmentationTest(unittest.TestCase):
    def test_preserves_one_step_per_non_empty_line_and_ignores_title(self) -> None:
        steps = segment_specification(
            "Fluxo de contato:\n\n- Acessar a pagina.\n- Preencher nome e sobrenome.\n- Enviar o formulario."
        )

        self.assertEqual(
            [step.text for step in steps],
            ["Acessar a pagina.", "Preencher nome e sobrenome.", "Enviar o formulario."],
        )

    def test_splits_single_paragraph_only_at_sentence_boundaries(self) -> None:
        steps = segment_specification("Acessar a pagina. Preencher nome e sobrenome. Enviar o formulario.")

        self.assertEqual(len(steps), 3)
        self.assertEqual(steps[1].text, "Preencher nome e sobrenome.")

    def test_removes_inline_scenario_title_before_the_first_step(self) -> None:
        steps = segment_specification(
            "Searching and opening a product: The user searches for Blue Jeans. "
            "The user opens the product."
        )

        self.assertEqual(
            [step.text for step in steps],
            ["The user searches for Blue Jeans.", "The user opens the product."],
        )

    def test_removes_repeated_steps_without_changing_text(self) -> None:
        steps = segment_specification("Clicar em Register.\nClicar em Register.")

        self.assertEqual([(step.id, step.text) for step in steps], [("R1", "Clicar em Register.")])
