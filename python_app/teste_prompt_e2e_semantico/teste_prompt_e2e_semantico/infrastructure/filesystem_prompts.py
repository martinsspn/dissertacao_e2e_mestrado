from __future__ import annotations

import json
from pathlib import Path

from teste_prompt_e2e_semantico.domain.models import GeneratedPrompt


class FileSystemPromptWriter:
    def prune_stale(self, output_dir: Path, active_spec_ids: set[str]) -> int:
        output_dir = output_dir.resolve()
        if not output_dir.exists():
            return 0
        removed = 0
        suffix = ".structured_context.prompt.md"
        for prompt_path in output_dir.glob(f"*{suffix}"):
            spec_id = prompt_path.name.removesuffix(suffix)
            if spec_id not in active_spec_ids:
                prompt_path.unlink()
                removed += 1
        return removed

    def write(self, output_dir: Path, generated_prompt: GeneratedPrompt) -> Path:
        output_dir = output_dir.resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / (
            f"{generated_prompt.spec.source_path.stem}.{generated_prompt.approach}.prompt.md"
        )
        output_path.write_text(generated_prompt.prompt, encoding="utf-8")
        return output_path

    def write_summary(self, output_dir: Path, results: list[dict[str, str]]) -> Path:
        output_dir = output_dir.resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
        summary_path = output_dir / "prompt_generation_summary.json"
        summary_path.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
        return summary_path
