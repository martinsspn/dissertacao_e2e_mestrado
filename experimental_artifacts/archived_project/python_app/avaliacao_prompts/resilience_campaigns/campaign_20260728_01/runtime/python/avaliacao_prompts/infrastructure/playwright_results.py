from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Iterator

from avaliacao_prompts.domain.models import ExecutionResult


_ANSI_ESCAPE = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")


def read_playwright_json(path: Path) -> dict[Path, ExecutionResult]:
    """Converte o JSON técnico do Playwright em um resultado por arquivo de teste."""
    payload = json.loads(path.read_text(encoding="utf-8"))
    root_dir = Path(payload.get("config", {}).get("rootDir", ".")).resolve()
    collected: dict[Path, list[ExecutionResult]] = {}
    for spec in _iter_specs(payload.get("suites", [])):
        test_file = (root_dir / spec["file"]).resolve()
        for test in spec.get("tests", []):
            attempts = test.get("results", [])
            attempt = attempts[-1] if attempts else {}
            collected.setdefault(test_file, []).append(_execution_result(test, attempt))
    return {
        test_file: _aggregate_file_results(test_results)
        for test_file, test_results in collected.items()
    }


def _iter_specs(suites: list[dict[str, Any]]) -> Iterator[dict[str, Any]]:
    for suite in suites:
        yield from suite.get("specs", [])
        yield from _iter_specs(suite.get("suites", []))


def _execution_result(test: dict[str, Any], attempt: dict[str, Any]) -> ExecutionResult:
    raw_status = attempt.get("status", "")
    expected_status = test.get("expectedStatus", "")
    errors = attempt.get("errors", [])
    message = _error_message(errors)
    status = _status(raw_status, expected_status, message)
    return ExecutionResult(
        status=status,
        error_type=_error_type(message) if message else "",
        error_message_excerpt=_excerpt(message),
        duration_seconds=round(float(attempt.get("duration", 0)) / 1000, 3),
    )


def _aggregate_file_results(results: list[ExecutionResult]) -> ExecutionResult:
    """Aprova uma especificação somente quando nenhum test() do arquivo falha."""
    failures = [
        result for result in results if result.status not in {"passed", "skipped"}
    ]
    if failures:
        priority = {
            "environment_error": 0,
            "syntax_error": 1,
            "timed_out": 2,
            "runtime_error": 3,
            "failed": 4,
        }
        representative = min(
            failures,
            key=lambda result: priority.get(result.status, 99),
        )
        status = representative.status
        error_type = representative.error_type
        error_message_excerpt = representative.error_message_excerpt
    elif any(result.status == "passed" for result in results):
        status = "passed"
        error_type = ""
        error_message_excerpt = ""
    else:
        status = "skipped"
        error_type = ""
        error_message_excerpt = ""

    durations = [
        result.duration_seconds
        for result in results
        if result.duration_seconds is not None
    ]
    return ExecutionResult(
        status=status,
        error_type=error_type,
        error_message_excerpt=error_message_excerpt,
        duration_seconds=round(sum(durations), 3) if durations else None,
    )


def _status(raw_status: str, expected_status: str, message: str) -> str:
    if raw_status == "skipped" or expected_status == "skipped":
        return "skipped"
    if raw_status == "passed":
        return "passed"
    lowered = message.lower()
    if "syntaxerror" in lowered or "unexpected token" in lowered:
        return "syntax_error"
    if "environment variable" in lowered or "defina demo_web_shop" in lowered or "define demo_web_shop" in lowered:
        return "environment_error"
    if raw_status == "timedOut":
        return "timed_out"
    return "failed"


def _error_type(message: str) -> str:
    lowered = message.lower()
    if "strict mode violation" in lowered:
        return "selector_ambiguity"
    if "timeouterror" in lowered and ("waiting for" in lowered or "locator" in lowered):
        return "locator_timeout"
    if "environment variable" in lowered or "demo_web_shop" in lowered:
        return "missing_environment_variable"
    if "syntaxerror" in lowered or "unexpected token" in lowered:
        return "syntax_error"
    if "expect(" in lowered or "expect." in lowered:
        return "assertion_failure"
    return "runtime_failure"


def _error_message(errors: list[dict[str, Any]]) -> str:
    if not errors:
        return ""
    error = errors[0]
    return str(error.get("message") or error.get("stack") or "")


def _excerpt(message: str, limit: int = 500) -> str:
    normalized = re.sub(r"\s+", " ", _ANSI_ESCAPE.sub("", message)).strip()
    return normalized if len(normalized) <= limit else normalized[: limit - 1].rstrip() + "…"
