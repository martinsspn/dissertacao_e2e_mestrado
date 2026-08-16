#!/usr/bin/env python3
"""Create an indexed, reproducible snapshot of the dissertation experiment data."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
OUT = REPO / (
    "python_app/avaliacao_prompts/"
    "dissertation_results_snapshot_20260728_01"
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256(path.read_bytes())
    return digest.hexdigest()


def relative(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(REPO))
    except ValueError:
        return str(path.resolve())


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def gemini_effort(root: Path) -> dict:
    result = {}
    for condition in ("baseline", "structured_context"):
        records = [
            load(path) for path in sorted((root / condition).glob("*/metadata.json"))
        ]
        if len(records) != 20 or any(item["status"] != "completed" for item in records):
            raise RuntimeError(f"metadados Gemini incompletos: {condition}")
        result[condition] = {
            "requests": len(records),
            "elapsed_seconds": round(
                sum(float(item["elapsed_seconds"]) for item in records), 3
            ),
            "input_tokens": sum(
                int(item["usage"]["total_input_tokens"]) for item in records
            ),
            "output_tokens": sum(
                int(item["usage"]["total_output_tokens"]) for item in records
            ),
            "thought_tokens": sum(
                int(item["usage"]["total_thought_tokens"]) for item in records
            ),
            "total_tokens": sum(
                int(item["usage"]["total_tokens"]) for item in records
            ),
        }
    return result


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    semantic_path = REPO / (
        "python_app/avaliacao_prompts/"
        "resultados_adequacao_semantica_20260728/summary.json"
    )
    semantic_csv = semantic_path.with_name("semantic_review.csv")
    qwen_generation_path = REPO / (
        "python_app/teste_prompt_e2e_semantico/ollama_runs/"
        "ollama_qwen25coder_demowebshop20_20260727_01/generation_summary.json"
    )
    qwen_execution_path = REPO / (
        "python_app/avaliacao_prompts/"
        "resultados_qwen25coder_demowebshop20_20260727_01/execution_summary.json"
    )
    repair_path = REPO / (
        "python_app/avaliacao_prompts/repair_results/"
        "qwen25coder_repair_20260728_01/consolidated/summary.json"
    )
    resilience_path = REPO / (
        "python_app/avaliacao_prompts/resilience_campaign_results/"
        "campaign_20260728_01/mutations/consolidated/summary.json"
    )
    eligibility_path = REPO / (
        "python_app/avaliacao_prompts/resilience_campaign_results/"
        "campaign_20260728_01/eligibility/eligibility_campaign_manifest.json"
    )
    mutation_manifest_path = resilience_path.parents[1] / "mutation_campaign_manifest.json"
    frozen_campaign_path = REPO / (
        "python_app/avaliacao_prompts/resilience_campaigns/"
        "campaign_20260728_01/campaign_manifest.json"
    )
    gemini_root = Path(
        "/home/martinsspn/openai_playwright_batch/runs/"
        "gemini-3.6-flash-demowebshop20-20260727"
    )

    semantic = load(semantic_path)
    qwen_generation = load(qwen_generation_path)
    repair = load(repair_path)
    resilience = load(resilience_path)
    gemini_generation = gemini_effort(gemini_root)

    condition_rows = semantic["conditions"]
    with (OUT / "generation_execution_semantic.csv").open(
        "w", newline="", encoding="utf-8"
    ) as stream:
        writer = csv.DictWriter(stream, fieldnames=list(condition_rows[0]))
        writer.writeheader()
        writer.writerows(condition_rows)

    paired_rows = semantic["paired_comparison"]
    with (OUT / "paired_semantic_comparison.csv").open(
        "w", newline="", encoding="utf-8"
    ) as stream:
        writer = csv.DictWriter(stream, fieldnames=list(paired_rows[0]))
        writer.writeheader()
        writer.writerows(paired_rows)

    sources = [
        ("semantic_review", "official", semantic_path),
        ("semantic_review_rows", "official", semantic_csv),
        ("qwen_new_generation", "official", qwen_generation_path),
        ("qwen_new_execution", "official", qwen_execution_path),
        (
            "gpt_static_comparison",
            "official",
            REPO / "python_app/avaliacao_prompts/relatorios/comparativo_resultados.md",
        ),
        (
            "qwen_old_static_execution",
            "official_post_locator_instruction",
            REPO
            / (
                "python_app/avaliacao_prompts/relatorios/"
                "comparativo_qwen_playwright_locators_20260724_02.md"
            ),
        ),
        ("repair_summary", "official", repair_path),
        (
            "repair_effort_rows",
            "official",
            repair_path.with_name("repair_effort.csv"),
        ),
        ("resilience_summary", "official", resilience_path),
        (
            "resilience_mutation_units",
            "official",
            resilience_path.with_name("mutation_units.csv"),
        ),
        (
            "resilience_repetitions",
            "official",
            resilience_path.with_name("paired_repetitions.csv"),
        ),
        ("eligibility_manifest", "official_signed", eligibility_path),
        ("mutation_manifest", "official_signed", mutation_manifest_path),
        ("frozen_campaign_manifest", "official_signed", frozen_campaign_path),
        (
            "resilience_protocol",
            "official",
            REPO / "docs/plano_experimento_mutacao_20260728.md",
        ),
        (
            "repair_protocol",
            "official",
            REPO / "docs/protocolo_rodada_reparo_20260728.md",
        ),
        (
            "gemini_generation_manifest",
            "external_auxiliary_repository",
            gemini_root / "run_manifest.json",
        ),
    ]
    index_rows = []
    for category, status, path in sources:
        if not path.is_file():
            raise FileNotFoundError(path)
        index_rows.append(
            {
                "category": category,
                "status": status,
                "path": relative(path),
                "sha256": sha256(path),
                "bytes": path.stat().st_size,
            }
        )
    with (OUT / "artifact_index.csv").open(
        "w", newline="", encoding="utf-8"
    ) as stream:
        writer = csv.DictWriter(stream, fieldnames=list(index_rows[0]))
        writer.writeheader()
        writer.writerows(index_rows)

    summary = {
        "schema_version": 1,
        "snapshot_id": "dissertation_results_snapshot_20260728_01",
        "latex_modified": False,
        "scope": {
            "generated_test_files_reviewed": semantic["total_files"],
            "paired_scenarios": sum(item["pairs"] for item in paired_rows),
            "rounds": [
                "gpt_original_12",
                "qwen_old_14",
                "qwen_new_20",
                "gemini_new_20",
            ],
            "conditions": ["baseline", "structured_context"],
        },
        "execution_and_semantic_conformity": semantic,
        "generation_effort": {
            "qwen_new_20": qwen_generation,
            "gemini_new_20": {
                "model": "gemini-3.6-flash",
                "reasoning_effort": "medium",
                "stateless_requests": True,
                "conditions": gemini_generation,
                "source": relative(gemini_root / "run_manifest.json"),
            },
            "gpt_original_12": {
                "tokens": None,
                "elapsed_seconds": None,
                "availability": "not_recorded_in_original_interactive_generation",
            },
        },
        "static_analysis_reported": {
            "gpt_original_12": {
                "source": (
                    "python_app/avaliacao_prompts/relatorios/"
                    "comparativo_resultados.md"
                ),
                "baseline": {
                    "low_risk_files": "6/12",
                    "graph_url_coverage_percent": 100.0,
                    "graph_text_coverage_percent": 88.2,
                    "getby_share_percent": 49.4,
                    "mean_locators_per_test": 13.67,
                    "mean_actions_per_test": 8.33,
                    "mean_prompt_characters": 386,
                },
                "structured_context": {
                    "low_risk_files": "11/12",
                    "graph_url_coverage_percent": 100.0,
                    "graph_text_coverage_percent": 96.5,
                    "getby_share_percent": 72.8,
                    "mean_locators_per_test": 13.17,
                    "mean_actions_per_test": 6.92,
                    "mean_prompt_characters": 3480,
                },
            },
            "qwen_old_14_post_locator_instruction": {
                "source": (
                    "python_app/avaliacao_prompts/relatorios/"
                    "comparativo_qwen_playwright_locators_20260724_02.md"
                ),
                "baseline": {
                    "execution_passed": "0/14",
                    "graph_url_coverage_percent": 60.7,
                    "graph_text_coverage_percent": 91.1,
                    "low_risk_files": "0/14",
                    "mean_human_review_score_12": 4.43,
                },
                "structured_context": {
                    "execution_passed": "2/14",
                    "graph_url_coverage_percent": 100.0,
                    "graph_text_coverage_percent": 90.8,
                    "low_risk_files": "7/14",
                    "mean_human_review_score_12": 7.43,
                },
            },
        },
        "repair_effort": repair,
        "resilience": resilience,
        "exclusions_and_limits": [
            "Pilotos de mutacao anteriores ao congelamento foram excluidos.",
            "Unidades sem controle valido ou sem exposicao pareada foram excluidas "
            "do denominador de sobrevivencia.",
            "Resultados agregados entre modelos sao secundarios; a leitura principal "
            "deve permanecer separada por modelo e rodada.",
            "Aprovacao de execucao nao implica conformidade semantica.",
            "Tokens e tempo da geracao interativa original do GPT nao foram registrados.",
        ],
        "artifact_index": "artifact_index.csv",
    }
    (OUT / "metrics_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    rows_by_key = {
        (row["model"], row["round"], row["condition"]): row for row in condition_rows
    }
    markdown = [
        "# Snapshot consolidado dos resultados",
        "",
        "Este diretório reúne as métricas derivadas e aponta, por hash SHA-256, "
        "para os artefatos primários. Nenhum arquivo LaTeX foi alterado.",
        "",
        "## Execução e adequação semântica",
        "",
        "| Modelo/rodada | Baseline: execução | Estruturado: execução | "
        "Baseline: adequado | Estruturado: adequado |",
        "|---|---:|---:|---:|---:|",
    ]
    for model, round_id in (
        ("gpt-5.6-sol", "gpt_original_12"),
        ("gemini-3.6-flash", "gemini_new_20"),
        ("qwen2.5-coder:7b", "qwen_new_20"),
        ("qwen2.5-coder:7b", "qwen_old_14"),
    ):
        a = rows_by_key[(model, round_id, "baseline")]
        b = rows_by_key[(model, round_id, "structured_context")]
        markdown.append(
            f"| {model} / {round_id} | {a['execution_passed']}/{a['files']} | "
            f"{b['execution_passed']}/{b['files']} | {a['adequate']}/{a['files']} | "
            f"{b['adequate']}/{b['files']} |"
        )
    overall = resilience["overall"]
    markdown += [
        "",
        "## Reparo",
        "",
        f"- Tentativas: {repair['totals']['attempted']}; coletadas: "
        f"{repair['totals']['collected']}.",
        f"- Reparos efetivos: {repair['totals']['successful_repairs']} "
        f"({repair['totals']['repair_success_rate'] * 100:.2f}%).",
        f"- Tempo total de inferência: "
        f"{repair['totals']['client_seconds_total']:.3f} s; tokens de entrada/saída: "
        f"{repair['totals']['prompt_tokens']}/{repair['totals']['output_tokens']}.",
        "",
        "## Resiliência",
        "",
        f"- 20 mutações selecionadas, {overall['control_valid']} controles válidos e "
        f"{overall['applicable']} unidades pareadas aplicáveis.",
        f"- Sobrevivência robusta: baseline {overall['baseline_survived']}/"
        f"{overall['applicable']}; contexto estruturado "
        f"{overall['structured_survived']}/{overall['applicable']}.",
        f"- McNemar exato bilateral agregado: "
        f"p={overall['mcnemar_exact_two_sided_p']:.4f}.",
        f"- Execuções Playwright de resiliência: "
        f"{resilience['execution_evidence']['resilience_total_playwright_executions']}.",
        "",
        "Os resultados de resiliência devem ser apresentados prioritariamente por "
        "modelo, porque o agregado combina amostras pequenas e heterogêneas.",
        "",
        "## Arquivos",
        "",
        "- `metrics_summary.json`: todas as métricas consolidadas.",
        "- `generation_execution_semantic.csv`: uma linha por condição e rodada.",
        "- `paired_semantic_comparison.csv`: comparação pareada dos escores.",
        "- `artifact_index.csv`: localização, estado e hash dos artefatos primários.",
        "",
    ]
    (OUT / "metrics_summary.md").write_text(
        "\n".join(markdown), encoding="utf-8"
    )

    snapshot_files = [
        OUT / "metrics_summary.json",
        OUT / "metrics_summary.md",
        OUT / "generation_execution_semantic.csv",
        OUT / "paired_semantic_comparison.csv",
        OUT / "artifact_index.csv",
    ]
    snapshot_manifest = {
        "snapshot_id": summary["snapshot_id"],
        "files": [
            {
                "path": path.name,
                "sha256": sha256(path),
                "bytes": path.stat().st_size,
            }
            for path in snapshot_files
        ],
    }
    canonical = json.dumps(snapshot_manifest, sort_keys=True, ensure_ascii=False)
    snapshot_manifest["snapshot_sha256"] = hashlib.sha256(
        canonical.encode("utf-8")
    ).hexdigest()
    (OUT / "snapshot_manifest.json").write_text(
        json.dumps(snapshot_manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(OUT)


if __name__ == "__main__":
    main()
