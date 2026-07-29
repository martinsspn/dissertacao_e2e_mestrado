from __future__ import annotations

import base64
import hashlib
import json
import math
import os
import random
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator

from avaliacao_prompts.infrastructure.playwright_results import read_playwright_json
from avaliacao_prompts.resilience.plan import verify_plan


@dataclass(frozen=True)
class RunOutcome:
    status: str
    mutation_events: tuple[dict[str, Any], ...] = ()
    control_observation: dict[str, Any] | None = None
    returncode: int | None = None
    duration_seconds: float | None = None
    error_type: str = ""
    error_message_excerpt: str = ""
    artifacts_dir: str = ""


def execute_eligibility(
    execution_manifest_path: Path,
    playwright_config: Path,
    node_project_dir: Path,
    output_dir: Path,
    repetitions: int,
) -> Path:
    if output_dir.exists():
        raise FileExistsError(
            f"O diretório de elegibilidade já existe e não será sobrescrito: {output_dir}"
        )
    if repetitions < 1:
        raise ValueError("repetitions deve ser >= 1")
    manifest = json.loads(execution_manifest_path.read_text(encoding="utf-8"))
    plan_path = Path(manifest["mutation_plan"])
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    if not verify_plan(plan) or plan["plan_sha256"] != manifest["mutation_plan_sha256"]:
        raise ValueError("Plano ou vínculo entre plano e execução foi alterado.")

    output_dir.mkdir(parents=True)
    runtime = _runtime_metadata(node_project_dir)
    statuses: dict[str, dict[str, list[str]]] = {}
    details: dict[str, dict[str, list[dict[str, Any]]]] = {}
    for pair in sorted(manifest["pairs"], key=lambda item: item["scenario_id"]):
        scenario = pair["scenario_id"]
        statuses[scenario] = {"A": [], "B": []}
        details[scenario] = {"A": [], "B": []}
        order = _condition_order(plan["plan_sha256"], f"original:{scenario}")
        for repetition in range(1, repetitions + 1):
            for condition in order:
                test_file = _derived_file(
                    execution_manifest_path.parent,
                    condition,
                    scenario,
                )
                outcome = _run_one(
                    test_file=test_file,
                    test_dir=test_file.parent,
                    config=playwright_config,
                    node_project=node_project_dir,
                    plan=plan_path,
                    mutation_id="",
                    control_only=False,
                    json_path=output_dir
                    / "runs"
                    / f"{scenario}-{condition}-r{repetition}.json",
                )
                statuses[scenario][condition].append(outcome.status)
                details[scenario][condition].append(
                    {
                        "repetition": repetition,
                        "order": order,
                        "outcome": _outcome_dict(outcome),
                    }
                )

    eligible = sorted(
        scenario
        for scenario, conditions in statuses.items()
        if all(value == "passed" for value in conditions["A"] + conditions["B"])
    )
    payload: dict[str, Any] = {
        "schema_version": 1,
        "execution_manifest": str(execution_manifest_path.resolve()),
        "execution_manifest_sha256": manifest["execution_manifest_sha256"],
        "mutation_plan_sha256": plan["plan_sha256"],
        "track_id": manifest.get("track_id", ""),
        "model_id": manifest.get("model_id", ""),
        "repetitions": repetitions,
        "runtime": runtime,
        "configured_environment_names": _configured_environment_names(),
        "statuses": statuses,
        "details": details,
        "eligible_scenarios": eligible,
        "ineligible_scenarios": sorted(set(statuses) - set(eligible)),
    }
    payload["eligibility_results_sha256"] = _signed_payload_hash(
        payload,
        "eligibility_results_sha256",
    )
    output = output_dir / "eligibility_results.json"
    output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return output.resolve()


