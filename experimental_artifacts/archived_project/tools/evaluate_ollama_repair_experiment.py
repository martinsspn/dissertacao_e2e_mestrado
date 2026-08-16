#!/usr/bin/env python3
"""Coleta e, opcionalmente, executa individualmente os testes reparados."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "python_app" / "avaliacao_prompts" / "playwright.config.ts"


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repair-run", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--execute-live", action="store_true")
    parser.add_argument("--limit", type=int)
    return parser.parse_args()


def iter_specs(suites: list[dict[str, Any]]) -> Iterator[dict[str, Any]]:
    for suite in suites:
        yield from suite.get("specs", [])
        yield from iter_specs(suite.get("suites", []))


def result_from_json(path: Path) -> tuple[str, str, float]:
    if not path.is_file() or not path.read_text(encoding="utf-8").lstrip().startswith("{"):
        return "environment_error", "", 0.0
    payload = json.loads(path.read_text(encoding="utf-8"))
    statuses: list[str] = []
    messages: list[str] = []
    durations: list[float] = []
    for spec in iter_specs(payload.get("suites", [])):
        for test in spec.get("tests", []):
            results = test.get("results", [])
            if not results:
                continue
            result = results[-1]
            statuses.append(result.get("status", "unknown"))
            durations.append(float(result.get("duration", 0)))
            message = (result.get("error") or {}).get("message", "")
            if message:
                messages.append(message)
    if not statuses:
        errors = payload.get("errors", [])
        return "collection_error", "\n\n".join(error.get("message", "") for error in errors), 0.0
    status = "passed" if all(item == "passed" for item in statuses) else "failed"
    return status, "\n\n".join(dict.fromkeys(messages)), sum(durations)


def create_account() -> dict[str, str]:
    completed = subprocess.run(
        ["node", str(ROOT / "tools" / "create_demowebshop_repair_account.mjs")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        timeout=60,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError("Não foi possível criar a conta sintética: " + completed.stderr)
    return json.loads(completed.stdout)


def execution_environment(account: dict[str, str] | None) -> dict[str, str]:
    env = os.environ.copy()
    env.update(
        {
            "PROMPT_E2E_BASE_URL": "https://demowebshop.tricentis.com/",
            "BASE_URL": "https://demowebshop.tricentis.com",
            "BILLING_FIRST_NAME": "Repair",
            "BILLING_LAST_NAME": "Evaluation",
            "BILLING_EMAIL": "repair-address@example.com",
            "BILLING_CITY": "Natal",
            "BILLING_ADDRESS1": "Research Avenue 100",
            "BILLING_ZIP": "59000-000",
            "SHIPPING_FIRST_NAME": "Repair",
            "SHIPPING_LAST_NAME": "Evaluation",
            "SHIPPING_EMAIL": "repair-address@example.com",
            "SHIPPING_CITY": "Natal",
            "SHIPPING_ADDRESS1": "Research Avenue 100",
            "SHIPPING_ZIP": "59000-000",
            "CARDHOLDER_NAME": "Repair Evaluation",
            "CARD_NUMBER": "4111111111111111",
            "CARD_CODE": "123",
        }
    )
    if account:
        email = account["email"]
        password = account["password"]
        env.update(
            {
                "DEMO_WEB_SHOP_EMAIL": email,
                "DEMO_WEB_SHOP_USERNAME": email,
                "DEMO_WEB_SHOP_PASSWORD": password,
                "E2E_EMAIL": email,
                "E2E_PASSWORD": password,
                "TEST_EMAIL": email,
                "TEST_PASSWORD": password,
                "EMAIL": email,
                "PASSWORD": password,
                "INVALID_PASSWORD": password + "-invalid",
                "DEMO_WEB_SHOP_FIRST_NAME": account["firstName"],
                "DEMO_WEB_SHOP_LAST_NAME": account["lastName"],
                "DEMO_WEB_SHOP_COUNTRY": "United States",
                "DEMO_WEB_SHOP_STATE": "New York",
                "DEMO_WEB_SHOP_CITY": "New York",
                "DEMO_WEB_SHOP_ADDRESS": "Research Avenue 100",
                "DEMO_WEB_SHOP_ZIP_CODE": "10001",
                "DEMO_WEB_SHOP_PHONE": "2125550100",
            }
        )
    return env


def main() -> int:
    args = arguments()
    repair_run = args.repair_run.resolve()
    output = args.output_dir.resolve()
    if output.exists():
        print(f"Saída existente recusada: {output}", file=sys.stderr)
        return 2
    manifest = json.loads((repair_run / "manifest.json").read_text(encoding="utf-8"))
    records = manifest["records"]
    if args.limit is not None:
        records = records[: args.limit]
    output.mkdir(parents=True)
    account = create_account() if args.execute_live else None
    env = execution_environment(account)
    evaluated: list[dict[str, Any]] = []
    started_at = datetime.now(timezone.utc)

    for index, record in enumerate(records, start=1):
        repaired = Path(record["repaired_file"])
        case_id = "__".join(
            [
                record["model_origin"].replace(":", "-"),
                record["round"],
                record["condition"],
                record["scenario"],
            ]
        )
        case = output / case_id
        case.mkdir()
        case_env = dict(env)
        case_env["RESILIENCE_TEST_DIR"] = str(repaired.parent)
        collection_command = [
            "npx",
            "playwright",
            "test",
            repaired.name,
            f"--config={CONFIG}",
            "--list",
        ]
        print(f"[repair-eval] collect {index}/{len(records)} {case_id}", flush=True)
        collect_started = time.monotonic()
        collected = subprocess.run(
            collection_command,
            cwd=ROOT,
            env=case_env,
            text=True,
            capture_output=True,
            timeout=30,
            check=False,
        )
        collect_seconds = time.monotonic() - collect_started
        (case / "collection.stdout.txt").write_text(collected.stdout, encoding="utf-8")
        (case / "collection.stderr.txt").write_text(collected.stderr, encoding="utf-8")
        collection_status = "collected" if collected.returncode == 0 else "collection_error"
        execution_status = "not_executed"
        failure_message = ""
        duration_ms = 0.0
        execution_seconds = 0.0

        if args.execute_live and collection_status == "collected":
            print(f"[repair-eval] execute {index}/{len(records)} {case_id}", flush=True)
            json_path = case / "playwright.json"
            execution_command = [
                "npx",
                "playwright",
                "test",
                repaired.name,
                f"--config={CONFIG}",
                "--reporter=json",
            ]
            execution_started = time.monotonic()
            executed = subprocess.run(
                execution_command,
                cwd=ROOT,
                env=case_env,
                text=True,
                capture_output=True,
                timeout=90,
                check=False,
            )
            execution_seconds = time.monotonic() - execution_started
            json_path.write_text(executed.stdout, encoding="utf-8")
            (case / "playwright.stderr.txt").write_text(executed.stderr, encoding="utf-8")
            execution_status, failure_message, duration_ms = result_from_json(json_path)

        evaluated.append(
            record
            | {
                "collection_status": collection_status,
                "collection_returncode": collected.returncode,
                "collection_seconds": round(collect_seconds, 3),
                "execution_status_after_repair": execution_status,
                "execution_seconds_client": round(execution_seconds, 3),
                "playwright_duration_ms": round(duration_ms, 3),
                "failure_message_after_repair": failure_message,
            }
        )
        (case / "evaluation_record.json").write_text(
            json.dumps(evaluated[-1], ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    result = {
        "repair_run": str(repair_run),
        "started_at_utc": started_at.isoformat(),
        "finished_at_utc": datetime.now(timezone.utc).isoformat(),
        "execute_live": args.execute_live,
        "environment": {
            "base_url": "https://demowebshop.tricentis.com/",
            "credential_aliases_configured": bool(account),
            "credential_values_recorded": False,
            "workers": 1,
            "fresh_context_per_test": True,
        },
        "records": evaluated,
    }
    (output / "evaluation_manifest.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"[repair-eval] concluído: {output}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
