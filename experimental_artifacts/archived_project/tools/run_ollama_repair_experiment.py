#!/usr/bin/env python3
"""Executa uma tentativa isolada de reparo para cada teste Playwright reprovado."""

from __future__ import annotations

import argparse
import csv
import difflib
import hashlib
import json
import re
import sys
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from run_ollama_prompt_experiment import extract_typescript, post_json_windows


ROOT = Path(__file__).resolve().parents[1]
EVAL = ROOT / "python_app" / "avaliacao_prompts"
GENERATOR = ROOT / "python_app" / "teste_prompt_e2e_semantico"
NEW_INPUTS = Path("/home/martinsspn/openai_playwright_batch/inputs/demowebshop20-20260727-ready")
ANSI = re.compile(r"\x1b\[[0-9;]*m")

SYSTEM_PROMPT = """\
Você repara testes E2E Playwright em TypeScript. Produza uma única versão
completa do arquivo .spec.ts fornecido. Preserve a intenção e todas as
pré-condições e verificações da especificação. Corrija sintaxe, fluxo, locators,
esperas e asserções indicados pelas evidências. Use o Demo Web Shop em
https://demowebshop.tricentis.com e variáveis de ambiente quando a especificação
exigir credenciais. Não use DOM simulado, funções indefinidas, dados de outro
teste, waitForTimeout, XPath ou expectativas assíncronas sem await. Não remova
etapas apenas para fazer o teste passar. Responda somente com um bloco de código
typescript contendo o arquivo completo, sem explicações.
"""


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--review-csv", type=Path, default=EVAL / "resultados_adequacao_semantica_20260728" / "semantic_review.csv")
    parser.add_argument("--model", default="qwen2.5-coder:7b")
    parser.add_argument("--seed", type=int, default=20260728)
    parser.add_argument("--num-ctx", type=int, default=16384)
    parser.add_argument("--num-predict", type=int, default=4096)
    parser.add_argument("--timeout", type=int, default=1800)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--scenario", action="append", default=[])
    return parser.parse_args()


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def read_review(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        rows = [row for row in csv.DictReader(handle) if row["execution_status"] != "passed"]
    return sorted(rows, key=lambda row: (
        row["model"], row["round"], row["condition"], row["scenario"]
    ))


def playwright_failures(path: Path) -> dict[str, str]:
    if not path.is_file():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    messages: dict[str, list[str]] = defaultdict(list)

    def visit(suite: dict[str, Any]) -> None:
        scenario = Path(suite.get("file", "")).name.removesuffix(".spec.ts")
        for spec in suite.get("specs", []):
            for test in spec.get("tests", []):
                for result in test.get("results", []):
                    message = (result.get("error") or {}).get("message", "")
                    if scenario and message:
                        messages[scenario].append(ANSI.sub("", message).strip())
        for child in suite.get("suites", []):
            visit(child)

    for suite in payload.get("suites", []):
        visit(suite)
    for error in payload.get("errors", []):
        location = error.get("location") or {}
        scenario = Path(location.get("file", "")).name.removesuffix(".spec.ts")
        if scenario:
            messages[scenario].append(ANSI.sub("", error.get("message", "")).strip())
    return {
        scenario: "\n\n".join(dict.fromkeys(values))
        for scenario, values in messages.items()
    }


def failure_index() -> dict[tuple[str, str, str], str]:
    sources = {
        ("qwen_old_14", "baseline"): EVAL / "resultados_qwen_playwright_locators_20260724_02" / "baseline.playwright.json",
        ("qwen_old_14", "structured_context"): EVAL / "resultados_qwen_playwright_locators_20260724_02" / "structured_context.playwright.json",
        ("qwen_new_20", "baseline"): EVAL / "resultados_qwen25coder_demowebshop20_20260727_01" / "baseline.playwright.json",
        ("qwen_new_20", "structured_context"): EVAL / "resultados_qwen25coder_demowebshop20_20260727_01" / "structured_context.playwright.json",
        ("gemini_new_20", "baseline"): EVAL / "resultados_gemini36flash_demowebshop20_20260728_01" / "baseline.executable_subset.playwright.json",
        ("gemini_new_20", "structured_context"): EVAL / "resultados_gemini36flash_demowebshop20_20260728_01" / "structured_context.playwright.json",
    }
    index: dict[tuple[str, str, str], str] = {}
    for (round_id, condition), path in sources.items():
        for scenario, message in playwright_failures(path).items():
            index[(round_id, condition, scenario)] = message
    syntax = playwright_failures(
        EVAL / "resultados_gemini36flash_demowebshop20_20260728_01" / "baseline.playwright.json"
    )
    for scenario, message in syntax.items():
        index[("gemini_new_20", "baseline", scenario)] = message
    return index


def spec_path(round_id: str, scenario: str) -> Path:
    if round_id in {"qwen_new_20", "gemini_new_20"}:
        return NEW_INPUTS / "baseline" / f"{scenario}.txt"
    return GENERATOR / "specs" / f"{scenario}.txt"


def structured_prompt_path(round_id: str, scenario: str) -> Path:
    if round_id == "qwen_old_14":
        return GENERATOR / "generated_prompts_playwright_locators_20260724_02" / f"{scenario}.structured_context.prompt.md"
    if round_id == "gpt_original_12":
        return GENERATOR / "generated_prompts" / f"{scenario}.structured_context.prompt.md"
    return NEW_INPUTS / "structured_context" / f"{scenario}.prompt.md"


def changed_lines(before: str, after: str) -> tuple[int, int]:
    matcher = difflib.SequenceMatcher(a=before.splitlines(), b=after.splitlines())
    additions = deletions = 0
    for operation, i1, i2, j1, j2 in matcher.get_opcodes():
        if operation in {"replace", "delete"}:
            deletions += i2 - i1
        if operation in {"replace", "insert"}:
            additions += j2 - j1
    return additions, deletions


def make_prompt(
    row: dict[str, str],
    original: str,
    specification: str,
    execution_error: str,
    structured: str | None,
) -> str:
    parts = [
        "Condição experimental: " + row["condition"],
        "\nESPECIFICAÇÃO ORIGINAL:\n" + specification,
        "\nARQUIVO GERADO QUE DEVE SER REPARADO:\n```typescript\n" + original + "\n```",
        "\nEVIDÊNCIA DA FALHA DE EXECUÇÃO:\n" + (execution_error or "Falha registrada sem mensagem detalhada."),
        "\nDIAGNÓSTICO DA REVISÃO:\n" + row["review_note"],
    ]
    if structured is not None:
        parts.append("\nPROMPT ESTRUTURADO ORIGINAL DESTA CONDIÇÃO:\n" + structured)
    parts.append(
        "\nFaça uma única tentativa de reparo. Mantenha todas as verificações exigidas "
        "e devolva o arquivo TypeScript completo."
    )
    return "\n".join(parts)


def main() -> int:
    args = arguments()
    output = args.output_root.resolve()
    if output.exists():
        print(f"Saída existente recusada: {output}", file=sys.stderr)
        return 2
    rows = read_review(args.review_csv.resolve())
    if args.scenario:
        allowed = set(args.scenario)
        rows = [row for row in rows if row["scenario"] in allowed]
    if args.limit is not None:
        rows = rows[: args.limit]
    if not rows:
        raise ValueError("Nenhum arquivo reprovado selecionado.")

    errors = failure_index()
    output.mkdir(parents=True)
    started_at = datetime.now(timezone.utc)
    records: list[dict[str, Any]] = []
    for index, row in enumerate(rows, start=1):
        original_path = ROOT / row["source_file"]
        spec = spec_path(row["round"], row["scenario"])
        if not original_path.is_file() or not spec.is_file():
            raise FileNotFoundError(original_path if not original_path.is_file() else spec)
        original = original_path.read_text(encoding="utf-8")
        specification = spec.read_text(encoding="utf-8")
        structured_path = None
        structured = None
        if row["condition"] == "structured_context":
            structured_path = structured_prompt_path(row["round"], row["scenario"])
            if not structured_path.is_file():
                raise FileNotFoundError(structured_path)
            structured = structured_path.read_text(encoding="utf-8")
        error = errors.get((row["round"], row["condition"], row["scenario"]), "")
        prompt = make_prompt(row, original, specification, error, structured)
        case = (
            output
            / slug(row["model"])
            / row["round"]
            / row["condition"]
            / row["scenario"]
        )
        case.mkdir(parents=True)
        (case / "repair_input.md").write_text(prompt, encoding="utf-8")
        print(
            f"[repair] {index}/{len(rows)} {row['model']} {row['round']} "
            f"{row['condition']} {row['scenario']}",
            flush=True,
        )
        started = time.monotonic()
        payload = {
            "model": args.model,
            "system": SYSTEM_PROMPT,
            "prompt": prompt,
            "stream": False,
            "keep_alive": "30m",
            "options": {
                "temperature": 0,
                "seed": args.seed,
                "num_ctx": args.num_ctx,
                "num_predict": args.num_predict,
            },
        }
        response = post_json_windows(payload, args.timeout)
        elapsed = time.monotonic() - started
        raw = str(response.get("response", ""))
        repaired = extract_typescript(raw)
        (case / "response.raw.md").write_text(raw, encoding="utf-8")
        (case / f"{row['scenario']}.spec.ts").write_text(repaired, encoding="utf-8")
        additions, deletions = changed_lines(original, repaired)
        record = {
            "model_origin": row["model"],
            "round": row["round"],
            "condition": row["condition"],
            "scenario": row["scenario"],
            "original_execution_status": row["execution_status"],
            "original_semantic_score_6": int(row["semantic_total_6"]),
            "original_file": str(original_path),
            "specification_file": str(spec),
            "structured_prompt_file": str(structured_path) if structured_path else None,
            "repaired_file": str(case / f"{row['scenario']}.spec.ts"),
            "repair_model": args.model,
            "repair_attempt": 1,
            "stateless": True,
            "temperature": 0,
            "seed": args.seed,
            "num_ctx": args.num_ctx,
            "num_predict": args.num_predict,
            "elapsed_seconds_client": round(elapsed, 3),
            "prompt_eval_count": response.get("prompt_eval_count"),
            "eval_count": response.get("eval_count"),
            "total_duration_ns": response.get("total_duration"),
            "prompt_eval_duration_ns": response.get("prompt_eval_duration"),
            "eval_duration_ns": response.get("eval_duration"),
            "done_reason": response.get("done_reason"),
            "original_sha256": digest(original),
            "repair_prompt_sha256": digest(prompt),
            "raw_response_sha256": digest(raw),
            "repaired_sha256": digest(repaired),
            "original_lines": len(original.splitlines()),
            "repaired_lines": len(repaired.splitlines()),
            "lines_added": additions,
            "lines_deleted": deletions,
            "line_similarity_ratio": round(
                difflib.SequenceMatcher(
                    a=original.splitlines(), b=repaired.splitlines()
                ).ratio(),
                4,
            ),
        }
        (case / "repair_metadata.json").write_text(
            json.dumps(record, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        records.append(record)

    manifest = {
        "run_id": output.name,
        "started_at_utc": started_at.isoformat(),
        "finished_at_utc": datetime.now(timezone.utc).isoformat(),
        "repair_model": args.model,
        "system_prompt": SYSTEM_PROMPT,
        "settings": {
            "temperature": 0,
            "seed": args.seed,
            "num_ctx": args.num_ctx,
            "num_predict": args.num_predict,
            "attempts_per_file": 1,
        },
        "isolation": {
            "transport": "windows-powershell",
            "api": "/api/generate",
            "context_reused": False,
            "other_generated_tests_read": False,
            "existing_output_reuse_allowed": False,
        },
        "selected_files": len(records),
        "records": records,
    }
    (output / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"[repair] concluído: {output}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
