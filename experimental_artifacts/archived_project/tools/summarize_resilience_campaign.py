#!/usr/bin/env python3
"""Verify and consolidate the frozen resilience campaign results."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from collections import Counter, defaultdict
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def exact_mcnemar_p(baseline_only: int, structured_only: int) -> float:
    discordant = baseline_only + structured_only
    if discordant == 0:
        return 1.0
    lower = min(baseline_only, structured_only)
    tail = sum(math.comb(discordant, k) for k in range(lower + 1)) / (2**discordant)
    return min(1.0, 2 * tail)


def robust(outcomes: list[str]) -> bool:
    return len(outcomes) == 3 and all(item == "passed_interacted" for item in outcomes)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--results-root",
        type=Path,
        default=Path(
            "python_app/avaliacao_prompts/resilience_campaign_results/"
            "campaign_20260728_01"
        ),
    )
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()

    root = args.results_root.resolve()
    mutation_root = root / "mutations"
    output = (args.output_dir or mutation_root / "consolidated").resolve()
    output.mkdir(parents=True, exist_ok=True)

    manifest_path = mutation_root / "mutation_campaign_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    verification_errors: list[str] = []
    units: list[dict] = []
    repetitions: list[dict] = []

    for record in manifest["records"]:
        result_path = mutation_root / record["result"]
        if sha256(result_path) != record["result_file_sha256"]:
            verification_errors.append(f"hash divergente: {result_path}")
        markdown_path = result_path.with_suffix(".md")
        if sha256(markdown_path) != record["markdown_file_sha256"]:
            verification_errors.append(f"hash divergente: {markdown_path}")

        data = json.loads(result_path.read_text(encoding="utf-8"))
        if data["track_id"] != record["track_id"] or data["model_id"] != record["model_id"]:
            verification_errors.append(f"identidade divergente: {result_path}")
        if len(data["mutation_results"]) != record["selected_count"]:
            verification_errors.append(f"contagem divergente: {result_path}")

        for item in data["mutation_results"]:
            outcomes_a = [run["outcomes"]["A"] for run in item["condition_runs"]]
            outcomes_b = [run["outcomes"]["B"] for run in item["condition_runs"]]
            robust_a = robust(outcomes_a) if item["paired_applicable"] else False
            robust_b = robust(outcomes_b) if item["paired_applicable"] else False
            paired = (
                "ambos"
                if robust_a and robust_b
                else "somente_baseline"
                if robust_a
                else "somente_estruturado"
                if robust_b
                else "nenhum"
                if item["paired_applicable"]
                else "nao_aplicavel"
            )
            units.append(
                {
                    "track": data["track_id"],
                    "model": data["model_id"],
                    "scenario": item["scenario_id"],
                    "mutation_id": item["mutation_id"],
                    "stratum": item["stratum"],
                    "operator": item["operator"],
                    "control_valid": item["control_valid"],
                    "paired_applicable": item["paired_applicable"],
                    "invalid_reasons": "|".join(item["invalid_reasons"]),
                    "baseline_robust_3_of_3": robust_a,
                    "structured_robust_3_of_3": robust_b,
                    "paired_result": paired,
                    "baseline_outcomes": "|".join(outcomes_a),
                    "structured_outcomes": "|".join(outcomes_b),
                }
            )
            for run in item["condition_runs"]:
                for condition, approach in (("A", "baseline"), ("B", "structured")):
                    detail = run["details"][condition]
                    repetitions.append(
                        {
                            "track": data["track_id"],
                            "model": data["model_id"],
                            "scenario": item["scenario_id"],
                            "mutation_id": item["mutation_id"],
                            "stratum": item["stratum"],
                            "operator": item["operator"],
                            "repetition": run["repetition"],
                            "execution_order": "|".join(run["order"]),
                            "condition": condition,
                            "approach": approach,
                            "outcome": run["outcomes"][condition],
                            "returncode": detail["returncode"],
                            "duration_seconds": detail["duration_seconds"],
                            "error_type": detail["error_type"],
                            "artifacts_dir": detail["artifacts_dir"],
                        }
                    )

    if verification_errors:
        raise SystemExit("\n".join(verification_errors))

    artifact_dirs = list(mutation_root.rglob("*.artifacts"))
    trace_count = sum(
        1 for path in artifact_dirs if any(path.rglob("trace.zip"))
    )
    screenshot_count = sum(
        1 for path in artifact_dirs if any(path.rglob("*.png"))
    )
    evidence = {
        "eligibility_playwright_executions": 66,
        "mutation_control_executions": sum(
            len(json.loads((mutation_root / r["result"]).read_text())["mutation_results"])
            * 6
            for r in manifest["records"]
        ),
        "mutation_exposure_executions": sum(
            6 for unit in units if unit["control_valid"]
        ),
        "mutation_condition_executions": len(repetitions),
        "mutation_total_playwright_executions": (
            20 * 6
            + sum(6 for unit in units if unit["control_valid"])
            + len(repetitions)
        ),
        "resilience_total_playwright_executions": (
            66
            + 20 * 6
            + sum(6 for unit in units if unit["control_valid"])
            + len(repetitions)
        ),
        "mutation_artifact_directories": len(artifact_dirs),
        "mutation_traces": trace_count,
        "mutation_screenshot_directories": screenshot_count,
    }

    def aggregate(rows: list[dict], key: tuple[str, ...]) -> list[dict]:
        groups: dict[tuple, list[dict]] = defaultdict(list)
        for row in rows:
            groups[tuple(row[name] for name in key)].append(row)
        result = []
        for identity, group in sorted(groups.items()):
            applicable = [row for row in group if row["paired_applicable"]]
            both = sum(row["paired_result"] == "ambos" for row in applicable)
            baseline_only = sum(
                row["paired_result"] == "somente_baseline" for row in applicable
            )
            structured_only = sum(
                row["paired_result"] == "somente_estruturado" for row in applicable
            )
            neither = sum(row["paired_result"] == "nenhum" for row in applicable)
            baseline = sum(row["baseline_robust_3_of_3"] for row in applicable)
            structured = sum(row["structured_robust_3_of_3"] for row in applicable)
            result.append(
                {
                    **dict(zip(key, identity)),
                    "selected": len(group),
                    "control_valid": sum(row["control_valid"] for row in group),
                    "applicable": len(applicable),
                    "baseline_survived": baseline,
                    "baseline_rate": baseline / len(applicable) if applicable else None,
                    "structured_survived": structured,
                    "structured_rate": structured / len(applicable) if applicable else None,
                    "both": both,
                    "baseline_only": baseline_only,
                    "structured_only": structured_only,
                    "neither": neither,
                    "mcnemar_exact_two_sided_p": exact_mcnemar_p(
                        baseline_only, structured_only
                    )
                    if applicable
                    else None,
                }
            )
        return result

    summary = {
        "schema_version": 1,
        "campaign": "campaign_20260728_01",
        "verified": True,
        "mutation_campaign_manifest_sha256": sha256(manifest_path),
        "signed_mutation_campaign_sha256": manifest["mutation_campaign_sha256"],
        "condition_mapping": {"A": "baseline", "B": "structured"},
        "robustness_rule": "passed_interacted em 3 de 3 repeticoes",
        "overall": aggregate(units, tuple())[0],
        "by_track_and_model": aggregate(units, ("track", "model")),
        "by_track": aggregate(units, ("track",)),
        "by_model": aggregate(units, ("model",)),
        "by_operator": aggregate(units, ("operator",)),
        "by_stratum": aggregate(units, ("stratum",)),
        "invalid_reason_counts": dict(
            Counter(
                reason
                for row in units
                for reason in row["invalid_reasons"].split("|")
                if reason
            )
        ),
        "execution_evidence": evidence,
    }

    unit_fields = list(units[0])
    repetition_fields = list(repetitions[0])
    write_csv(output / "mutation_units.csv", units, unit_fields)
    write_csv(output / "paired_repetitions.csv", repetitions, repetition_fields)
    (output / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    lines = [
        "# Consolidação da campanha de mutações",
        "",
        f"- Manifesto verificado: `{summary['mutation_campaign_manifest_sha256']}`",
        f"- Unidades selecionadas: {summary['overall']['selected']}",
        f"- Controles válidos: {summary['overall']['control_valid']}",
        f"- Unidades pareadas aplicáveis: {summary['overall']['applicable']}",
        f"- Execuções Playwright de resiliência (elegibilidade + mutação): "
        f"{evidence['resilience_total_playwright_executions']}",
        "",
        "## Resultado por coorte",
        "",
        "| Trilha | Modelo | Aplicáveis | Baseline | Estruturado | Só estruturado | p McNemar |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for row in summary["by_track_and_model"]:
        lines.append(
            f"| {row['track']} | {row['model']} | {row['applicable']} | "
            f"{row['baseline_survived']}/{row['applicable']} | "
            f"{row['structured_survived']}/{row['applicable']} | "
            f"{row['structured_only']} | {row['mcnemar_exact_two_sided_p']:.3f} |"
        )
    lines += [
        "",
        "A condição A corresponde ao baseline e a condição B ao contexto estruturado. "
        "A sobrevivência exige aprovação com interação comprovada no alvo em três de "
        "três repetições. Unidades sem controle válido ou sem exposição pareada foram "
        "excluídas do denominador.",
        "",
    ]
    (output / "summary.md").write_text("\n".join(lines), encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
