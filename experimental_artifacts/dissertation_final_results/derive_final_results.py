#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import statistics
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "archived_project" / "python_app" / "avaliacao_prompts"
QWEN_NEW_ROUND_DUPLICATES = {
    "fluxo_computadores_desktops",
    "user_registration_book_purchase",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def in_final_base(row: dict[str, str], model_key: str = "model") -> bool:
    return not (
        row[model_key] == "qwen2.5-coder:7b"
        and row["round"] == "qwen_new_20"
        and row["scenario"] in QWEN_NEW_ROUND_DUPLICATES
    )


def semantic_results() -> dict[str, object]:
    source = ROOT / "resultados_adequacao_semantica_20260728" / "semantic_review.csv"
    rows = [row for row in read_csv(source) if in_final_base(row)]
    if len(rows) != 128:
        raise SystemExit(f"base semântica inesperada: {len(rows)} arquivos")

    conditions: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    pairs: dict[tuple[str, str], dict[str, dict[str, str]]] = defaultdict(dict)
    for row in rows:
        conditions[(row["model"], row["condition"])].append(row)
        pairs[(row["model"], row["scenario"])][row["condition"]] = row

    condition_summary = []
    for (model, condition), group in sorted(conditions.items()):
        condition_summary.append(
            {
                "model": model,
                "condition": condition,
                "files": len(group),
                "execution_passed": sum(row["execution_status"] == "passed" for row in group),
                "adequate": sum(row["semantic_classification"] == "adequate" for row in group),
                "partially_adequate": sum(
                    row["semantic_classification"] == "partially_adequate" for row in group
                ),
                "inadequate": sum(row["semantic_classification"] == "inadequate" for row in group),
                "mean_semantic_score_6": round(
                    sum(int(row["semantic_total_6"]) for row in group) / len(group), 3
                ),
            }
        )

    paired_summary = []
    for model in sorted({row["model"] for row in rows}):
        group = [value for (item_model, _), value in pairs.items() if item_model == model]
        deltas = [
            int(pair["structured_context"]["semantic_total_6"])
            - int(pair["baseline"]["semantic_total_6"])
            for pair in group
        ]
        paired_summary.append(
            {
                "model": model,
                "pairs": len(group),
                "execution": {
                    "both_passed": sum(
                        pair["baseline"]["execution_status"] == "passed"
                        and pair["structured_context"]["execution_status"] == "passed"
                        for pair in group
                    ),
                    "baseline_only": sum(
                        pair["baseline"]["execution_status"] == "passed"
                        and pair["structured_context"]["execution_status"] != "passed"
                        for pair in group
                    ),
                    "structured_only": sum(
                        pair["baseline"]["execution_status"] != "passed"
                        and pair["structured_context"]["execution_status"] == "passed"
                        for pair in group
                    ),
                    "neither_passed": sum(
                        pair["baseline"]["execution_status"] != "passed"
                        and pair["structured_context"]["execution_status"] != "passed"
                        for pair in group
                    ),
                },
                "semantic_scores": {
                    "structured_improved": sum(delta > 0 for delta in deltas),
                    "same_score": sum(delta == 0 for delta in deltas),
                    "structured_worsened": sum(delta < 0 for delta in deltas),
                    "mean_delta": round(sum(deltas) / len(deltas), 3),
                    "median_delta": statistics.median(deltas),
                },
            }
        )
    return {"conditions": condition_summary, "paired": paired_summary}


def repair_results() -> dict[str, object]:
    source = (
        ROOT
        / "repair_results"
        / "qwen25coder_repair_20260728_01"
        / "consolidated"
        / "repair_effort.csv"
    )
    rows = [row for row in read_csv(source) if in_final_base(row, model_key="model_origin")]
    if len(rows) != 91:
        raise SystemExit(f"base de correção inesperada: {len(rows)} arquivos")
    successful = sum(row["successful_repair"].lower() == "true" for row in rows)
    return {
        "attempted": len(rows),
        "collected": sum(row["collection_status"] == "collected" for row in rows),
        "execution_passed": sum(row["execution_status_after_repair"] == "passed" for row in rows),
        "successful_repairs": successful,
        "success_rate": round(successful / len(rows), 6),
        "client_seconds_total": round(sum(float(row["elapsed_seconds_client"]) for row in rows), 3),
        "prompt_tokens": sum(int(row["prompt_eval_count"]) for row in rows),
        "output_tokens": sum(int(row["eval_count"]) for row in rows),
        "line_churn": sum(int(row["lines_added"]) + int(row["lines_deleted"]) for row in rows),
        "mean_line_similarity": round(
            sum(float(row["line_similarity_ratio"]) for row in rows) / len(rows), 6
        ),
    }


def main() -> None:
    print(json.dumps({"semantic": semantic_results(), "repair": repair_results()}, indent=2))


if __name__ == "__main__":
    main()
