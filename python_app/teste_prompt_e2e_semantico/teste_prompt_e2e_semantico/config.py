from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _env_path(name: str, default: str) -> Path:
    return Path(os.getenv(name, default)).expanduser().resolve()


@dataclass(frozen=True)
class PromptGeneratorConfig:
    neo4j_uri: str = os.getenv("NEO4J_URI", "bolt://neo4j:7687")
    neo4j_user: str = os.getenv("NEO4J_USER", "neo4j")
    neo4j_password: str = os.getenv("NEO4J_PASSWORD", "neo4j_password")
    neo4j_ready_timeout_seconds: int = int(
        os.getenv("PROMPT_E2E_NEO4J_READY_TIMEOUT_SECONDS", os.getenv("NEO4J_READY_TIMEOUT_SECONDS", "60"))
    )
    base_url: str = os.getenv("PROMPT_E2E_BASE_URL", "https://demowebshop.tricentis.com/")
    specs_dir: Path = _env_path("PROMPT_E2E_SPECS_DIR", "specs")
    output_dir: Path = _env_path("PROMPT_E2E_OUTPUT_DIR", "generated_prompts")
