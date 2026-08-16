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
        description="Executa a seleção congelada de mutações da campanha."
    )
    parser.add_argument("--campaign-dir", type=Path, required=True)
    parser.add_argument("--eligibility-dir", type=Path, required=True)
    parser.add_argument("--selection", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--credential-file", type=Path, required=True)
    parser.add_argument("--repetitions", type=int, default=3)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    campaign = args.campaign_dir.resolve()
    eligibility = args.eligibility_dir.resolve()
    selection_path = args.selection.resolve()
    output = args.output_dir.resolve()
    credential_file = args.credential_file.expanduser().resolve()
    if output.exists():
        raise FileExistsError(f"Resultados já existem: {output}")
    if args.repetitions != 3:
        raise ValueError("A campanha congelada exige exatamente três repetições.")
    if not credential_file.is_file():
        raise FileNotFoundError(credential_file)
    if stat.S_IMODE(credential_file.stat().st_mode) != 0o600:
        raise PermissionError("O arquivo de credenciais deve usar permissão 0600.")

    campaign_manifest = load_json(campaign / "campaign_manifest.json")
    eligibility_manifest = load_json(
        eligibility / "eligibility_campaign_manifest.json"
    )
    selection = load_json(selection_path)
    validate_links(campaign_manifest, eligibility_manifest, selection)

    credentials = validate_credentials(load_json(credential_file))
    runtime_python = campaign / "runtime" / "python"
    runtime_playwright = campaign / "runtime" / "playwright"
    environment = normalized_environment(credentials, runtime_python)
    output.mkdir(parents=True)

    cohort_index = {
        (item["track_id"], item["model_id"]): item
        for item in campaign_manifest["cohorts"]
    }
    eligibility_index = {
        (item["track_id"], item["model_id"]): item
        for item in eligibility_manifest["records"]
    }
    records: list[dict[str, Any]] = []
    for selected in selection["records"]:
        key = (selected["track_id"], selected["model_id"])
        cohort = cohort_index[key]
        eligible = eligibility_index[key]
        execution_manifest = campaign / cohort["execution_manifest"]
        eligibility_result = eligibility / eligible["result"]
        cohort_output = output / f"track_{key[0]}" / key[1]
        print(f"[mutations] iniciando {key[0]}/{key[1]}", flush=True)
        command = [
            "python3",
            "-m",
            "avaliacao_prompts.resilience",
            "run",
            "--execution-manifest",
            str(execution_manifest),
            "--eligibility-results",
            str(eligibility_result),
            "--playwright-config",
            str(runtime_playwright / "playwright.config.ts"),
            "--node-project-dir",
            str(ROOT),
            "--control-test",
            str(runtime_playwright / "control.spec.ts"),
            "--output-dir",
            str(cohort_output),
            "--repetitions",
            str(args.repetitions),
            "--mutations-per-scenario",
            "2",
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
        slug = f"track_{key[0]}__{key[1]}"
        (log_dir / f"{slug}.stdout.txt").write_text(
            completed.stdout,
            encoding="utf-8",
        )
        (log_dir / f"{slug}.stderr.txt").write_text(
            completed.stderr,
            encoding="utf-8",
        )
        result_path = cohort_output / "resilience_results.json"
        if completed.returncode != 0 or not result_path.is_file():
            raise RuntimeError(
                f"Campanha falhou em {key[0]}/{key[1]}; consulte {log_dir}."
            )
        result = load_json(result_path)
        expected_ids = [
            item["mutation_id"] for item in selected["selected_mutations"]
        ]
        actual_ids = result["selection"]["selected_mutation_ids"]
        if expected_ids != actual_ids:
            raise ValueError(
                f"Seleção executada diverge da seleção congelada em {key}."
            )
        control_valid = sum(
            mutation["control_valid"]
            for mutation in result["mutation_results"]
        )
        paired_applicable = sum(
            mutation["control_valid"] and mutation["paired_applicable"]
            for mutation in result["mutation_results"]
        )
        records.append(
            {
                "track_id": key[0],
                "model_id": key[1],
                "execution_manifest_sha256": cohort[
                    "execution_manifest_sha256"
                ],
                "eligibility_results_sha256": eligible[
                    "eligibility_results_sha256"
                ],
                "selected_mutation_ids": actual_ids,
                "result": str(result_path.relative_to(output)),
                "result_file_sha256": sha256_file(result_path),
                "markdown_file_sha256": sha256_file(
                    cohort_output / "resilience_results.md"
                ),
                "selected_count": len(result["mutation_results"]),
                "control_valid_count": control_valid,
                "paired_applicable_count": paired_applicable,
            }
        )
        print(
            f"[mutations] concluído {key[0]}/{key[1]}: "
            f"{control_valid} controles válidos, "
            f"{paired_applicable} aplicáveis ao par",
            flush=True,
        )

    payload: dict[str, Any] = {
        "schema_version": 1,
        "campaign_manifest_sha256": campaign_manifest[
            "campaign_manifest_sha256"
        ],
        "eligibility_campaign_sha256": eligibility_manifest[
            "eligibility_campaign_sha256"
        ],
        "mutation_selection_sha256": selection[
            "mutation_selection_sha256"
        ],
        "runner_sha256": sha256_file(Path(__file__).resolve()),
        "repetitions": args.repetitions,
        "credential_values_recorded_in_results": False,
        "configured_environment_names": sorted(
            name
            for name in environment
            if name.startswith(("DEMO_WEB_SHOP_", "E2E_", "TEST_"))
        ),
        "records": records,
    }
    payload["mutation_campaign_sha256"] = signed_hash(
        payload,
        "mutation_campaign_sha256",
    )
    manifest_path = output / "mutation_campaign_manifest.json"
    manifest_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"[mutations] manifesto: {manifest_path}", flush=True)
    return 0


def validate_links(
    campaign: dict[str, Any],
    eligibility: dict[str, Any],
    selection: dict[str, Any],
) -> None:
    if not verify_signature(eligibility, "eligibility_campaign_sha256"):
        raise ValueError("Manifesto de elegibilidade alterado.")
    if not verify_signature(selection, "mutation_selection_sha256"):
        raise ValueError("Seleção de mutações alterada.")
    campaign_hash = campaign["campaign_manifest_sha256"]
    if eligibility["campaign_manifest_sha256"] != campaign_hash:
        raise ValueError("Elegibilidade não pertence à campanha.")
    if selection["campaign_manifest_sha256"] != campaign_hash:
        raise ValueError("Seleção não pertence à campanha.")
    if (
        selection["eligibility_campaign_sha256"]
        != eligibility["eligibility_campaign_sha256"]
    ):
        raise ValueError("Seleção não pertence à elegibilidade.")


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


def signed_hash(payload: dict[str, Any], field: str) -> str:
    unsigned = dict(payload)
    unsigned.pop(field, None)
    canonical = json.dumps(
        unsigned,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def verify_signature(payload: dict[str, Any], field: str) -> bool:
    return payload.get(field) == signed_hash(payload, field)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    raise SystemExit(main())
