from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class CatalogTarget:
    target_id: str
    scenario_id: str
    step: int
    ordinal: str
    page_url: str
    action: str
    tag: str
    attributes: dict[str, str]
    source_prompt: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PlannedMutation:
    mutation_id: str
    stratum: str
    operator: str
    target: CatalogTarget
    parameters: dict[str, str]

    def as_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["target"] = self.target.as_dict()
        return payload

