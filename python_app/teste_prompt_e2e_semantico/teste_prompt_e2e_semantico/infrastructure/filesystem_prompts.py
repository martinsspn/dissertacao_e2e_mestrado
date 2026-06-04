from __future__ import annotations

import json
from pathlib import Path

from teste_prompt_e2e_semantico.domain.models import GeneratedPrompt


class FileSystemPromptWriter:
    def write(self, output_dir: Path, generated_prompt: GeneratedPrompt) -> Path:
        output_dir = output_dir.resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"{generated_prompt.spec.source_path.stem}.prompt.md"
        output_path.write_text(generated_prompt.prompt, encoding="utf-8")
        return output_path

    def write_summary(self, output_dir: Path, results: list[dict[str, str]]) -> Path:
        output_dir = output_dir.resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
        summary_path = output_dir / "prompt_generation_summary.json"
        summary_path.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
        return summary_path
