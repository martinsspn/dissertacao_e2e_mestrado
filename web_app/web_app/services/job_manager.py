from __future__ import annotations

import json
import os
import subprocess
import threading
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from web_app.config import WebAppConfig
from web_app.domain import Job, timestamp


class JobManager:
    def __init__(self, config: WebAppConfig) -> None:
        self._config = config
        self._jobs_dir = config.data_dir / "jobs"
        self._index_path = self._jobs_dir / "jobs.json"
        self._lock = threading.Lock()
        self._jobs_dir.mkdir(parents=True, exist_ok=True)

    def start(self, job_type: str, command: list[str], env: dict[str, str] | None = None) -> Job:
        job_id = self._new_job_id(job_type)
        log_path = self._jobs_dir / f"{job_id}.log"
        job = Job(
            id=job_id,
            type=job_type,
            status="queued",
            command=command,
            started_at=None,
            finished_at=None,
            exit_code=None,
            log_path=log_path,
        )
        self._save(job)
        thread = threading.Thread(target=self._run, args=(job, env or {}), daemon=True)
        thread.start()
        return job

    def list(self) -> list[Job]:
        data = self._read_index()
        return [self._from_dict(item) for item in data]

    def latest(self, job_type: str | None = None) -> Job | None:
        jobs = self.list()
        if job_type is not None:
            jobs = [job for job in jobs if job.type == job_type]
        return jobs[-1] if jobs else None

    def get(self, job_id: str) -> Job | None:
        for job in self.list():
            if job.id == job_id:
                return job
        return None

    def read_log(self, job_id: str) -> str:
        job = self.get(job_id)
        if job is None or not job.log_path.exists():
            return ""
        return job.log_path.read_text(encoding="utf-8", errors="replace")

    def _run(self, job: Job, env: dict[str, str]) -> None:
        running = self._replace(job, status="running", started_at=timestamp())
        self._save(running)
        with running.log_path.open("w", encoding="utf-8") as log_file:
            log_file.write("$ " + " ".join(running.command) + "\n\n")
            log_file.flush()
            process = subprocess.Popen(
                running.command,
                cwd=self._config.repo_root,
                env={**os.environ, **env},
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
            )
            assert process.stdout is not None
            for line in process.stdout:
                log_file.write(line)
                log_file.flush()
            exit_code = process.wait()
        finished = self._replace(
            running,
            status="succeeded" if exit_code == 0 else "failed",
            finished_at=timestamp(),
            exit_code=exit_code,
        )
        self._save(finished)

    def _save(self, job: Job) -> None:
        with self._lock:
            jobs = [item for item in self._read_index() if item.get("id") != job.id]
            jobs.append(_job_to_dict(job))
            self._index_path.write_text(json.dumps(jobs, indent=2), encoding="utf-8")

    def _read_index(self) -> list[dict[str, object]]:
        if not self._index_path.exists():
            return []
        try:
            data = json.loads(self._index_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return []
        return data if isinstance(data, list) else []

    def _new_job_id(self, job_type: str) -> str:
        value = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        return f"{job_type}_{value}"

    def _replace(self, job: Job, **changes: object) -> Job:
        data = _job_to_dict(job)
        data.update(changes)
        return self._from_dict(data)

    def _from_dict(self, data: dict[str, object]) -> Job:
        return Job(
            id=str(data["id"]),
            type=str(data["type"]),
            status=str(data["status"]),  # type: ignore[arg-type]
            command=[str(item) for item in data["command"]],
            started_at=data.get("started_at") if isinstance(data.get("started_at"), str) else None,
            finished_at=data.get("finished_at") if isinstance(data.get("finished_at"), str) else None,
            exit_code=data.get("exit_code") if isinstance(data.get("exit_code"), int) else None,
            log_path=Path(str(data["log_path"])),
        )


def _job_to_dict(job: Job) -> dict[str, object]:
    data = asdict(job)
    data["log_path"] = str(job.log_path)
    return data
