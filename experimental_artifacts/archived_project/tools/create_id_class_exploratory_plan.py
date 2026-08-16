from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from pathlib import Path


SOURCE = Path("python_app/avaliacao_prompts/resilience_artifacts/frozen_mutation_plan.json")
OUTPUT = Path("python_app/avaliacao_prompts/resilience_artifacts/id_class_exploratory_plan.json")
SCENARIO = "suite_busca_blue_jeans"


def mutation_id(target_id: str, operator: str, parameters: dict[str, str]) -> str:
    material = f"id-class-exploratory-v1|{target_id}|{operator}|{json.dumps(parameters, sort_keys=True)}"
    return f"mutation-{hashlib.sha256(material.encode()).hexdigest()[:16]}"


def main() -> None:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    scenario_mutations = [
        item for item in source["mutations"] if item["target"]["scenario_id"] == SCENARIO
    ]
    search_field = next(
        deepcopy(item["target"])
        for item in scenario_mutations
        if item["target"]["attributes"].get("id") == "small-searchterms"
    )
    search_button = next(
        deepcopy(item["target"])
        for item in scenario_mutations
        if item["target"]["attributes"].get("input_type") == "submit"
        and item["target"]["attributes"].get("value") == "Search"
    )

    definitions = [
        (search_field, "rename_id", {"new_value": "small-searchterms--exploratory"}),
        (
            search_field,
            "rename_class",
            {"old_value": "search-box-text", "new_value": "search-box-text--exploratory"},
        ),
        (
            search_button,
            "rename_class",
            {"old_value": "search-box-button", "new_value": "search-box-button--exploratory"},
        ),
    ]
    mutations = []
    for target, operator, parameters in definitions:
        mutations.append(
            {
                "mutation_id": mutation_id(target["target_id"], operator, parameters),
                "stratum": "implementation_attribute_change",
                "operator": operator,
                "target": target,
                "parameters": parameters,
            }
        )

    payload = {
        "schema_version": 1,
        "selection_method": "exploratory_homepage_search_controls_without_reading_test_locators",
        "source_disclosure": (
            "Targets came from the frozen pre-generation catalog. Class names were read from "
            "the public DOM on 2026-07-20. This is a separate exploratory plan created after "
            "initial results and is not part of the confirmatory frozen plan."
        ),
        "source_plan_sha256": source["plan_sha256"],
        "observed_dom_classes": {
            "small-searchterms": "search-box-text ui-autocomplete-input",
            "Search submit": "button-1 search-box-button",
        },
        "catalog_size": 2,
        "mutation_count": len(mutations),
        "mutations": mutations,
    }
    canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    payload["plan_sha256"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUTPUT.resolve())
    print(payload["plan_sha256"])
    for item in mutations:
        print(item["mutation_id"], item["operator"], item["parameters"])


if __name__ == "__main__":
    main()