def execute_experiment(
    execution_manifest_path: Path,
    eligibility_results_path: Path,
    playwright_config: Path,
    node_project_dir: Path,
    control_test: Path,
    output_dir: Path,
    repetitions: int,
    mutation_ids: tuple[str, ...] = (),
    mutations_per_scenario: int | None = None,
    scenario_ids: tuple[str, ...] = (),
) -> tuple[Path, Path]:
    if output_dir.exists():
        raise FileExistsError(
            f"O diretório de resultados já existe e não será sobrescrito: {output_dir}"
        )
    manifest = json.loads(execution_manifest_path.read_text(encoding="utf-8"))
    eligibility_result = json.loads(
        eligibility_results_path.read_text(encoding="utf-8")
    )
    if not _verify_signed_payload(
        eligibility_result,
        "eligibility_results_sha256",
    ):
        raise ValueError("O resultado de elegibilidade foi alterado.")
    if (
        eligibility_result.get("execution_manifest_sha256")
        != manifest.get("execution_manifest_sha256")
    ):
        raise ValueError("A elegibilidade não pertence a este manifesto de execução.")
    plan_path = Path(manifest["mutation_plan"])
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    if not verify_plan(plan) or plan["plan_sha256"] != manifest["mutation_plan_sha256"]:
        raise ValueError("Plano ou vínculo entre plano e execução foi alterado.")
    if eligibility_result.get("mutation_plan_sha256") != plan["plan_sha256"]:
        raise ValueError("A elegibilidade não pertence a este plano de mutações.")
    if repetitions < 1:
        raise ValueError("repetitions deve ser >= 1")
    if mutations_per_scenario not in (None, 1, 2):
        raise ValueError("mutations_per_scenario deve ser 1, 2 ou None")
    if mutation_ids and mutations_per_scenario is not None:
        raise ValueError("--mutation e --mutations-per-scenario nao podem ser combinados")
    output_dir.mkdir(parents=True)
    runtime = _runtime_metadata(node_project_dir)

    all_pairs = {pair["scenario_id"]: pair for pair in manifest["pairs"]}
    requested_scenarios = set(scenario_ids)
    unknown_scenarios = requested_scenarios - set(all_pairs)
    if unknown_scenarios:
        raise ValueError(f"Cenários inexistentes: {', '.join(sorted(unknown_scenarios))}")
    pairs = {
        scenario: pair
        for scenario, pair in all_pairs.items()
        if not requested_scenarios or scenario in requested_scenarios
    }
    eligible = set(eligibility_result["eligible_scenarios"]) & set(pairs)

    requested = set(mutation_ids)
    eligible_mutations = [
        mutation
        for mutation in plan["mutations"]
        if mutation["target"]["scenario_id"] in eligible
        and (not requested or mutation["mutation_id"] in requested)
    ]
    unknown = requested - {mutation["mutation_id"] for mutation in plan["mutations"]}
    if unknown:
        raise ValueError(f"Mutações inexistentes: {', '.join(sorted(unknown))}")
    mutations = _select_mutations(
        eligible_mutations,
        plan_hash=plan["plan_sha256"],
        per_scenario=mutations_per_scenario,
    )

    mutation_results: list[dict[str, Any]] = []
    for mutation in mutations:
        mutation_id = mutation["mutation_id"]
        scenario = mutation["target"]["scenario_id"]
        control_runs: list[dict[str, Any]] = []
        control_valid = True
        invalid_reasons: set[str] = set()
        for repetition in range(1, repetitions + 1):
            original_control = _run_one(
                test_file=control_test,
                test_dir=control_test.parent,
                config=playwright_config,
                node_project=node_project_dir,
                plan=plan_path,
                mutation_id=mutation_id,
                control_only=True,
                json_path=output_dir / "controls" / f"{mutation_id}-original-r{repetition}.json",
            )
            mutated_control = _run_one(
                test_file=control_test,
                test_dir=control_test.parent,
                config=playwright_config,
                node_project=node_project_dir,
                plan=plan_path,
                mutation_id=mutation_id,
                control_only=False,
                json_path=output_dir / "controls" / f"{mutation_id}-mutated-r{repetition}.json",
            )
            reasons = _control_invalid_reasons(
                original_control,
                mutated_control,
                expected_target_id=mutation["target"]["target_id"],
            )
            if reasons:
                control_valid = False
                invalid_reasons.update(reasons)
            control_runs.append(
                {
                    "repetition": repetition,
                    "original": _outcome_dict(original_control),
                    "mutated": _outcome_dict(mutated_control),
                    "invalid_reasons": sorted(reasons),
                }
            )

        exposure_runs: list[dict[str, Any]] = []
        paired_applicable = control_valid
        if control_valid:
            exposure_order = _condition_order(plan["plan_sha256"], f"exposure:{mutation_id}")
            for repetition in range(1, repetitions + 1):
                exposure: dict[str, dict[str, Any]] = {}
                for condition in exposure_order:
                    test_file = _derived_file(execution_manifest_path.parent, condition, scenario)
                    outcome = _run_one(
                        test_file=test_file,
                        test_dir=test_file.parent,
                        config=playwright_config,
                        node_project=node_project_dir,
                        plan=plan_path,
                        mutation_id=mutation_id,
                        control_only=True,
                        json_path=output_dir / "exposure" / f"{mutation_id}-{condition}-r{repetition}.json",
                    )
                    interacted = _has_target_event(
                        outcome,
                        "marked",
                        mutation["target"]["target_id"],
                    ) and _has_target_event(
                        outcome,
                        "interacted",
                        mutation["target"]["target_id"],
                    )
                    exposure[condition] = {
                        "status": outcome.status,
                        "interacted": interacted,
                        "outcome": _outcome_dict(outcome),
                    }
                    if outcome.status != "passed" or not interacted:
                        paired_applicable = False
                exposure_runs.append({"repetition": repetition, "order": exposure_order, "conditions": exposure})

        condition_runs: list[dict[str, Any]] = []
        if control_valid and paired_applicable:
            order = _condition_order(plan["plan_sha256"], mutation_id)
            for repetition in range(1, repetitions + 1):
                outcomes: dict[str, str] = {}
                details: dict[str, dict[str, Any]] = {}
                for condition in order:
                    test_file = _derived_file(execution_manifest_path.parent, condition, scenario)
                    outcome = _run_one(
                        test_file=test_file,
                        test_dir=test_file.parent,
                        config=playwright_config,
                        node_project=node_project_dir,
                        plan=plan_path,
                        mutation_id=mutation_id,
                        control_only=False,
                        json_path=output_dir / "mutations" / f"{mutation_id}-{condition}-r{repetition}.json",
                    )
                    outcomes[condition] = _classify_mutated_outcome(
                        outcome,
                        expected_target_id=mutation["target"]["target_id"],
                    )
                    details[condition] = _outcome_dict(outcome)
                condition_runs.append(
                    {
                        "repetition": repetition,
                        "order": order,
                        "outcomes": outcomes,
                        "details": details,
                    }
                )
        mutation_results.append(
            {
                "mutation_id": mutation_id,
                "scenario_id": scenario,
                "stratum": mutation["stratum"],
                "operator": mutation["operator"],
                "control_valid": control_valid,
                "paired_applicable": paired_applicable,
                "invalid_reasons": sorted(invalid_reasons),
                "control_runs": control_runs,
                "exposure_runs": exposure_runs,
                "condition_runs": condition_runs,
            }
        )

    payload = {
        "schema_version": 2,
        "execution_manifest_sha256": manifest["execution_manifest_sha256"],
        "mutation_plan_sha256": plan["plan_sha256"],
        "track_id": manifest.get("track_id", ""),
        "model_id": manifest.get("model_id", ""),
        "allowlist_sha256": manifest.get("allowlist_sha256", ""),
        "semantic_review_sha256": manifest.get("semantic_review_sha256", ""),
        "eligibility_results": str(eligibility_results_path.resolve()),
        "eligibility_results_sha256": eligibility_result[
            "eligibility_results_sha256"
        ],
        "runtime": runtime,
        "configured_environment_names": _configured_environment_names(),
        "repetitions": repetitions,
        "selection": {
            "mode": "explicit_ids" if requested else "deterministic_neutral_sample" if mutations_per_scenario else "full_plan",
            "mutations_per_scenario": mutations_per_scenario,
            "included_strata": ["E1", "E2"] if mutations_per_scenario else ["E1", "E2", "E3", "E4"],
            "rule": (
                "one_E1_then_one_E2_when_available_then_hash_ranked_neutral_fill"
                if mutations_per_scenario
                else None
            ),
            "selected_mutation_ids": [mutation["mutation_id"] for mutation in mutations],
            "requested_scenarios": sorted(requested_scenarios),
        },
        "eligible_scenarios": sorted(eligible),
        "mutation_results": mutation_results,
    }
    json_output = output_dir / "resilience_results.json"
    json_output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    markdown_output = output_dir / "resilience_results.md"
    markdown_output.write_text(_markdown_report(payload, manifest["condition_key"]), encoding="utf-8")
    return json_output.resolve(), markdown_output.resolve()


