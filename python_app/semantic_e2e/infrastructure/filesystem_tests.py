from __future__ import annotations

import json
from pathlib import Path

from semantic_e2e.domain.models import GeneratedTest


class FileSystemGeneratedTestWriter:
    def write(self, output_dir: Path, generated_test: GeneratedTest) -> Path:
        output_dir = output_dir.resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"{generated_test.spec.source_path.stem}.spec.ts"
        output_path.write_text(generated_test.code, encoding="utf-8")
        return output_path

    def write_summary(self, output_dir: Path, results: list[dict[str, str]]) -> Path:
        output_dir = output_dir.resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
        summary_path = output_dir / "generation_summary.json"
        summary_path.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
        return summary_path
