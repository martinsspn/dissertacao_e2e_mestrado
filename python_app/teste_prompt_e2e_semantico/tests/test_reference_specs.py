from __future__ import annotations

import unittest
from pathlib import Path

from teste_prompt_e2e_semantico.application.spec_segmentation import segment_specification


class ReferenceSpecificationsTest(unittest.TestCase):
    def test_curated_suite_contains_independent_segmentable_scenarios(self) -> None:
        specs_dir = Path(__file__).resolve().parents[1] / "specs"
        spec_files = sorted(specs_dir.glob("suite_*.txt"))

        self.assertEqual(12, len(spec_files))

        for spec_file in spec_files:
            with self.subTest(specification=spec_file.name):
                raw_text = spec_file.read_text(encoding="utf-8")
                steps = segment_specification(raw_text)

                self.assertGreaterEqual(len(steps), 4)
                self.assertEqual("R1", steps[0].id)
                self.assertFalse(any(step.text.endswith(":") for step in steps))


if __name__ == "__main__":
    unittest.main()
