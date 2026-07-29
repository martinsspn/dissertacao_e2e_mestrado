import json
import tempfile
import unittest
from pathlib import Path

from avaliacao_prompts.infrastructure.playwright_results import read_playwright_json


class PlaywrightResultsTest(unittest.TestCase):
    def test_classifies_pass_skip_environment_and_selector_failures(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            payload = {
                "config": {"rootDir": str(root)},
                "suites": [
                    {
                        "specs": [
                            self._spec("passed.spec.ts", "passed", "passed", ""),
                            self._spec("skip.spec.ts", "skipped", "skipped", ""),
                            self._spec("env.spec.ts", "passed", "failed", "The environment variable DEMO_WEB_SHOP_EMAIL is required."),
                            self._spec("selector.spec.ts", "passed", "failed", "strict mode violation: resolved to 4 elements"),
                        ]
                    }
                ],
            }
            json_path = root / "results.json"
            json_path.write_text(json.dumps(payload), encoding="utf-8")

            results = read_playwright_json(json_path)

        self.assertEqual(results[(root / "passed.spec.ts").resolve()].status, "passed")
        self.assertEqual(results[(root / "skip.spec.ts").resolve()].status, "skipped")
        self.assertEqual(results[(root / "env.spec.ts").resolve()].status, "environment_error")
        self.assertEqual(results[(root / "selector.spec.ts").resolve()].error_type, "selector_ambiguity")

    def test_aggregates_all_tests_from_the_same_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            payload = {
                "config": {"rootDir": str(root)},
                "suites": [
                    {
                        "specs": [
                            self._spec("scenario.spec.ts", "passed", "passed", ""),
                            self._spec(
                                "scenario.spec.ts",
                                "passed",
                                "failed",
                                "strict mode violation: resolved to 2 elements",
                            ),
                        ]
                    }
                ],
            }
            json_path = root / "results.json"
            json_path.write_text(json.dumps(payload), encoding="utf-8")

            results = read_playwright_json(json_path)

        result = results[(root / "scenario.spec.ts").resolve()]
        self.assertEqual(result.status, "failed")
        self.assertEqual(result.error_type, "selector_ambiguity")
        self.assertEqual(result.duration_seconds, 2.5)

    @staticmethod
    def _spec(file: str, expected: str, status: str, message: str) -> dict:
        return {
            "file": file,
            "tests": [
                {
                    "expectedStatus": expected,
                    "results": [
                        {
                            "status": status,
                            "duration": 1250,
                            "errors": [{"message": message}] if message else [],
                        }
                    ],
                }
            ],
        }
