from __future__ import annotations

import hashlib
import json
from pathlib import Path

from avaliacao_prompts.resilience.catalog import aggregate_hash, build_catalog, hash_files
from avaliacao_prompts.resilience.models import CatalogTarget, PlannedMutation


def build_plan(specs_dir: Path, prompt_dir: Path) -> dict:
    spec_files = sorted(specs_dir.resolve().glob("*.txt"))
    prompt_files = sorted(prompt_dir.resolve().glob("*.structured_context.prompt.md"))
    if not spec_files or not prompt_files:
        raise ValueError("Especificações e prompts estruturados são obrigatórios para gerar o plano.")
    spec_hashes = hash_files(spec_files)
    prompt_hashes = hash_files(prompt_files)
    source_hash = aggregate_hash({f"spec/{k}": v for k, v in spec_hashes.items()} | {f"prompt/{k}": v for k, v in prompt_hashes.items()})
    catalog = build_catalog(prompt_dir)
    mutations = tuple(
        mutation
        for target in catalog
        for mutation in _applicable_mutations(target)
    )
    payload = {
        "schema_version": 1,
        "selection_method": "exhaustive_all_applicable_operators_without_reading_generated_tests",
        "source_disclosure": (
            "Targets are parsed from structured prompts produced before test generation. "
            "The plan generator does not read .spec.ts files or evaluation results."
        ),
        "source_aggregate_sha256": source_hash,
        "specification_sha256": spec_hashes,
        "structured_prompt_sha256": prompt_hashes,
        "catalog_size": len(catalog),
        "mutation_count": len(mutations),
        "strata": {
            "E1": "DOM structure changed; visible and accessible contract preserved",
            "E2": "implementation attribute or equivalent markup changed; perceptible contract preserved",
            "E3": "visible or accessible contract changed; reported separately",
            "E4": "explicit test contract changed; reported separately",
        },
        "mutations": [mutation.as_dict() for mutation in mutations],
    }
    canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    payload["plan_sha256"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return payload


def write_plan(output: Path, payload: dict) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return output.resolve()


def verify_plan(payload: dict) -> bool:
    expected = str(payload.get("plan_sha256", ""))
    unsigned = dict(payload)
    unsigned.pop("plan_sha256", None)
    canonical = json.dumps(unsigned, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    actual = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return bool(expected) and expected == actual


def _applicable_mutations(target: CatalogTarget) -> tuple[PlannedMutation, ...]:
    definitions: list[tuple[str, str, dict[str, str]]] = [
        ("E1", "insert_wrapper", {"tag": "div"}),
        ("E1", "insert_noninteractive_sibling_before", {"tag": "span"}),
    ]
    attributes = target.attributes
    if attributes.get("id"):
        definitions.append(("E2", "rename_id", {"new_value": f"{attributes['id']}--e2"}))
    classes = attributes.get("classes", attributes.get("class", "")).split()
    if classes:
        definitions.append(("E2", "rename_class", {"old_value": classes[0], "new_value": f"{classes[0]}--e2"}))
    if target.tag == "input" and attributes.get("input_type") == "submit":
        definitions.append(("E2", "input_submit_to_button", {}))
    if any(attributes.get(name) for name in ("label", "text", "value", "aria-label")):
        definitions.append(("E3", "change_accessible_name", {"suffix": " updated"}))
    test_id = attributes.get("data-testid") or attributes.get("data_testid")
    if test_id:
        definitions.append(("E4", "rename_test_id", {"new_value": f"{test_id}--e4"}))

    mutations: list[PlannedMutation] = []
    for stratum, operator, parameters in definitions:
        identity = f"{target.target_id}|{stratum}|{operator}|{json.dumps(parameters, sort_keys=True)}"
        mutations.append(
            PlannedMutation(
                mutation_id=f"mutation-{hashlib.sha256(identity.encode()).hexdigest()[:16]}",
                stratum=stratum,
                operator=operator,
                target=target,
                parameters=parameters,
            )
        )
    return tuple(mutations)
