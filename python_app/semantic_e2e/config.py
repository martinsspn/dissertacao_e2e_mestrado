from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _env_path(name: str, default: str) -> Path:
    return Path(os.getenv(name, default)).expanduser().resolve()


@dataclass(frozen=True)
class GeneratorConfig:
    neo4j_uri: str = os.getenv("NEO4J_URI", "bolt://neo4j:7687")
    neo4j_user: str = os.getenv("NEO4J_USER", "neo4j")
    neo4j_password: str = os.getenv("NEO4J_PASSWORD", "neo4j_password")
    base_url: str = os.getenv("SEMANTIC_E2E_BASE_URL", "https://demowebshop.tricentis.com/")
    specs_dir: Path = _env_path("SEMANTIC_E2E_SPECS_DIR", "specs")
    output_dir: Path = _env_path("SEMANTIC_E2E_OUTPUT_DIR", "generated_tests")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_base_url: str = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    llm_model: str = os.getenv("LLM_MODEL", "gpt-4.1-mini")
    llm_timeout_seconds: int = int(os.getenv("LLM_TIMEOUT_SECONDS", "120"))
    graph_max_edges: int = int(os.getenv("SEMANTIC_E2E_GRAPH_MAX_EDGES", "500"))
