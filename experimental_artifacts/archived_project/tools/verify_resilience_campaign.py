#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EVALUATOR = ROOT / "python_app" / "avaliacao_prompts"
sys.path.insert(0, str(EVALUATOR))

from avaliacao_prompts.resilience.plan import verify_plan  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verifica uma campanha congelada.")
    parser.add_argument("campaign_dir", type=Path)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    campaign = args.campaign_dir.resolve()
    report = verify_campaign(campaign)
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        output = args.output.resolve()
        if output.exists():
            raise FileExistsError(output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if report["valid"] else 2


def verify_campaign(campaign: Path) -> dict[str, Any]:
    errors: list[str] = []
    manifest_path = campaign / "campaign_manifest.json"
    manifest = load_json(manifest_path)

    expected_manifest_hash = manifest.get("campaign_manifest_sha256", "")
    unsigned = dict(manifest)
    unsigned.pop("campaign_manifest_sha256", None)
    actual_manifest_hash = sha256_text(canonical_json(unsigned))
    if expected_manifest_hash != actual_manifest_hash:
        errors.append("campaign_manifest_sha256 divergente")

    expected_aggregate = manifest.get("campaign_files_aggregate_sha256", "")
    actual_aggregate = aggregate_campaign_files(campaign)
    if expected_aggregate != actual_aggregate:
        errors.append("campaign_files_aggregate_sha256 divergente")

    inventory_checked = 0
    for item in manifest.get("source_inventory", []):
        destination = Path(item["destination"])
        if not destination.is_file():
            errors.append(f"destino inventariado ausente: {destination}")
            continue
        inventory_checked += 1
        if sha256_file(destination) != item["sha256"]:
            errors.append(f"hash de destino divergente: {destination}")

    runtime_checked = 0
    for name, item in manifest.get("runtime", {}).items():
        path = campaign / item["file"]
        if not path.is_file() or sha256_file(path) != item["sha256"]:
            errors.append(f"runtime congelado divergente: {name}")
        else:
            runtime_checked += 1

    plan_by_path: dict[Path, dict[str, Any]] = {}
    plan_summaries: dict[str, Any] = {}
    for round_id, summary in manifest.get("plans", {}).items():
        path = campaign / summary["file"]
        payload = load_json(path)
        plan_by_path[path.resolve()] = payload
        valid_internal = verify_plan(payload)
        valid_file = sha256_file(path) == summary["sha256"]
        valid_declared = payload.get("plan_sha256") == summary["plan_sha256"]
        if not (valid_internal and valid_file and valid_declared):
            errors.append(f"plano inválido: {round_id}")
        plan_summaries[round_id] = {
            "valid": valid_internal and valid_file and valid_declared,
            "catalog_size": payload.get("catalog_size"),
            "mutation_count": payload.get("mutation_count"),
        }

    cohort_summaries: list[dict[str, Any]] = []
    for cohort in manifest.get("cohorts", []):
        manifest_file = campaign / cohort["execution_manifest"]
        execution = load_json(manifest_file)
        cohort_errors: list[str] = []
        if sha256_file(manifest_file) != cohort["execution_manifest_sha256"]:
            cohort_errors.append("hash externo do manifesto divergente")
        if not verify_execution_manifest(execution):
            cohort_errors.append("hash interno do manifesto divergente")

        plan_path = Path(execution["mutation_plan"]).resolve()
        plan = plan_by_path.get(plan_path)
        if plan is None:
            cohort_errors.append("plano do manifesto não pertence à campanha")
            plan = load_json(plan_path)
        if plan.get("plan_sha256") != execution.get("mutation_plan_sha256"):
            cohort_errors.append("vínculo com plano divergente")

        for key in ("allowlist", "semantic_review", "fixture"):
            path = Path(execution[key])
            expected = execution[f"{key}_sha256"]
            if not path.is_file() or sha256_file(path) != expected:
                cohort_errors.append(f"hash divergente: {key}")
            if key == "fixture" and campaign not in path.resolve().parents:
                cohort_errors.append("fixture não pertence ao pacote congelado")

        target_mutations: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for mutation in plan.get("mutations", []):
            target_mutations[mutation["target"]["scenario_id"]].append(mutation)

        scenarios: list[dict[str, Any]] = []
        for pair in execution.get("pairs", []):
            scenario = pair["scenario_id"]
            for condition, letter in (
                ("baseline", "A"),
                ("structured", "B"),
            ):
                original = Path(pair[f"{condition}_original"])
                prepared = manifest_file.parent / letter / f"{scenario}.spec.ts"
                if not original.is_file():
                    cohort_errors.append(f"original ausente: {scenario}/{condition}")
                elif sha256_file(original) != pair[f"{condition}_sha256"]:
                    cohort_errors.append(f"hash original divergente: {scenario}/{condition}")
                if not prepared.is_file():
                    cohort_errors.append(f"instrumentado ausente: {scenario}/{condition}")
                elif sha256_file(prepared) != pair[f"{condition}_derived"]:
                    cohort_errors.append(f"hash instrumentado divergente: {scenario}/{condition}")

            neutral = [
                mutation
                for mutation in target_mutations.get(scenario, [])
                if mutation["stratum"] in {"E1", "E2"}
            ]
            if len(neutral) < 2:
                cohort_errors.append(f"menos de duas mutações neutras: {scenario}")
            scenarios.append(
                {
                    "scenario_id": scenario,
                    "target_count": len(
                        {
                            mutation["target"]["target_id"]
                            for mutation in target_mutations.get(scenario, [])
                        }
                    ),
                    "neutral_mutation_count": len(neutral),
                    "neutral_strata": sorted(
                        {mutation["stratum"] for mutation in neutral}
                    ),
                }
            )

        if cohort_errors:
            errors.extend(
                f"{execution.get('track_id')}/{execution.get('model_id')}: {error}"
                for error in cohort_errors
            )
        cohort_summaries.append(
            {
                "track_id": execution.get("track_id"),
                "model_id": execution.get("model_id"),
                "pair_count": len(execution.get("pairs", [])),
                "valid": not cohort_errors,
                "scenarios": scenarios,
            }
        )

    return {
        "schema_version": 1,
        "campaign": str(campaign),
        "valid": not errors,
        "status": manifest.get("status"),
        "live_site_requests_performed": manifest.get(
            "live_site_requests_performed"
        ),
        "campaign_manifest_sha256": expected_manifest_hash,
        "campaign_files_aggregate_sha256": expected_aggregate,
        "inventory_files_checked": inventory_checked,
        "runtime_files_checked": runtime_checked,
        "plans": plan_summaries,
        "cohorts": cohort_summaries,
        "errors": errors,
    }


def verify_execution_manifest(payload: dict[str, Any]) -> bool:
    expected = payload.get("execution_manifest_sha256", "")
    unsigned = dict(payload)
    unsigned.pop("execution_manifest_sha256", None)
    return expected == sha256_text(canonical_json(unsigned))


def aggregate_campaign_files(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(
        item
        for item in root.rglob("*")
        if item.is_file() and item.name != "campaign_manifest.json"
    ):
        relative = path.relative_to(root).as_posix()
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(sha256_file(path).encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def canonical_json(payload: Any) -> str:
    return json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    raise SystemExit(main())
