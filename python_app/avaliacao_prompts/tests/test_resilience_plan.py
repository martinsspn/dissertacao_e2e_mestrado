import json
import tempfile
import unittest
from pathlib import Path

from avaliacao_prompts.resilience.catalog import build_catalog
from avaliacao_prompts.resilience.plan import build_plan, verify_plan


class ResiliencePlanTest(unittest.TestCase):
    def test_builds_exhaustive_plan_without_test_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            specs = root / "specs"
            prompts = root / "prompts"
            specs.mkdir()
            prompts.mkdir()
            (specs / "suite_search.txt").write_text("The user searches.\n", encoding="utf-8")
            (prompts / "suite_search.structured_context.prompt.md").write_text(
                "\n".join(
                    [
                        "Contexto estruturado por etapa:",
                        "Etapa 1 (R1):",
                        "- pagina=https://example.test/",
                        "- controle_1=tag=input, label=Search:, id=search, name=q, input_type=text",
                        "- operacao_1=fill",
                        "- seletor_1=id:search",
                        "- controle_2=tag=input, input_type=submit, value=Search",
                        "- operacao_2=click",
                        "- seletor_2=role_name:Search",
                    ]
                ),
                encoding="utf-8",
            )
            # Um teste deliberadamente enviesado não pode afetar o plano, pois a
            # API não recebe nem percorre um diretório de .spec.ts.
            (root / "resultado.spec.ts").write_text("page.locator('#search')", encoding="utf-8")

            catalog = build_catalog(prompts)
            payload = build_plan(specs, prompts)
            repeated_payload = build_plan(specs, prompts)

        self.assertEqual(len(catalog), 2)
        self.assertEqual({target.page_url for target in catalog}, {"https://example.test/"})
        self.assertEqual(payload["catalog_size"], 2)
        self.assertEqual(payload["selection_method"], "exhaustive_all_applicable_operators_without_reading_generated_tests")
        self.assertEqual({item["stratum"] for item in payload["mutations"]}, {"E1", "E2", "E3"})
        self.assertTrue(verify_plan(payload))
        self.assertEqual(payload, repeated_payload)

    def test_detects_plan_tampering(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            specs = root / "specs"
            prompts = root / "prompts"
            specs.mkdir()
            prompts.mkdir()
            (specs / "a.txt").write_text("step", encoding="utf-8")
            (prompts / "a.structured_context.prompt.md").write_text(
                "Contexto estruturado por etapa:\nEtapa 1 (R1):\n"
                "- pagina=https://example.test/\n"
                "- controle=tag=a, text=Open, href=/open\n"
                "- operacao=click\n",
                encoding="utf-8",
            )
            payload = build_plan(specs, prompts)
            payload = json.loads(json.dumps(payload))
            payload["mutations"][0]["operator"] = "changed_after_results"

        self.assertFalse(verify_plan(payload))


if __name__ == "__main__":
    unittest.main()
