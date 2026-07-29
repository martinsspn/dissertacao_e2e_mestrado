from __future__ import annotations

import shutil
import subprocess
import sys

from web_app.config import WebAppConfig
from web_app.domain import Job
from web_app.services.job_manager import JobManager


class PipelineService:
    def __init__(self, config: WebAppConfig, jobs: JobManager) -> None:
        self._config = config
        self._jobs = jobs
        self._compose_cmd = _resolve_compose_command()

    def run_crawler(
        self,
        target_url: str,
        max_depth: int,
        max_states: int,
        max_runtime_minutes: int,
        wait_after_reload_ms: int,
        wait_after_event_ms: int,
        click_once: bool,
        random_order: bool,
    ) -> Job:
        return self._jobs.start(
            "crawl",
            self._compose_cmd + ["run", "--rm", "crawljax_java"],
            env={
                "TARGET_URL": target_url,
                "CRAWL_MAX_DEPTH": str(max_depth),
                "CRAWL_MAX_STATES": str(max_states),
                "CRAWL_MAX_RUNTIME_MINUTES": str(max_runtime_minutes),
                "CRAWL_WAIT_AFTER_RELOAD_MS": str(wait_after_reload_ms),
                "CRAWL_WAIT_AFTER_EVENT_MS": str(wait_after_event_ms),
                "CRAWL_CLICK_ONCE": str(click_once).lower(),
                "CRAWL_RANDOM_ORDER": str(random_order).lower(),
            },
        )

    def generate_prompts(self, target_url: str) -> Job:
        return self._jobs.start(
            "prompts",
            self._compose_cmd + ["run", "--rm", "prompt_e2e"],
            env={"TARGET_URL": target_url, "PROMPT_E2E_BASE_URL": target_url},
        )

    def evaluate_tests(self, approach: str, use_graph: bool, target_url: str) -> Job:
        tests_dir = self._config.generated_tests_dir / approach
        output_path = self._config.evaluation_reports_dir / f"{approach}.md"
        command = [
            sys.executable,
            "-m",
            "avaliacao_prompts",
            "--tests-dir",
            str(tests_dir),
            "--approach",
            approach,
            "--base-url",
            target_url,
            "--output",
            str(output_path),
            "--prompt-dir",
            str(self._config.prompts_dir),
            "--specs-dir",
            str(self._config.specs_dir),
        ]
        if use_graph:
            command.extend(
                [
                    "--neo4j-uri",
                    self._config.neo4j_uri,
                    "--neo4j-user",
                    self._config.neo4j_user,
                    "--neo4j-password",
                    self._config.neo4j_password,
                ]
            )
        else:
            command.append("--skip-graph")
        env = {
            "PYTHONPATH": str(self._config.evaluation_module_dir),
            "PROMPT_E2E_BASE_URL": target_url,
        }
        return self._jobs.start("evaluation", command, env=env)


def _resolve_compose_command() -> list[str]:
    if shutil.which("docker"):
        try:
            result = subprocess.run(
                ["docker", "compose", "version"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            )
            if result.returncode == 0:
                return ["docker", "compose"]
        except Exception:
            pass
    if shutil.which("docker-compose"):
        return ["docker-compose"]
    return ["docker", "compose"]
