from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _int_env(name: str, fallback: int) -> int:
    try:
        return int(os.getenv(name, str(fallback)))
    except ValueError:
        return fallback


def _bool_env(name: str, fallback: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return fallback
    return value.lower() == "true"


@dataclass(frozen=True)
class WebAppConfig:
    repo_root: Path = Path(os.getenv("SEMANTIC_E2E_REPO_ROOT", _repo_root())).resolve()
    data_dir: Path = Path(os.getenv("SEMANTIC_E2E_WEB_DATA_DIR", _repo_root() / "web_app_data")).resolve()
    target_url: str = os.getenv("TARGET_URL", "https://demowebshop.tricentis.com/")
    neo4j_uri: str = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    neo4j_user: str = os.getenv("NEO4J_USER", "neo4j")
    neo4j_password: str = os.getenv("NEO4J_PASSWORD", "neo4j_password")
    crawl_max_depth: int = _int_env("CRAWL_MAX_DEPTH", 8)
    crawl_max_states: int = _int_env("CRAWL_MAX_STATES", 400)
    crawl_max_runtime_minutes: int = _int_env("CRAWL_MAX_RUNTIME_MINUTES", 45)
    crawl_wait_after_reload_ms: int = _int_env("CRAWL_WAIT_AFTER_RELOAD_MS", 3000)
    crawl_wait_after_event_ms: int = _int_env("CRAWL_WAIT_AFTER_EVENT_MS", 2200)
    crawl_click_once: bool = _bool_env("CRAWL_CLICK_ONCE", False)
    crawl_random_order: bool = _bool_env("CRAWL_RANDOM_ORDER", True)

    @property
    def prompt_module_dir(self) -> Path:
        return self.repo_root / "python_app" / "teste_prompt_e2e_semantico"

    @property
    def specs_dir(self) -> Path:
        return self.prompt_module_dir / "specs"

    @property
    def prompts_dir(self) -> Path:
        return self.prompt_module_dir / "generated_prompts"

    @property
    def generated_tests_dir(self) -> Path:
        return self.prompt_module_dir / "generated_tests"

    @property
    def evaluation_reports_dir(self) -> Path:
        return self.prompt_module_dir / "evaluation_reports"