def _select_mutations(
    mutations: list[dict[str, Any]],
    plan_hash: str,
    per_scenario: int | None,
) -> list[dict[str, Any]]:
    """Select a small neutral sample without consulting condition outcomes.

    E1 is always represented. With two slots, E2 is represented when the
    scenario has an applicable E2 operator; remaining slots are filled from
    E1/E2. Ranking is a stable hash of the frozen plan, scenario and mutation.
    """
    if per_scenario is None:
        return mutations
    grouped: dict[str, list[dict[str, Any]]] = {}
    for mutation in mutations:
        if mutation["stratum"] in {"E1", "E2"}:
            grouped.setdefault(mutation["target"]["scenario_id"], []).append(mutation)

    selected: list[dict[str, Any]] = []
    for scenario in sorted(grouped):
        candidates = grouped[scenario]

        def rank(item: dict[str, Any]) -> str:
            material = f"{plan_hash}:reduced-neutral-v1:{scenario}:{item['mutation_id']}"
            return hashlib.sha256(material.encode()).hexdigest()

        e1 = sorted((item for item in candidates if item["stratum"] == "E1"), key=rank)
        e2 = sorted((item for item in candidates if item["stratum"] == "E2"), key=rank)
        chosen: list[dict[str, Any]] = []
        if e1:
            chosen.append(e1[0])
        if per_scenario == 2 and e2:
            chosen.append(e2[0])
        remaining = sorted(
            (item for item in candidates if item not in chosen),
            key=rank,
        )
        chosen.extend(remaining[: per_scenario - len(chosen)])
        selected.extend(chosen)
    return selected


