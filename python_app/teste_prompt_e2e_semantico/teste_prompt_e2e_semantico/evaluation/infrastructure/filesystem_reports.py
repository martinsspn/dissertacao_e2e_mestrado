from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any

from teste_prompt_e2e_semantico.evaluation.domain.models import EvaluationReport


class FileSystemEvaluationReportWriter:
    def write_json(self, output_path: Path, reports: list[EvaluationReport]) -> Path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps([_to_jsonable(report) for report in reports], indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        return output_path


def _to_jsonable(value: Any) -> Any:
    if isinstance(value, Path):
        return str(value)
    if is_dataclass(value):
        return _to_jsonable(asdict(value))
    if isinstance(value, dict):
        return {key: _to_jsonable(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_to_jsonable(item) for item in value]
    return value
