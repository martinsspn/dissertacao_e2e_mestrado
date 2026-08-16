#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EVALUATOR = ROOT / "python_app" / "avaliacao_prompts"
sys.path.insert(0, str(EVALUATOR))

from avaliacao_prompts.resilience.run import _select_mutations  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--campaign-dir", type=Path, required=True)
    parser.add_argument("--eligibility-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    campaign = args.campaign_dir.resolve()
    eligibility = args.eligibility_dir.resolve()
    output = args.output.resolve()
    if output.exists():
        raise FileExistsError(output)
    campaign_manifest = load_json(campaign / "campaign_manifest.json")
    eligibility_manifest = load_json(
        eligibility / "eligibility_campaign_manifest.json"
    )
    if (
        eligibility_manifest["campaign_manifest_sha256"]
        != campaign_manifest["campaign_manifest_sha256"]
    ):
        raise ValueError("Elegibilidade não pertence à campanha.")
    if not verify_signature(
        eligibility_manifest,
        "eligibility_campaign_sha256",
    ):
        raise ValueError("Manifesto de elegibilidade alterado.")

    records: list[dict[str, Any]] = []
    cohort_index = {
        (item["track_id"], item["model_id"]): item
        for item in campaign_manifest["cohorts"]
    }
    for eligibility_record in eligibility_manifest["records"]:
        key = (
            eligibility_record["track_id"],
            eligibility_record["model_id"],
        )
        cohort = cohort_index[key]
        execution = load_json(campaign / cohort["execution_manifest"])
        plan = load_json(Path(execution["mutation_plan"]))
        result_path = eligibility / eligibility_record["result"]
        result = load_json(result_path)
        if not verify_signature(result, "eligibility_results_sha256"):
            raise ValueError(f"Elegibilidade alterada: {key}")

        eligible = set(result["eligible_scenarios"])
        candidates = [
            mutation
            for mutation in plan["mutations"]
            if mutation["target"]["scenario_id"] in eligible
        ]
        selected = _select_mutations(
            candidates,
            plan_hash=plan["plan_sha256"],
            per_scenario=2,
        )
        expected_count = len(eligible) * 2
        if len(selected) != expected_count:
            raise ValueError(
                f"Seleção incompleta para {key}: {len(selected)}/{expected_count}"
            )
        records.append(
            {
                "track_id": key[0],
                "model_id": key[1],
                "execution_manifest_sha256": execution[
                    "execution_manifest_sha256"
                ],
                "eligibility_results_sha256": result[
                    "eligibility_results_sha256"
                ],
                "plan_sha256": plan["plan_sha256"],
                "eligible_scenarios": sorted(eligible),
                "selected_mutations": [
                    {
                        "mutation_id": mutation["mutation_id"],
                        "scenario_id": mutation["target"]["scenario_id"],
                        "target_id": mutation["target"]["target_id"],
                        "stratum": mutation["stratum"],
                        "operator": mutation["operator"],
                    }
                    for mutation in selected
                ],
            }
        )

    payload: dict[str, Any] = {
        "schema_version": 1,
        "campaign_manifest_sha256": campaign_manifest[
            "campaign_manifest_sha256"
        ],
        "eligibility_campaign_sha256": eligibility_manifest[
            "eligibility_campaign_sha256"
        ],
        "selection_rule": (
            "two_neutral_mutations_per_scenario:"
            "one_E1_then_one_E2_when_available_else_second_E1:"
            "hash_ranked_reduced-neutral-v1"
        ),
        "records": records,
    }
    payload["mutation_selection_sha256"] = signed_hash(
        payload,
        "mutation_selection_sha256",
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


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


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    raise SystemExit(main())
