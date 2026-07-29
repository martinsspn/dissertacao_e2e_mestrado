import json
import tempfile
import unittest
from pathlib import Path

from avaliacao_prompts.resilience.execution import prepare_execution, scenario_id_for_test
from avaliacao_prompts.resilience.plan import build_plan, write_plan
from avaliacao_prompts.resilience.run import (
    RunOutcome,
    _classify_mutated_outcome,
    _condition_order,
    _control_invalid_reasons,
    _mcnemar_exact,
    _select_mutations,
    _signed_payload_hash,
    _verify_signed_payload,
    execute_experiment,
)


class ResilienceExecutionTest(unittest.TestCase):
    def test_pairs_conditions_and_only_replaces_import(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            baseline = root / "baseline"
            structured = root / "structured"
            specs = root / "specs"
            prompts = root / "prompts"
            for path in (baseline, structured, specs, prompts):
                path.mkdir()
            source = "import { test, expect } from '@playwright/test';\ntest('x', async () => {});\n"
            (baseline / "teste_login_valido_baseline.spec.ts").write_text(source, encoding="utf-8")
            (structured / "teste_login_valido_estruturado.spec.ts").write_text(source, encoding="utf-8")
            (specs / "suite_login_valido.txt").write_text("login", encoding="utf-8")
            (prompts / "suite_login_valido.structured_context.prompt.md").write_text(
                "Contexto estruturado por etapa:\nEtapa 1 (R1):\n"
                "- pagina=https://example.test/login\n"
                "- controle=tag=input, id=Email, label=Email:\n"
                "- operacao=fill\n",
                encoding="utf-8",
            )
            plan_path = write_plan(root / "plan.json", build_plan(specs, prompts))
            fixture = root / "fixture.ts"
            fixture.write_text("export {};", encoding="utf-8")
            allowlist = root / "allowlist.json"
            allowlist.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "track_id": "P",
                        "model_id": "model",
                        "scenario_ids": ["suite_login_valido"],
                    }
                ),
                encoding="utf-8",
            )
            semantic_review = root / "semantic_review.csv"
            semantic_review.write_text("scenario,score\nsuite_login_valido,6\n", encoding="utf-8")

            manifest_path = prepare_execution(
                baseline,
                structured,
                fixture,
                plan_path,
                root / "run",
                allowlist,
                semantic_review,
                "P",
                "model",
            )
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            derived = (root / "run" / "A" / "suite_login_valido.spec.ts").read_text(encoding="utf-8")

        self.assertEqual(len(manifest["pairs"]), 1)
        self.assertEqual(manifest["condition_key"], {"A": "baseline", "B": "structured_context"})
        self.assertEqual(manifest["track_id"], "P")
        self.assertTrue(manifest["allowlist_sha256"])
        self.assertTrue(manifest["semantic_review_sha256"])
        self.assertNotIn("@playwright/test", derived)
        self.assertIn("fixture", derived)
        self.assertIn("test('x'", derived)

    def test_known_aliases_are_stable(self) -> None:
        self.assertEqual(
            scenario_id_for_test(Path("teste_buscar_blue_jeans_baseline.spec.ts"), "baseline"),
            "suite_busca_blue_jeans",
        )
        self.assertEqual(
            scenario_id_for_test(Path("teste_wishlist_estruturado.spec.ts"), "structured_context"),
            "suite_adicionar_wishlist",
        )
        self.assertEqual(
            scenario_id_for_test(Path("suite_navegar_sobre_nos.spec.ts"), "baseline"),
            "suite_navegar_sobre_nos",
        )

    def test_control_validity_does_not_depend_on_condition_results(self) -> None:
        original = RunOutcome(
            "passed",
            ({"status": "marked"}, {"status": "interacted"}),
            {"pathname": "/search", "supported": True},
        )
        mutated = RunOutcome(
            "passed",
            ({"status": "applied"}, {"status": "interacted"}),
            {"pathname": "/search", "supported": True},
        )
        self.assertEqual(_control_invalid_reasons(original, mutated), set())
        self.assertIn(
            "functional_observation_changed",
            _control_invalid_reasons(
                original,
                RunOutcome(
                    "passed",
                    ({"status": "applied"}, {"status": "interacted"}),
                    {"pathname": "/error"},
                ),
            ),
        )

    def test_mutated_pass_requires_interaction_with_expected_target(self) -> None:
        applied_only = RunOutcome(
            "passed",
            ({"status": "applied", "targetId": "target"},),
        )
        interacted = RunOutcome(
            "passed",
            (
                {"status": "applied", "targetId": "target"},
                {"status": "interacted", "targetId": "target"},
            ),
        )
        wrong = RunOutcome(
            "passed",
            (
                {"status": "applied", "targetId": "target"},
                {"status": "interacted", "targetId": "other"},
            ),
        )

        self.assertEqual(
            _classify_mutated_outcome(applied_only, expected_target_id="target"),
            "false_positive_no_interaction",
        )
        self.assertEqual(
            _classify_mutated_outcome(interacted, expected_target_id="target"),
            "passed_interacted",
        )
        self.assertEqual(
            _classify_mutated_outcome(wrong, expected_target_id="target"),
            "wrong_target",
        )

    def test_prepare_refuses_to_overwrite_existing_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "existing"
            output.mkdir()
            with self.assertRaises(FileExistsError):
                prepare_execution(
                    root,
                    root,
                    root / "fixture.ts",
                    root / "plan.json",
                    output,
                    root / "allowlist.json",
                    root / "review.csv",
                    "P",
                    "model",
                )

    def test_run_refuses_to_overwrite_existing_results(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "existing-results"
            output.mkdir()
            with self.assertRaises(FileExistsError):
                execute_experiment(
                    execution_manifest_path=root / "manifest.json",
                    eligibility_results_path=root / "eligibility.json",
                    playwright_config=root / "playwright.config.ts",
                    node_project_dir=root,
                    control_test=root / "control.spec.ts",
                    output_dir=output,
                    repetitions=3,
                )

    def test_eligibility_payload_signature_detects_tampering(self) -> None:
        payload = {
            "schema_version": 1,
            "eligible_scenarios": ["scenario"],
        }
        payload["eligibility_results_sha256"] = _signed_payload_hash(
            payload,
            "eligibility_results_sha256",
        )
        self.assertTrue(
            _verify_signed_payload(payload, "eligibility_results_sha256")
        )
        payload["eligible_scenarios"].append("changed")
        self.assertFalse(
            _verify_signed_payload(payload, "eligibility_results_sha256")
        )

    def test_failure_classes_are_specific(self) -> None:
        applied = ({"status": "applied", "targetId": "target"},)
        self.assertEqual(
            _classify_mutated_outcome(
                RunOutcome("timed_out", applied, error_type="locator_timeout"),
                expected_target_id="target",
            ),
            "locator_not_found",
        )
        self.assertEqual(
            _classify_mutated_outcome(
                RunOutcome("failed", applied, error_type="selector_ambiguity"),
                expected_target_id="target",
            ),
            "strict_mode_ambiguity",
        )
        self.assertEqual(
            _classify_mutated_outcome(
                RunOutcome("failed", applied, error_type="assertion_failure"),
                expected_target_id="target",
            ),
            "assertion_failure",
        )

    def test_randomized_order_and_exact_test_are_reproducible(self) -> None:
        self.assertEqual(_condition_order("hash", "unit"), _condition_order("hash", "unit"))
        self.assertEqual(_mcnemar_exact(0, 0), 1.0)
        self.assertAlmostEqual(_mcnemar_exact(0, 5), 0.0625)

    def test_reduced_selection_is_neutral_deterministic_and_stratified(self) -> None:
        mutations = [
            {"mutation_id": "e1-a", "stratum": "E1", "target": {"scenario_id": "s"}},
            {"mutation_id": "e1-b", "stratum": "E1", "target": {"scenario_id": "s"}},
            {"mutation_id": "e2-a", "stratum": "E2", "target": {"scenario_id": "s"}},
            {"mutation_id": "e3-a", "stratum": "E3", "target": {"scenario_id": "s"}},
        ]
        selected = _select_mutations(mutations, "frozen-hash", 2)
        repeated = _select_mutations(mutations, "frozen-hash", 2)

        self.assertEqual(selected, repeated)
        self.assertEqual({item["stratum"] for item in selected}, {"E1", "E2"})
        self.assertEqual(len(selected), 2)


if __name__ == "__main__":
    unittest.main()
