from __future__ import annotations

from pathlib import Path

from teste_prompt_e2e_semantico.domain.models import SpecPlan


class FileSystemSpecRepository:
    def list_specs(self, specs_dir: Path) -> list[Path]:
        return sorted(specs_dir.resolve().glob("*.txt"))

    def load(self, path: Path) -> SpecPlan:
        raw_text = path.read_text(encoding="utf-8")
        title = path.stem.replace("_", " ").strip().title()
        return SpecPlan(source_path=path, raw_text=raw_text, title=title)
