#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EVALUATOR = ROOT / "python_app" / "avaliacao_prompts"
sys.path.insert(0, str(EVALUATOR))

from avaliacao_prompts.resilience.execution import prepare_execution, scenario_id_for_test  # noqa: E402
from avaliacao_prompts.resilience.plan import build_plan, verify_plan, write_plan  # noqa: E402


GPT_ROUND_SCENARIOS = (
    "suite_adicionar_carrinho",
    "suite_adicionar_wishlist",
    "suite_busca_blue_jeans",
    "suite_checkout_blue_jeans",
    "suite_configurar_desktop",
    "suite_detalhes_fiction",
    "suite_limpar_carrinho",
    "suite_limpar_wishlist",
    "suite_login_invalido",
    "suite_login_valido",
    "suite_logout",
    "suite_registro_usuario",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Prepara e congela, sem executar o site, a campanha de mutação."
    )
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument(
        "--new-input-root",
        type=Path,
        default=Path(
            "/home/martinsspn/openai_playwright_batch/inputs/"
            "demowebshop20-20260727-ready"
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output = args.output_dir.resolve()
    if output.exists():
        raise FileExistsError(
            f"A campanha já existe e não será sobrescrita: {output}"
        )

    paths = source_paths(args.new_input_root.resolve())
    _require_sources(paths)
    output.mkdir(parents=True)
    inventory: list[dict[str, str]] = []

    reviews = freeze_reviews(output, paths, inventory)
    runtime = freeze_runtime(output, paths, inventory)
    input_sets = freeze_input_rounds(output, paths, inventory)
    plans = build_round_plans(output, input_sets)
    cohorts = freeze_cohort_sources(output, paths, inventory)
    validate_semantic_eligibility(cohorts, reviews)
    prepared = prepare_cohorts(
        output=output,
        cohorts=cohorts,
        plans=plans,
        reviews=reviews,
        runtime=runtime,
        inventory=inventory,
    )
    manifest = write_campaign_manifest(
        output=output,
        inputs=input_sets,
        plans=plans,
        prepared=prepared,
        runtime=runtime,
        source_inventory=inventory,
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


def source_paths(new_input_root: Path) -> dict[str, Path]:
    tests = ROOT / "python_app" / "teste_prompt_e2e_semantico"
    evaluation = ROOT / "python_app" / "avaliacao_prompts"
    return {
        "gpt_specs": tests / "specs",
        "gpt_prompts": tests / "generated_prompts",
        "gemini_specs": new_input_root / "baseline",
        "gemini_prompts": new_input_root / "structured_context",
        "gpt_baseline": tests
        / "generated_tests"
        / "archive_before_qwen25coder_gpu_20260724_01"
        / "baseline",
        "gpt_structured": tests
        / "generated_tests"
        / "archive_before_qwen25coder_gpu_20260724_01"
        / "structured_context",
        "gemini_baseline": tests
        / "generated_tests"
        / "baseline_gemini36flash_demowebshop20_20260727_01",
        "gemini_structured": tests
        / "generated_tests"
        / "structured_context_gemini36flash_demowebshop20_20260727_01",
        "gpt_repaired_cart": evaluation
        / "repair_runs"
        / "qwen25coder_repair_20260728_01"
        / "gpt-5-6-sol"
        / "gpt_original_12"
        / "baseline"
        / "suite_adicionar_carrinho"
        / "suite_adicionar_carrinho.spec.ts",
        "gemini_repaired_downloads": evaluation
        / "repair_runs"
        / "qwen25coder_repair_20260728_01"
        / "gemini-3-6-flash"
        / "gemini_new_20"
        / "baseline"
        / "fluxo_computadores_desktops"
        / "fluxo_computadores_desktops.spec.ts",
        "gemini_repaired_about": evaluation
        / "repair_runs"
        / "qwen25coder_repair_20260728_01"
        / "gemini-3-6-flash"
        / "gemini_new_20"
        / "structured_context"
        / "suite_navegar_sobre_nos"
        / "suite_navegar_sobre_nos.spec.ts",
        "original_review": evaluation
        / "resultados_adequacao_semantica_20260728"
        / "semantic_review.csv",
        "repair_review": evaluation
        / "repair_results"
        / "qwen25coder_repair_20260728_01"
        / "semantic_review_passed.csv",
        "fixture": evaluation / "playwright_resilience" / "fixture.ts",
        "control": evaluation / "playwright_resilience" / "control.spec.ts",
        "playwright_config": evaluation / "playwright.config.ts",
        "evaluator_package": evaluation / "avaliacao_prompts",
        "package_json": ROOT / "package.json",
        "package_lock": ROOT / "package-lock.json",
        "preparer": ROOT / "tools" / "prepare_resilience_campaign.py",
        "verifier": ROOT / "tools" / "verify_resilience_campaign.py",
        "allowlists": evaluation
        / "resilience_artifacts"
        / "eligibility_candidates",
    }


def _require_sources(paths: dict[str, Path]) -> None:
    missing = [f"{name}: {path}" for name, path in paths.items() if not path.exists()]
    if missing:
        raise FileNotFoundError("Fontes ausentes:\n" + "\n".join(missing))


def freeze_reviews(
    output: Path,
    paths: dict[str, Path],
    inventory: list[dict[str, str]],
) -> dict[str, Path]:
    review_dir = output / "reviews"
    original = copy_source(
        paths["original_review"],
        review_dir / "original_semantic_review.csv",
        "review",
        inventory,
    )
    repaired = copy_source(
        paths["repair_review"],
        review_dir / "repair_semantic_review.csv",
        "review",
        inventory,
    )
    bundles: dict[str, Path] = {}
    for track, sources in {
        "P": [original],
        "R": [original, repaired],
    }.items():
        payload = {
            "schema_version": 1,
            "track_id": track,
            "sources": [
                {
                    "file": path.name,
                    "sha256": sha256_file(path),
                }
                for path in sources
            ],
        }
        bundle = review_dir / f"track_{track}_review_bundle.json"
        write_json(bundle, payload)
        bundles[track] = bundle
    return {
        "original": original,
        "repaired": repaired,
        "P": bundles["P"],
        "R": bundles["R"],
    }


def freeze_runtime(
    output: Path,
    paths: dict[str, Path],
    inventory: list[dict[str, str]],
) -> dict[str, Path]:
    runtime = output / "runtime"
    frozen = {
        "fixture": copy_source(
            paths["fixture"],
            runtime / "playwright" / "fixture.ts",
            "runtime",
            inventory,
        ),
        "control": copy_source(
            paths["control"],
            runtime / "playwright" / "control.spec.ts",
            "runtime",
            inventory,
        ),
        "playwright_config": copy_source(
            paths["playwright_config"],
            runtime / "playwright" / "playwright.config.ts",
            "runtime",
            inventory,
        ),
        "package_json": copy_source(
            paths["package_json"],
            runtime / "node" / "package.json",
            "runtime",
            inventory,
        ),
        "package_lock": copy_source(
            paths["package_lock"],
            runtime / "node" / "package-lock.json",
            "runtime",
            inventory,
        ),
        "preparer": copy_source(
            paths["preparer"],
            runtime / "tools" / "prepare_resilience_campaign.py",
            "runtime",
            inventory,
        ),
        "verifier": copy_source(
            paths["verifier"],
            runtime / "tools" / "verify_resilience_campaign.py",
            "runtime",
            inventory,
        ),
    }
    package_target = runtime / "python" / "avaliacao_prompts"
    for source in sorted(paths["evaluator_package"].rglob("*.py")):
        relative = source.relative_to(paths["evaluator_package"])
        copy_source(
            source,
            package_target / relative,
            "runtime_python",
            inventory,
        )
    frozen["python_path"] = runtime / "python"
    return frozen


def freeze_input_rounds(
    output: Path,
    paths: dict[str, Path],
    inventory: list[dict[str, str]],
) -> dict[str, dict[str, Path]]:
    rounds: dict[str, dict[str, Path]] = {}
    gpt_root = output / "inputs" / "gpt_original_12"
    rounds["gpt_original_12"] = copy_input_round(
        scenarios=GPT_ROUND_SCENARIOS,
        source_specs=paths["gpt_specs"],
        source_prompts=paths["gpt_prompts"],
        prompt_suffix=".structured_context.prompt.md",
        destination=gpt_root,
        inventory=inventory,
    )

    gemini_scenarios = tuple(
        sorted(path.stem for path in paths["gemini_specs"].glob("*.txt"))
    )
    if len(gemini_scenarios) != 20:
        raise ValueError(
            f"A rodada ampliada deveria conter 20 especificações, não {len(gemini_scenarios)}."
        )
    gemini_root = output / "inputs" / "gemini_new_20"
    rounds["gemini_new_20"] = copy_input_round(
        scenarios=gemini_scenarios,
        source_specs=paths["gemini_specs"],
        source_prompts=paths["gemini_prompts"],
        prompt_suffix=".prompt.md",
        destination=gemini_root,
        inventory=inventory,
    )
    return rounds


def copy_input_round(
    *,
    scenarios: tuple[str, ...],
    source_specs: Path,
    source_prompts: Path,
    prompt_suffix: str,
    destination: Path,
    inventory: list[dict[str, str]],
) -> dict[str, Path]:
    specs = destination / "specs"
    prompts = destination / "prompts"
    for scenario in scenarios:
        copy_source(
            source_specs / f"{scenario}.txt",
            specs / f"{scenario}.txt",
            "specification",
            inventory,
        )
        copy_source(
            source_prompts / f"{scenario}{prompt_suffix}",
            prompts / f"{scenario}.structured_context.prompt.md",
            "structured_prompt",
            inventory,
        )
    return {"root": destination, "specs": specs, "prompts": prompts}


def build_round_plans(
    output: Path,
    input_sets: dict[str, dict[str, Path]],
) -> dict[str, Path]:
    plans: dict[str, Path] = {}
    for round_id, paths in input_sets.items():
        payload = build_plan(paths["specs"], paths["prompts"])
        plan_path = write_plan(
            output / "plans" / f"{round_id}.mutation_plan.json",
            payload,
        )
        if not verify_plan(payload):
            raise ValueError(f"Plano inválido após geração: {round_id}")
        plans[round_id] = plan_path
    return plans


def freeze_cohort_sources(
    output: Path,
    paths: dict[str, Path],
    inventory: list[dict[str, str]],
) -> dict[tuple[str, str], dict[str, Any]]:
    gpt_baseline = index_tests(paths["gpt_baseline"], "baseline")
    gpt_structured = index_tests(paths["gpt_structured"], "structured_context")
    gemini_baseline = index_tests(paths["gemini_baseline"], "baseline")
    gemini_structured = index_tests(paths["gemini_structured"], "structured_context")

    definitions: dict[tuple[str, str], dict[str, Any]] = {
        ("P", "gpt-5.6-sol"): {
            "round": "gpt_original_12",
            "baseline": gpt_baseline,
            "structured_context": gpt_structured,
        },
        ("P", "gemini-3.6-flash"): {
            "round": "gemini_new_20",
            "baseline": gemini_baseline,
            "structured_context": gemini_structured,
        },
        ("R", "gpt-5.6-sol"): {
            "round": "gpt_original_12",
            "baseline": {
                "suite_adicionar_carrinho": paths["gpt_repaired_cart"],
            },
            "structured_context": {
                "suite_adicionar_carrinho": gpt_structured[
                    "suite_adicionar_carrinho"
                ],
            },
        },
        ("R", "gemini-3.6-flash"): {
            "round": "gemini_new_20",
            "baseline": {
                "fluxo_computadores_desktops": paths[
                    "gemini_repaired_downloads"
                ],
                "suite_navegar_sobre_nos": gemini_baseline[
                    "suite_navegar_sobre_nos"
                ],
            },
            "structured_context": {
                "fluxo_computadores_desktops": gemini_structured[
                    "fluxo_computadores_desktops"
                ],
                "suite_navegar_sobre_nos": paths["gemini_repaired_about"],
            },
        },
    }

    frozen: dict[tuple[str, str], dict[str, Any]] = {}
    for (track, model), definition in definitions.items():
        allowlist_source = paths["allowlists"] / f"track_{track}_{model}.json"
        allowlist = json.loads(allowlist_source.read_text(encoding="utf-8"))
        scenarios = tuple(allowlist["scenario_ids"])
        root = output / "cohort_sources" / f"track_{track}" / model
        for condition in ("baseline", "structured_context"):
            sources = definition[condition]
            for scenario in scenarios:
                if scenario not in sources:
                    raise ValueError(
                        f"Fonte ausente para {track}/{model}/{condition}/{scenario}"
                    )
                copy_source(
                    sources[scenario],
                    root / condition / f"{scenario}.spec.ts",
                    f"test_{track}_{model}_{condition}",
                    inventory,
                )
        frozen[(track, model)] = {
            "round": definition["round"],
            "root": root,
            "allowlist_source": allowlist_source,
            "scenario_ids": scenarios,
        }
    return frozen


def validate_semantic_eligibility(
    cohorts: dict[tuple[str, str], dict[str, Any]],
    reviews: dict[str, Path],
) -> None:
    original = csv_index(
        reviews["original"],
        ("model", "round", "scenario", "condition"),
    )
    repaired = csv_index(
        reviews["repaired"],
        ("model_origin", "round", "scenario", "condition"),
    )
    repaired_conditions = {
        ("R", "gpt-5.6-sol", "suite_adicionar_carrinho", "baseline"),
        ("R", "gemini-3.6-flash", "fluxo_computadores_desktops", "baseline"),
        ("R", "gemini-3.6-flash", "suite_navegar_sobre_nos", "structured_context"),
    }
    for (track, model), cohort in cohorts.items():
        round_id = cohort["round"]
        for scenario in cohort["scenario_ids"]:
            for condition in ("baseline", "structured_context"):
                key = (track, model, scenario, condition)
                if key in repaired_conditions:
                    row = repaired[(model, round_id, scenario, condition)]
                    if (
                        row.get("semantic_total_6") != "6"
                        or row.get("semantic_classification") != "adequate"
                    ):
                        raise ValueError(f"Reparo sem adequação 6/6: {key}")
                else:
                    row = original[(model, round_id, scenario, condition)]
                    if (
                        row.get("execution_status") != "passed"
                        or row.get("semantic_total_6") != "6"
                    ):
                        raise ValueError(f"Original sem aprovação e 6/6: {key}")


def prepare_cohorts(
    *,
    output: Path,
    cohorts: dict[tuple[str, str], dict[str, Any]],
    plans: dict[str, Path],
    reviews: dict[str, Path],
    runtime: dict[str, Path],
    inventory: list[dict[str, str]],
) -> dict[tuple[str, str], Path]:
    prepared: dict[tuple[str, str], Path] = {}
    for (track, model), cohort in cohorts.items():
        allowlist = copy_source(
            cohort["allowlist_source"],
            output / "allowlists" / f"track_{track}_{model}.json",
            "allowlist",
            inventory,
        )
        manifest = prepare_execution(
            baseline_dir=cohort["root"] / "baseline",
            structured_dir=cohort["root"] / "structured_context",
            fixture=runtime["fixture"],
            frozen_plan=plans[cohort["round"]],
            output_dir=output / "prepared" / f"track_{track}" / model,
            allowlist=allowlist,
            semantic_review=reviews[track],
            track_id=track,
            model_id=model,
        )
        prepared[(track, model)] = manifest
    return prepared


def write_campaign_manifest(
    *,
    output: Path,
    inputs: dict[str, dict[str, Path]],
    plans: dict[str, Path],
    prepared: dict[tuple[str, str], Path],
    runtime: dict[str, Path],
    source_inventory: list[dict[str, str]],
) -> dict[str, Any]:
    plan_summaries = {}
    for round_id, path in plans.items():
        payload = json.loads(path.read_text(encoding="utf-8"))
        plan_summaries[round_id] = {
            "file": str(path.relative_to(output)),
            "sha256": sha256_file(path),
            "plan_sha256": payload["plan_sha256"],
            "catalog_size": payload["catalog_size"],
            "mutation_count": payload["mutation_count"],
        }
    payload: dict[str, Any] = {
        "schema_version": 1,
        "status": "prepared_not_executed",
        "live_site_requests_performed": False,
        "rounds": {
            round_id: {
                "specification_count": len(list(paths["specs"].glob("*.txt"))),
                "prompt_count": len(list(paths["prompts"].glob("*.md"))),
            }
            for round_id, paths in inputs.items()
        },
        "plans": plan_summaries,
        "runtime": {
            name: {
                "file": str(path.relative_to(output)),
                "sha256": sha256_file(path),
            }
            for name, path in runtime.items()
            if path.is_file()
        },
        "cohorts": [
            {
                "track_id": track,
                "model_id": model,
                "execution_manifest": str(path.relative_to(output)),
                "execution_manifest_sha256": sha256_file(path),
            }
            for (track, model), path in sorted(prepared.items())
        ],
        "source_inventory": sorted(
            source_inventory,
            key=lambda item: (item["role"], item["destination"]),
        ),
    }
    payload["campaign_files_aggregate_sha256"] = aggregate_campaign_files(output)
    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    payload["campaign_manifest_sha256"] = hashlib.sha256(
        canonical.encode("utf-8")
    ).hexdigest()
    write_json(output / "campaign_manifest.json", payload)
    return payload


def index_tests(directory: Path, approach: str) -> dict[str, Path]:
    indexed: dict[str, Path] = {}
    for path in sorted(directory.glob("*.spec.ts")):
        scenario = scenario_id_for_test(path, approach)
        if scenario in indexed:
            raise ValueError(f"Teste duplicado para {scenario}: {directory}")
        indexed[scenario] = path
    return indexed


def csv_index(path: Path, fields: tuple[str, ...]) -> dict[tuple[str, ...], dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    result: dict[tuple[str, ...], dict[str, str]] = {}
    for row in rows:
        key = tuple(row[field] for field in fields)
        if key in result:
            raise ValueError(f"Chave duplicada em {path}: {key}")
        result[key] = row
    return result


def copy_source(
    source: Path,
    destination: Path,
    role: str,
    inventory: list[dict[str, str]],
) -> Path:
    if not source.is_file():
        raise FileNotFoundError(source)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        raise FileExistsError(destination)
    shutil.copy2(source, destination)
    source_hash = sha256_file(source)
    destination_hash = sha256_file(destination)
    if source_hash != destination_hash:
        raise ValueError(f"Cópia divergente: {source} -> {destination}")
    inventory.append(
        {
            "role": role,
            "source": str(source.resolve()),
            "destination": str(destination),
            "sha256": source_hash,
        }
    )
    return destination


def aggregate_campaign_files(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        relative = path.relative_to(root).as_posix()
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(sha256_file(path).encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise FileExistsError(path)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    raise SystemExit(main())
