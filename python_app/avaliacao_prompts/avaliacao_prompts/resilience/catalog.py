from __future__ import annotations

import hashlib
import re
from pathlib import Path

from avaliacao_prompts.resilience.models import CatalogTarget


_STEP = re.compile(r"^Etapa\s+(?P<number>\d+)\s+\(R\d+\):$")
_FIELD = re.compile(r"^-\s+(?P<name>[a-z_]+?)(?:_(?P<ordinal>\d+))?=(?P<value>.*)$")
_ATTRIBUTE = re.compile(r"(?P<name>[a-z_][a-z0-9_-]*)=(?P<value>[^,]+)(?:,\s*|$)")


def build_catalog(prompt_dir: Path) -> tuple[CatalogTarget, ...]:
    targets: list[CatalogTarget] = []
    for prompt in sorted(prompt_dir.resolve().glob("*.structured_context.prompt.md")):
        targets.extend(_targets_from_prompt(prompt))
    unique = {target.target_id: target for target in targets}
    return tuple(unique[key] for key in sorted(unique))


def _targets_from_prompt(path: Path) -> list[CatalogTarget]:
    scenario_id = path.name.removesuffix(".structured_context.prompt.md")
    lines = path.read_text(encoding="utf-8").splitlines()
    in_context = False
    current_step: int | None = None
    fields: dict[tuple[int, str], dict[str, str]] = {}
    for line in lines:
        if line == "Contexto estruturado por etapa:":
            in_context = True
            continue
        if not in_context:
            continue
        step_match = _STEP.match(line)
        if step_match:
            current_step = int(step_match.group("number"))
            continue
        if current_step is None:
            continue
        match = _FIELD.match(line)
        if not match:
            if line.startswith(("Etapas sem contexto", "Use as informacoes")):
                current_step = None
            continue
        name = match.group("name")
        ordinal = match.group("ordinal") or "0"
        fields.setdefault((current_step, ordinal), {})[name] = match.group("value").strip()

    result: list[CatalogTarget] = []
    for (step, ordinal), values in sorted(fields.items()):
        control = values.get("controle")
        if not control:
            continue
        attributes = {
            match.group("name"): match.group("value").strip()
            for match in _ATTRIBUTE.finditer(control)
        }
        tag = attributes.pop("tag", "").lower()
        # O formato compacto registra `pagina=` uma única vez para todos os
        # controles numerados da etapa. Herdar esse valor não depende do teste
        # gerado nem de seu resultado.
        shared_values = fields.get((step, "0"), {})
        page_url = values.get("pagina", shared_values.get("pagina", ""))
        action = values.get("operacao", "")
        identity = "|".join(
            [scenario_id, str(step), ordinal, page_url, action, tag]
            + [f"{key}={attributes[key]}" for key in sorted(attributes)]
        )
        result.append(
            CatalogTarget(
                target_id=f"target-{hashlib.sha256(identity.encode()).hexdigest()[:16]}",
                scenario_id=scenario_id,
                step=step,
                ordinal=ordinal,
                page_url=page_url,
                action=action,
                tag=tag,
                attributes=attributes,
                source_prompt=path.name,
            )
        )
    return result


def hash_files(paths: list[Path]) -> dict[str, str]:
    return {
        path.name: hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted((item.resolve() for item in paths), key=lambda item: item.name)
    }


def aggregate_hash(hashes: dict[str, str]) -> str:
    canonical = "\n".join(f"{name}:{hashes[name]}" for name in sorted(hashes))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
