from __future__ import annotations

import re
from pathlib import Path

from web_app.config import WebAppConfig


_SAFE_ID = re.compile(r"[^a-zA-Z0-9_-]+")


class FileSystemService:
    def __init__(self, config: WebAppConfig) -> None:
        self._config = config
        self._config.specs_dir.mkdir(parents=True, exist_ok=True)
        self._config.prompts_dir.mkdir(parents=True, exist_ok=True)
        self._config.generated_tests_dir.mkdir(parents=True, exist_ok=True)
        self._config.evaluation_reports_dir.mkdir(parents=True, exist_ok=True)

    def list_specs(self) -> list[Path]:
        return sorted(self._config.specs_dir.glob("*.txt"))

    def read_spec(self, spec_id: str) -> str:
        return self._spec_path(spec_id).read_text(encoding="utf-8")

    def write_spec(self, spec_id: str, content: str) -> Path:
        path = self._spec_path(spec_id)
        path.write_text(content.strip() + "\n", encoding="utf-8")
        return path

    def write_uploaded_spec(self, filename: str, content: bytes) -> Path:
        spec_id = Path(filename).stem
        text = content.decode("utf-8", errors="replace")
        return self.write_spec(spec_id, text)

    def delete_specs(self, spec_ids: list[str]) -> int:
        deleted = 0
        for spec_id in spec_ids:
            path = self._spec_path(spec_id)
            if path.exists():
                path.unlink()
                deleted += 1
        return deleted

    def list_prompts(self) -> list[Path]:
        return sorted(self._config.prompts_dir.glob("*.prompt.md")) if self._config.prompts_dir.exists() else []

    def read_prompt(self, prompt_id: str) -> str:
        return self._prompt_path(prompt_id).read_text(encoding="utf-8")

    def prompt_paths(self, prompt_ids: list[str] | None = None) -> list[Path]:
        if prompt_ids is None:
            return self.list_prompts()
        paths: list[Path] = []
        for prompt_id in prompt_ids:
            path = self._prompt_path(prompt_id)
            if path.exists():
                paths.append(path)
        return sorted(paths)

    def delete_prompts(self, prompt_ids: list[str]) -> int:
        deleted = 0
        for path in self.prompt_paths(prompt_ids):
            path.unlink()
            deleted += 1
        return deleted

    def list_tests(self, approach: str) -> list[Path]:
        tests_dir = self._tests_dir(approach)
        return sorted(tests_dir.glob("*.spec.ts")) if tests_dir.exists() else []

    def read_test(self, approach: str, spec_id: str) -> str:
        return self._test_path(approach, spec_id).read_text(encoding="utf-8")

    def write_test(self, approach: str, spec_id: str, code: str) -> Path:
        path = self._test_path(approach, spec_id)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(code.rstrip() + "\n", encoding="utf-8")
        return path

    def list_reports(self) -> list[Path]:
        return sorted(self._config.evaluation_reports_dir.glob("*.json"))

    def read_report(self, report_id: str) -> str:
        return self._report_path(report_id).read_text(encoding="utf-8")

    def _spec_path(self, spec_id: str) -> Path:
        return self._config.specs_dir / f"{_safe_id(spec_id)}.txt"

    def _prompt_path(self, prompt_id: str) -> Path:
        return self._config.prompts_dir / f"{_safe_id(prompt_id)}.prompt.md"

    def _tests_dir(self, approach: str) -> Path:
        return self._config.generated_tests_dir / _safe_id(approach)

    def _test_path(self, approach: str, spec_id: str) -> Path:
        return self._tests_dir(approach) / f"{_safe_id(spec_id)}.spec.ts"

    def _report_path(self, report_id: str) -> Path:
        return self._config.evaluation_reports_dir / f"{_safe_id(report_id)}.json"


def _safe_id(value: str) -> str:
    normalized = _SAFE_ID.sub("_", value.strip()).strip("_")
    return normalized or "sem_titulo"
