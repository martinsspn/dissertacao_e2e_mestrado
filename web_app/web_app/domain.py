from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Literal


JobStatus = Literal["queued", "running", "succeeded", "failed"]


@dataclass(frozen=True)
class Job:
    id: str
    type: str
    status: JobStatus
    command: list[str]
    started_at: str | None
    finished_at: str | None
    exit_code: int | None
    log_path: Path


def timestamp() -> str:
    return datetime.now().isoformat(timespec="seconds")