def _run_one(
    test_file: Path,
    test_dir: Path,
    config: Path,
    node_project: Path,
    plan: Path,
    mutation_id: str,
    control_only: bool,
    json_path: Path,
) -> RunOutcome:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    artifacts_dir = json_path.with_suffix(".artifacts")
    env = os.environ.copy()
    env.update(
        {
            "RESILIENCE_TEST_DIR": str(test_dir.resolve()),
            "RESILIENCE_PLAN": str(plan.resolve()),
            "RESILIENCE_MUTATION_ID": mutation_id,
            "RESILIENCE_CONTROL_ONLY": "1" if control_only else "0",
            "RESILIENCE_CAPTURE_EVIDENCE": "1",
        }
    )
    command = [
        "npx",
        "playwright",
        "test",
        test_file.name,
        f"--config={config.resolve()}",
        "--reporter=json",
        "--workers=1",
        "--retries=0",
        "--trace=on",
        f"--output={artifacts_dir.resolve()}",
    ]
    started = time.monotonic()
    completed = subprocess.run(
        command,
        cwd=node_project.resolve(),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    duration = round(time.monotonic() - started, 3)
    json_path.write_text(completed.stdout, encoding="utf-8")
    json_path.with_suffix(".stderr.txt").write_text(completed.stderr, encoding="utf-8")
    if not completed.stdout.lstrip().startswith("{"):
        return RunOutcome(
            "environment_error",
            returncode=completed.returncode,
            duration_seconds=duration,
            error_type="environment_error",
            error_message_excerpt=_excerpt(completed.stderr or completed.stdout),
            artifacts_dir=str(artifacts_dir.resolve()),
        )
    parsed_results = read_playwright_json(json_path)
    result = next(iter(parsed_results.values()), None)
    payload = json.loads(completed.stdout)
    attachments = _attachments(payload)
    return RunOutcome(
        status=result.status if result else "environment_error",
        mutation_events=tuple(attachments.get("resilience-mutation-events", [])),
        control_observation=attachments.get("resilience-control-observation"),
        returncode=completed.returncode,
        duration_seconds=duration,
        error_type=result.error_type if result else "environment_error",
        error_message_excerpt=result.error_message_excerpt if result else "",
        artifacts_dir=str(artifacts_dir.resolve()),
    )


def _attachments(payload: dict[str, Any]) -> dict[str, Any]:
    values: dict[str, Any] = {}
    for spec in _iter_specs(payload.get("suites", [])):
        for test in spec.get("tests", []):
            for result in test.get("results", []):
                for attachment in result.get("attachments", []):
                    body = attachment.get("body")
                    if body and attachment.get("contentType") == "application/json":
                        values[attachment["name"]] = json.loads(base64.b64decode(body).decode("utf-8"))
    return values


def _iter_specs(suites: list[dict[str, Any]]) -> Iterator[dict[str, Any]]:
    for suite in suites:
        yield from suite.get("specs", [])
        yield from _iter_specs(suite.get("suites", []))


def _control_invalid_reasons(
    original: RunOutcome,
    mutated: RunOutcome,
    *,
    expected_target_id: str | None = None,
) -> set[str]:
    reasons: set[str] = set()
    if original.status != "passed":
        reasons.add("original_control_failed")
    if mutated.status != "passed":
        reasons.add("mutated_control_failed")
    if not _has_target_event(original, "marked", expected_target_id):
        reasons.add("original_target_not_marked")
    if not _has_target_event(original, "interacted", expected_target_id):
        reasons.add("original_target_not_interacted")
    if not _has_target_event(mutated, "applied", expected_target_id):
        reasons.add("mutation_not_applied")
    if not _has_target_event(mutated, "interacted", expected_target_id):
        reasons.add("mutated_target_not_interacted")
    if original.control_observation != mutated.control_observation:
        reasons.add("functional_observation_changed")
    return reasons


def _has_target_event(
    outcome: RunOutcome,
    status: str,
    target_id: str | None,
) -> bool:
    return any(
        event.get("status") == status
        and (target_id is None or event.get("targetId") == target_id)
        for event in outcome.mutation_events
    )


def _classify_mutated_outcome(
    outcome: RunOutcome,
    *,
    expected_target_id: str,
) -> str:
    events = outcome.mutation_events
    if any(event.get("status") in {"ambiguous", "error", "missing"} for event in events):
        return "instrumentation_failure"
    if not _has_target_event(outcome, "applied", expected_target_id):
        return "instrumentation_failure"
    interactions = [event for event in events if event.get("status") == "interacted"]
    if interactions and not any(
        event.get("targetId") == expected_target_id for event in interactions
    ):
        return "wrong_target"
    if outcome.status == "passed" and not interactions:
        return "false_positive_no_interaction"
    if outcome.status == "passed":
        return "passed_interacted"
    if outcome.status == "environment_error":
        return "environment_failure"
    if outcome.error_type == "selector_ambiguity":
        return "strict_mode_ambiguity"
    if outcome.error_type == "locator_timeout":
        return "locator_not_found"
    if outcome.error_type == "assertion_failure":
        return "assertion_failure"
    if outcome.status == "timed_out":
        return "unrelated_timeout"
    if outcome.status in {"syntax_error", "runtime_error"}:
        return "runtime_code_error"
    return "runtime_code_error"


def _condition_order(plan_hash: str, unit: str) -> list[str]:
    seed = int(hashlib.sha256(f"{plan_hash}:{unit}".encode()).hexdigest()[:16], 16)
    result = ["A", "B"]
    random.Random(seed).shuffle(result)
    return result


def _derived_file(root: Path, condition: str, scenario: str) -> Path:
    return (root / condition / f"{scenario}.spec.ts").resolve()


def _outcome_dict(outcome: RunOutcome) -> dict[str, Any]:
    return {
        "status": outcome.status,
        "mutation_events": list(outcome.mutation_events),
        "control_observation": outcome.control_observation,
        "returncode": outcome.returncode,
        "duration_seconds": outcome.duration_seconds,
        "error_type": outcome.error_type,
        "error_message_excerpt": outcome.error_message_excerpt,
        "artifacts_dir": outcome.artifacts_dir,
    }


def _configured_environment_names() -> list[str]:
    return sorted(
        name
        for name in (
            "PROMPT_E2E_BASE_URL",
            "BASE_URL",
            "DEMO_WEB_SHOP_EMAIL",
            "DEMO_WEB_SHOP_PASSWORD",
            "E2E_EMAIL",
            "E2E_PASSWORD",
            "TEST_EMAIL",
            "TEST_PASSWORD",
        )
        if name in os.environ
    )


def _signed_payload_hash(payload: dict[str, Any], signature_field: str) -> str:
    unsigned = dict(payload)
    unsigned.pop(signature_field, None)
    canonical = json.dumps(
        unsigned,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _verify_signed_payload(payload: dict[str, Any], signature_field: str) -> bool:
    expected = str(payload.get(signature_field, ""))
    return bool(expected) and expected == _signed_payload_hash(
        payload,
        signature_field,
    )


def _runtime_metadata(node_project: Path) -> dict[str, str]:
    return {
        "node": _version_command(["node", "--version"], node_project),
        "playwright": _version_command(["npx", "playwright", "--version"], node_project),
        "chromium": _version_command(
            [
                "node",
                "-e",
                (
                    "const {chromium}=require('@playwright/test');"
                    "(async()=>{const b=await chromium.launch({headless:true});"
                    "console.log(b.version());await b.close();})()"
                ),
            ],
            node_project,
        ),
    }


def _version_command(command: list[str], cwd: Path) -> str:
    try:
        completed = subprocess.run(
            command,
            cwd=cwd.resolve(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
            timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        return f"unavailable: {_excerpt(str(error))}"
    if completed.returncode != 0:
        return f"unavailable: {_excerpt(completed.stderr)}"
    return completed.stdout.strip()


def _excerpt(value: str, limit: int = 500) -> str:
    normalized = " ".join(value.split())
    return normalized if len(normalized) <= limit else normalized[: limit - 1].rstrip() + "…"


def _markdown_report(payload: dict[str, Any], condition_key: dict[str, str]) -> str:
    strata: dict[str, list[dict[str, Any]]] = {}
    invalid = 0
    for mutation in payload["mutation_results"]:
        if not mutation["control_valid"]:
            invalid += 1
            continue
        if not mutation["paired_applicable"]:
            continue
        strata.setdefault(mutation["stratum"], []).append(mutation)
    not_applicable = sum(
        1
        for mutation in payload["mutation_results"]
        if mutation["control_valid"] and not mutation["paired_applicable"]
    )
    lines = [
        "# Resultado da avaliação de resiliência",
        "",
        "## Escopo",
        "",
        f"- Plano de mutações: `{payload['mutation_plan_sha256']}`.",
        f"- Cenários elegíveis nas duas condições: {len(payload['eligible_scenarios'])}.",
        f"- Repetições: {payload['repetitions']}.",
        f"- Mutações selecionadas: {len(payload['mutation_results'])}.",
        (
            f"- Seleção reduzida: até {payload['selection']['mutations_per_scenario']} mutações neutras por cenário "
            "(uma E1 e uma E2 quando disponível; desempate por hash do plano)."
            if payload["selection"]["mode"] == "deterministic_neutral_sample"
            else f"- Modo de seleção: `{payload['selection']['mode']}`."
        ),
        f"- Mutantes inválidos pelo controle diferencial: {invalid}.",
        f"- Mutantes não aplicáveis porque ambos os testes não interagiram com o alvo original: {not_applicable}.",
        "- Os resultados são apresentados por estrato; não há conclusão universal baseada em média única.",
        "",
        "## Comparação pareada por estrato",
        "",
        "| Estrato | Pares válidos | Ambos passam | Só baseline | Só estruturado | Ambos falham | McNemar exato |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for stratum in sorted(strata):
        counts = {"both": 0, "A": 0, "B": 0, "neither": 0}
        for mutation in strata[stratum]:
            a_outcomes = [
                run["outcomes"].get("A")
                for run in mutation["condition_runs"]
            ]
            b_outcomes = [
                run["outcomes"].get("B")
                for run in mutation["condition_runs"]
            ]
            a = len(a_outcomes) == payload["repetitions"] and all(
                outcome == "passed_interacted" for outcome in a_outcomes
            )
            b = len(b_outcomes) == payload["repetitions"] and all(
                outcome == "passed_interacted" for outcome in b_outcomes
            )
            counts["both" if a and b else "A" if a else "B" if b else "neither"] += 1
        p_value = _mcnemar_exact(counts["A"], counts["B"])
        baseline_only = counts["A"] if condition_key["A"] == "baseline" else counts["B"]
        structured_only = counts["B"] if condition_key["B"] == "structured_context" else counts["A"]
        total = sum(counts.values())
        lines.append(
            f"| {stratum} | {total} | {counts['both']} | {baseline_only} | {structured_only} "
            f"| {counts['neither']} | {p_value:.4f} |"
        )
    lines.extend([
        "",
        "## Resultado por mutação",
        "",
        f"Condição A: **{condition_key['A']}**. Condição B: **{condition_key['B']}**.",
        "",
        "| Cenário | Mutação | Estrato | Operador | Controle | Aplicável ao par | A | B |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ])
    for mutation in payload["mutation_results"]:
        outcomes_a = ", ".join(run["outcomes"].get("A", "-") for run in mutation["condition_runs"]) or "-"
        outcomes_b = ", ".join(run["outcomes"].get("B", "-") for run in mutation["condition_runs"]) or "-"
        lines.append(
            f"| `{mutation['scenario_id']}` | `{mutation['mutation_id']}` | {mutation['stratum']} "
            f"| `{mutation['operator']}` | {'válido' if mutation['control_valid'] else 'inválido'} "
            f"| {'sim' if mutation['paired_applicable'] else 'não'} | {outcomes_a} | {outcomes_b} |"
        )
    lines.extend([
        "",
        "## Cenários elegíveis",
        "",
        *[f"- `{scenario}`" for scenario in payload["eligible_scenarios"]],
        "",
        "## Limite",
        "",
        "Os valores descrevem somente os operadores e elementos do plano utilizado nesta execução. "
        "Mudanças do contrato visível ou acessível não devem ser interpretadas como o mesmo fenômeno de mudanças internas neutras. "
        "Cenários diferentes podem reutilizar o mesmo componente da interface; nesses casos, os pares não são "
        "evidências independentes da quantidade de componentes alterados.",
        "",
    ])
    return "\n".join(lines)


def _mcnemar_exact(left_only: int, right_only: int) -> float:
    discordant = left_only + right_only
    if discordant == 0:
        return 1.0
    tail = sum(math.comb(discordant, k) for k in range(0, min(left_only, right_only) + 1)) / (2**discordant)
    return min(1.0, 2 * tail)
