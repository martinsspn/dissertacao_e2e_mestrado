#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Executa as quatro coortes de elegibilidade sem revelar credenciais."
    )
    parser.add_argument("--campaign-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--credential-file", type=Path, required=True)
    parser.add_argument("--repetitions", type=int, default=3)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    campaign = args.campaign_dir.resolve()
    output = args.output_dir.resolve()
    credential_file = args.credential_file.expanduser().resolve()
    if output.exists():
        raise FileExistsError(f"Resultados já existem: {output}")
    if args.repetitions != 3:
        raise ValueError("A campanha congelada exige exatamente três repetições.")

    campaign_manifest = load_json(campaign / "campaign_manifest.json")
    if campaign_manifest.get("status") != "prepared_not_executed":
        raise ValueError("Campanha não está no estado preparado.")
    runtime_python = campaign / "runtime" / "python"
    runtime_config = campaign / "runtime" / "playwright" / "playwright.config.ts"
    credentials, account_created = load_or_create_credentials(credential_file)
    environment = normalized_environment(credentials, runtime_python)
    output.mkdir(parents=True)
    records: list[dict[str, Any]] = []
    for cohort in campaign_manifest["cohorts"]:
        track = cohort["track_id"]
        model = cohort["model_id"]
        execution_manifest = campaign / cohort["execution_manifest"]
        cohort_output = output / f"track_{track}" / model
        print(f"[eligibility] iniciando {track}/{model}", flush=True)
        command = [
            "python3",
            "-m",
            "avaliacao_prompts.resilience",
            "eligibility",
            "--execution-manifest",
            str(execution_manifest),
            "--playwright-config",
            str(runtime_config),
            "--node-project-dir",
            str(ROOT),
            "--output-dir",
            str(cohort_output),
            "--repetitions",
            str(args.repetitions),
            "--execute-live-site",
        ]
        completed = subprocess.run(
            command,
            cwd=ROOT,
            env=environment,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        log_dir = output / "runner_logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        slug = f"track_{track}__{model}"
        (log_dir / f"{slug}.stdout.txt").write_text(
            completed.stdout,
            encoding="utf-8",
        )
        (log_dir / f"{slug}.stderr.txt").write_text(
            completed.stderr,
            encoding="utf-8",
        )
        result_path = cohort_output / "eligibility_results.json"
        if completed.returncode != 0 or not result_path.is_file():
            raise RuntimeError(
                f"Elegibilidade falhou em {track}/{model}; consulte {log_dir}."
            )
        result = load_json(result_path)
        if not verify_signed_payload(result, "eligibility_results_sha256"):
            raise ValueError(f"Resultado de elegibilidade inválido: {track}/{model}")
        records.append(
            {
                "track_id": track,
                "model_id": model,
                "execution_manifest_sha256": cohort[
                    "execution_manifest_sha256"
                ],
                "result": str(result_path.relative_to(output)),
                "result_file_sha256": sha256_file(result_path),
                "eligibility_results_sha256": result[
                    "eligibility_results_sha256"
                ],
                "eligible_scenarios": result["eligible_scenarios"],
                "ineligible_scenarios": result["ineligible_scenarios"],
            }
        )
        print(
            f"[eligibility] concluído {track}/{model}: "
            f"{len(result['eligible_scenarios'])} elegíveis",
            flush=True,
        )

    payload: dict[str, Any] = {
        "schema_version": 1,
        "campaign_manifest_sha256": campaign_manifest[
            "campaign_manifest_sha256"
        ],
        "campaign_files_aggregate_sha256": campaign_manifest[
            "campaign_files_aggregate_sha256"
        ],
        "runner_sha256": sha256_file(Path(__file__).resolve()),
        "account_helper_sha256": sha256_file(
            ROOT / "tools" / "create_demowebshop_repair_account.mjs"
        ),
        "repetitions": args.repetitions,
        "account": {
            "created_for_this_campaign": account_created,
            "credential_values_recorded_in_results": False,
            "credential_file_outside_repository": str(credential_file),
            "credential_file_mode": oct(stat.S_IMODE(credential_file.stat().st_mode)),
        },
        "configured_environment_names": sorted(
            name
            for name in environment
            if name.startswith(("DEMO_WEB_SHOP_", "E2E_", "TEST_"))
        ),
        "records": records,
    }
    payload["eligibility_campaign_sha256"] = signed_payload_hash(
        payload,
        "eligibility_campaign_sha256",
    )
    manifest_path = output / "eligibility_campaign_manifest.json"
    manifest_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"[eligibility] manifesto: {manifest_path}", flush=True)
    return 0


def load_or_create_credentials(path: Path) -> tuple[dict[str, str], bool]:
    if path.is_file():
        payload = load_json(path)
        return validate_credentials(payload), False

    path.parent.mkdir(parents=True, exist_ok=True)
    completed = subprocess.run(
        ["node", str(ROOT / "tools" / "create_demowebshop_repair_account.mjs")],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            "Não foi possível criar a conta sintética: "
            + " ".join(completed.stderr.split())
        )
    credentials = validate_credentials(json.loads(completed.stdout))
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(credentials, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    temporary.chmod(0o600)
    temporary.replace(path)
    path.chmod(0o600)
    return credentials, True


def validate_credentials(payload: dict[str, Any]) -> dict[str, str]:
    required = ("email", "password", "firstName", "lastName")
    if any(not isinstance(payload.get(name), str) or not payload[name] for name in required):
        raise ValueError("Arquivo de credenciais inválido.")
    return {name: payload[name] for name in required}


def normalized_environment(
    credentials: dict[str, str],
    runtime_python: Path,
) -> dict[str, str]:
    environment = os.environ.copy()
    email = credentials["email"]
    password = credentials["password"]
    environment.update(
        {
            "PYTHONPATH": str(runtime_python),
            "PROMPT_E2E_BASE_URL": "https://demowebshop.tricentis.com/",
            "BASE_URL": "https://demowebshop.tricentis.com",
            "DEMO_WEB_SHOP_EMAIL": email,
            "DEMO_WEB_SHOP_USERNAME": email,
            "DEMO_WEB_SHOP_PASSWORD": password,
            "DEMO_WEB_SHOP_INVALID_PASSWORD": f"{password}-invalid",
            "E2E_EMAIL": email,
            "E2E_USERNAME": email,
            "E2E_PASSWORD": password,
            "TEST_EMAIL": email,
            "TEST_USERNAME": email,
            "TEST_PASSWORD": password,
            "DEMO_WEB_SHOP_FIRST_NAME": credentials["firstName"],
            "DEMO_WEB_SHOP_LAST_NAME": credentials["lastName"],
        }
    )
    return environment


def signed_payload_hash(payload: dict[str, Any], field: str) -> str:
    unsigned = dict(payload)
    unsigned.pop(field, None)
    canonical = json.dumps(
        unsigned,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def verify_signed_payload(payload: dict[str, Any], field: str) -> bool:
    expected = str(payload.get(field, ""))
    return bool(expected) and expected == signed_payload_hash(payload, field)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    raise SystemExit(main())
