#!/usr/bin/env python3
"""Consolida esforço, eficácia e elegibilidade provisória da rodada de reparo."""

from __future__ import annotations

import argparse
import csv
import json
import statistics
from collections import Counter, defaultdict
from pathlib import Path


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evaluation-manifest", type=Path, required=True)
    parser.add_argument("--semantic-review", type=Path, required=True)
    parser.add_argument("--original-review", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args()


def failure_class(record: dict) -> str:
    if record["collection_status"] != "collected":
        return "collection_error"
    if record["execution_status_after_repair"] == "passed":
        return "passed"
    message = record.get("failure_message_after_repair", "").lower()
    if "strict mode violation" in message:
        return "selector_ambiguity"
    if "timeouterror" in message and ("locator" in message or "waiting for" in message):
        return "locator_timeout"
    if "net::err_" in message:
        return "navigation_or_environment"
    if "referenceerror" in message or "typeerror" in message or "can be only used with locator" in message:
        return "runtime_code_error"
    if "expect(" in message or "expected:" in message or "received:" in message:
        return "assertion_failure"
    if "expected string, got undefined" in message or "environment variable" in message:
        return "environment_configuration"
    return "other_generated_test_failure"


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> int:
    args = arguments()
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    evaluation = json.loads(args.evaluation_manifest.read_text(encoding="utf-8"))
    records = evaluation["records"]
    semantic_rows = load_csv(args.semantic_review)
    semantic = {
        (row["model_origin"], row["round"], row["condition"], row["scenario"]): row
        for row in semantic_rows
    }
    original_rows = load_csv(args.original_review)
    enriched = []
    for record in records:
        key = (
            record["model_origin"],
            record["round"],
            record["condition"],
            record["scenario"],
        )
        review = semantic.get(key)
        enriched.append(
            record
            | {
                "failure_class_after_repair": failure_class(record),
                "semantic_total_after_repair": int(review["semantic_total_6"]) if review else None,
                "semantic_classification_after_repair": review["semantic_classification"] if review else "not_reviewed_execution_failed",
                "successful_repair": bool(
                    record["execution_status_after_repair"] == "passed"
                    and review
                    and review["semantic_classification"] == "adequate"
                ),
            }
        )

    fields = list(enriched[0])
    with (output / "repair_effort.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(enriched)

    groups: dict[tuple[str, str, str], list[dict]] = defaultdict(list)
    for record in enriched:
        groups[(record["model_origin"], record["round"], record["condition"])].append(record)
    group_summary = []
    for (model, round_id, condition), items in sorted(groups.items()):
        group_summary.append(
            {
                "model_origin": model,
                "round": round_id,
                "condition": condition,
                "attempted": len(items),
                "collected": sum(item["collection_status"] == "collected" for item in items),
                "execution_passed": sum(item["execution_status_after_repair"] == "passed" for item in items),
                "successful_repairs": sum(item["successful_repair"] for item in items),
                "repair_success_rate": round(sum(item["successful_repair"] for item in items) / len(items), 4),
                "client_seconds_total": round(sum(item["elapsed_seconds_client"] for item in items), 3),
                "client_seconds_mean": round(statistics.mean(item["elapsed_seconds_client"] for item in items), 3),
                "prompt_tokens": sum(item.get("prompt_eval_count") or 0 for item in items),
                "output_tokens": sum(item.get("eval_count") or 0 for item in items),
                "line_churn": sum(item["lines_added"] + item["lines_deleted"] for item in items),
                "mean_line_similarity": round(statistics.mean(item["line_similarity_ratio"] for item in items), 4),
            }
        )

    # Estado híbrido provisório: arquivo original quando já passava; cópia
    # reparada quando a tentativa passou e recebeu 6/6.
    state: dict[tuple[str, str, str], dict[str, bool]] = defaultdict(dict)
    for row in original_rows:
        key = (row["model"], row["round"], row["scenario"])
        state[key][row["condition"]] = (
            row["execution_status"] == "passed"
            and row["semantic_classification"] == "adequate"
        )
    for item in enriched:
        key = (item["model_origin"], item["round"], item["scenario"])
        if item["successful_repair"]:
            state[key][item["condition"]] = True
    eligible = [
        {
            "model": model,
            "round": round_id,
            "scenario": scenario,
        }
        for (model, round_id, scenario), conditions in sorted(state.items())
        if conditions.get("baseline") and conditions.get("structured_context")
    ]

    totals = {
        "attempted": len(enriched),
        "collected": sum(item["collection_status"] == "collected" for item in enriched),
        "execution_passed": sum(item["execution_status_after_repair"] == "passed" for item in enriched),
        "semantic_false_passes": sum(
            item["execution_status_after_repair"] == "passed" and not item["successful_repair"]
            for item in enriched
        ),
        "successful_repairs": sum(item["successful_repair"] for item in enriched),
        "repair_success_rate": round(sum(item["successful_repair"] for item in enriched) / len(enriched), 4),
        "client_seconds_total": round(sum(item["elapsed_seconds_client"] for item in enriched), 3),
        "client_seconds_median": round(statistics.median(item["elapsed_seconds_client"] for item in enriched), 3),
        "prompt_tokens": sum(item.get("prompt_eval_count") or 0 for item in enriched),
        "output_tokens": sum(item.get("eval_count") or 0 for item in enriched),
        "lines_added": sum(item["lines_added"] for item in enriched),
        "lines_deleted": sum(item["lines_deleted"] for item in enriched),
        "line_churn": sum(item["lines_added"] + item["lines_deleted"] for item in enriched),
        "mean_line_similarity": round(statistics.mean(item["line_similarity_ratio"] for item in enriched), 4),
        "failure_classes": dict(Counter(item["failure_class_after_repair"] for item in enriched)),
    }
    successes = max(totals["successful_repairs"], 1)
    totals["client_seconds_per_successful_repair"] = round(totals["client_seconds_total"] / successes, 3)
    totals["tokens_per_successful_repair"] = round(
        (totals["prompt_tokens"] + totals["output_tokens"]) / successes, 1
    )

    summary = {
        "repair_model": "qwen2.5-coder:7b",
        "attempts_per_file": 1,
        "totals": totals,
        "groups": group_summary,
        "provisional_mutation_eligible_pairs": eligible,
        "provisional_eligible_pair_count": len(eligible),
        "notes": [
            "Original generated files were not modified.",
            "Execution pass alone was not accepted as successful repair.",
            "Eligibility is provisional until three normalized original/repaired repetitions are completed.",
            "Repaired and unrepaired artifacts must be reported as separate resilience tracks.",
        ],
    }
    (output / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    lines = [
        "# Resultado da rodada única de reparo",
        "",
        "Todos os arquivos receberam no máximo uma chamada sem estado ao Qwen 2.5 Coder 7B.",
        "Aprovação em execução só conta como reparo bem-sucedido quando a revisão também confirma 6/6.",
        "",
        "## Visão geral",
        "",
        "| Indicador | Resultado |",
        "| --- | ---: |",
        f"| Arquivos reparados | {totals['attempted']} |",
        f"| Coletáveis após reparo | {totals['collected']} |",
        f"| Aprovados em execução | {totals['execution_passed']} |",
        f"| Falsos sucessos semânticos | {totals['semantic_false_passes']} |",
        f"| Reparos executáveis e semanticamente adequados | {totals['successful_repairs']} |",
        f"| Taxa efetiva de reparo | {100 * totals['repair_success_rate']:.1f}% |",
        f"| Tempo total de inferência | {totals['client_seconds_total']:.1f} s |",
        f"| Tokens de entrada | {totals['prompt_tokens']} |",
        f"| Tokens de saída | {totals['output_tokens']} |",
        f"| Churn total | {totals['line_churn']} linhas |",
        f"| Tempo por reparo efetivo | {totals['client_seconds_per_successful_repair']:.1f} s |",
        "",
        "## Resultado por origem",
        "",
        "| Origem | Rodada | Condição | Tentados | Coletados | Passaram | Reparos efetivos | Tempo médio (s) | Tokens | Churn |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for item in group_summary:
        lines.append(
            f"| {item['model_origin']} | {item['round']} | {item['condition']} | "
            f"{item['attempted']} | {item['collected']} | {item['execution_passed']} | "
            f"{item['successful_repairs']} | {item['client_seconds_mean']:.1f} | "
            f"{item['prompt_tokens'] + item['output_tokens']} | {item['line_churn']} |"
        )
    lines += [
        "",
        "## Pares provisoriamente elegíveis para mutação após reparo",
        "",
    ]
    for item in eligible:
        lines.append(f"- {item['model']} / {item['round']} / {item['scenario']}")
    lines += [
        "",
        "Os pares acima combinam testes originais já aprovados com reparos efetivos.",
        "Eles ainda precisam passar em três repetições normalizadas antes do congelamento.",
        "O fluxo de registro e compra deve permanecer fora da campanha no site público",
        "por criar contas permanentes.",
        "",
    ]
    (output / "summary.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
