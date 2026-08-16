from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import asdict, dataclass
from pathlib import Path

from avaliacao_prompts.resilience.plan import verify_plan


_IMPORT = re.compile(r"(?P<prefix>from\s+)(?P<quote>['\"])@playwright/test(?P=quote)(?P<suffix>\s*;?)")


@dataclass(frozen=True)
class TestPair:
    scenario_id: str
    baseline_original: str
    structured_original: str
    baseline_sha256: str
    structured_sha256: str
    baseline_derived: str
    structured_derived: str


def prepare_execution(
    baseline_dir: Path,
    structured_dir: Path,
    fixture: Path,
    frozen_plan: Path,
    output_dir: Path,
    allowlist: Path,
    semantic_review: Path,
    track_id: str,
    model_id: str,
) -> Path:
    if output_dir.exists():
        raise FileExistsError(
            f"O diretório de execução já existe e não será sobrescrito: {output_dir}"
        )
    plan = json.loads(frozen_plan.read_text(encoding="utf-8"))
    if not verify_plan(plan):
        raise ValueError("O plano de mutações não possui hash interno válido.")
    baseline = _index_tests(baseline_dir, "baseline")
    structured = _index_tests(structured_dir, "structured_context")
    allowed = _read_allowlist(allowlist, track_id=track_id, model_id=model_id)
    paired = baseline.keys() & structured.keys()
    missing = sorted(allowed - paired)
    if missing:
        raise ValueError(
            "Cenários da allowlist sem par baseline/contexto: "
            + ", ".join(missing)
        )
    scenarios = sorted(allowed)

    baseline_output = output_dir / "A"
    structured_output = output_dir / "B"
    baseline_output.mkdir(parents=True)
    structured_output.mkdir(parents=True)
    pairs: list[TestPair] = []
    for scenario in scenarios:
        left = baseline[scenario]
        right = structured[scenario]
        left_target = baseline_output / f"{scenario}.spec.ts"
        right_target = structured_output / f"{scenario}.spec.ts"
        left_hash = _instrument_copy(left, left_target, fixture)
        right_hash = _instrument_copy(right, right_target, fixture)
        pairs.append(
            TestPair(
                scenario_id=scenario,
                baseline_original=str(left.resolve()),
                structured_original=str(right.resolve()),
                baseline_sha256=_sha256(left.read_bytes()),
                structured_sha256=_sha256(right.read_bytes()),
                baseline_derived=left_hash,
                structured_derived=right_hash,
            )
        )

    # A/B mascara os nomes durante a execução. A chave permanece neste
    # manifesto e deve ser revelada apenas na análise final.
    payload = {
        "schema_version": 1,
        "mutation_plan": str(frozen_plan.resolve()),
        "mutation_plan_sha256": plan["plan_sha256"],
        "fixture": str(fixture.resolve()),
        "fixture_sha256": _sha256(fixture.read_bytes()),
        "track_id": track_id,
        "model_id": model_id,
        "allowlist": str(allowlist.resolve()),
        "allowlist_sha256": _sha256(allowlist.read_bytes()),
        "semantic_review": str(semantic_review.resolve()),
        "semantic_review_sha256": _sha256(semantic_review.read_bytes()),
        "transformation": "only_replace_import_source_from_@playwright/test_to_frozen_fixture",
        "condition_key": {"A": "baseline", "B": "structured_context"},
        "pairs": [asdict(pair) for pair in pairs],
    }
    canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    payload["execution_manifest_sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    output = output_dir / "execution_manifest.json"
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return output.resolve()


def scenario_id_for_test(path: Path, approach: str) -> str:
    stem = path.name.removesuffix(".spec.ts")
    suffix = "_baseline" if approach == "baseline" else "_estruturado"
    opposite_suffix = "_estruturado" if approach == "baseline" else "_baseline"
    if stem.endswith(opposite_suffix):
        raise ValueError(f"Nome de teste incompatível com {approach}: {path.name}")
    if not stem.endswith(suffix):
        return stem
    name = stem.removesuffix(suffix).removeprefix("teste_")
    aliases = {
        "buscar_blue_jeans": "suite_busca_blue_jeans",
        "wishlist": "suite_adicionar_wishlist",
    }
    return aliases.get(name, f"suite_{name}")


def _index_tests(directory: Path, approach: str) -> dict[str, Path]:
    result: dict[str, Path] = {}
    for path in sorted(directory.resolve().glob("*.spec.ts")):
        scenario = scenario_id_for_test(path, approach)
        if scenario in result:
            raise ValueError(f"Mais de um teste para o cenário {scenario} em {directory}")
        result[scenario] = path
    return result


def _instrument_copy(source: Path, target: Path, fixture: Path) -> str:
    text = source.read_text(encoding="utf-8")
    relative_fixture = Path(os.path.relpath(fixture.resolve(), target.parent.resolve())).as_posix()
    if not relative_fixture.startswith("."):
        relative_fixture = f"./{relative_fixture}"
    replacement = rf"\g<prefix>\g<quote>{relative_fixture}\g<quote>\g<suffix>"
    transformed, count = _IMPORT.subn(replacement, text, count=1)
    if count != 1:
        raise ValueError(f"Importação única de @playwright/test não encontrada em {source}")
    target.write_text(transformed, encoding="utf-8")
    return _sha256(transformed.encode("utf-8"))


def _sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def _read_allowlist(path: Path, *, track_id: str, model_id: str) -> set[str]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("schema_version") != 1:
        raise ValueError("Allowlist deve usar schema_version=1.")
    if payload.get("track_id") != track_id:
        raise ValueError("A trilha informada não corresponde à allowlist.")
    if payload.get("model_id") != model_id:
        raise ValueError("O modelo informado não corresponde à allowlist.")
    scenarios = payload.get("scenario_ids")
    if not isinstance(scenarios, list) or not scenarios:
        raise ValueError("Allowlist deve conter scenario_ids não vazio.")
    if any(not isinstance(item, str) or not item.strip() for item in scenarios):
        raise ValueError("Todos os scenario_ids da allowlist devem ser textos não vazios.")
    normalized = {item.strip() for item in scenarios}
    if len(normalized) != len(scenarios):
        raise ValueError("Allowlist contém cenários duplicados.")
    return normalized
