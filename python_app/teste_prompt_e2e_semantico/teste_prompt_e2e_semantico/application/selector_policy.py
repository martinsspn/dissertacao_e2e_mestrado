from __future__ import annotations

import re

from teste_prompt_e2e_semantico.domain.models import NavigationTransition, SelectorCandidate


_STRONG_KEYS = ("role", "aria", "label", "testid", "data-testid", "data-test", "placeholder")
_MEDIUM_KEYS = ("id", "name", "text", "href", "css")
_WEAK_KEYS = ("xpath", "class", "nth", "index")
_LOW_VALUE_TEXTS = {
    "",
    "(0)",
    "0",
    "home",
    "home/",
    "prev",
    "next",
    "wait...",
    "loading",
    "categories",
}


def selector_candidates_for(transition: NavigationTransition, limit: int = 5) -> list[SelectorCandidate]:
    candidates: list[SelectorCandidate] = []
    for key, value in _flatten_selectors(transition.selectors).items():
        candidate = _classify_selector(key, value, transition.selector_scores.get(key))
        if candidate is not None:
            candidates.append(candidate)

    candidates.sort(key=lambda candidate: candidate.score, reverse=True)
    return candidates[:limit]


def selector_quality_score(transition: NavigationTransition) -> float:
    candidates = selector_candidates_for(transition, limit=3)
    if not candidates:
        return 0.0
    return sum(candidate.score for candidate in candidates) / len(candidates)


def _flatten_selectors(selectors: dict[str, object]) -> dict[str, str]:
    flattened: dict[str, str] = {}
    for key, value in selectors.items():
        if value is None:
            continue
        if isinstance(value, str):
            if value.strip():
                flattened[key] = value.strip()
            continue
        if isinstance(value, (int, float, bool)):
            flattened[key] = str(value)
            continue
        if isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, str) and item.strip():
                    flattened[f"{key}[{index}]"] = item.strip()
            continue
        if isinstance(value, dict):
            for child_key, child_value in value.items():
                if child_value is not None and str(child_value).strip():
                    flattened[f"{key}.{child_key}"] = str(child_value).strip()
    return flattened


def _classify_selector(key: str, value: str, source_score: object) -> SelectorCandidate | None:
    normalized_key = key.lower()
    normalized_value = value.lower()
    base = _coerce_score(source_score)
    score_cap = 1.0
    reason = "selector disponivel no grafo"

    if any(marker in normalized_key for marker in _STRONG_KEYS):
        base += 0.35
        reason = "preferivel por representar atributo semantico ou de teste"
    elif any(marker in normalized_key for marker in _MEDIUM_KEYS):
        base += 0.15
        reason = "util quando nao houver seletor semantico melhor"
    elif any(marker in normalized_key for marker in _WEAK_KEYS):
        base -= 0.45
        score_cap = min(score_cap, 0.35)
        reason = "fragil; usar apenas se nao houver alternativa"

    if "xpath" in normalized_key:
        base -= 0.35
        score_cap = min(score_cap, 0.25)
        reason = "xpath tende a quebrar com mudancas estruturais"
    if "text" in normalized_key and _is_low_value_text(value):
        base -= 0.65
        score_cap = min(score_cap, 0.35)
        reason = "texto pouco descritivo para acao de usuario"
    if "nth-child" in normalized_value or re.search(r":nth-\w+\(", normalized_value):
        base -= 0.3
        score_cap = min(score_cap, 0.25)
        reason = "depende de posicao no DOM"
    if len(value) > 120:
        base -= 0.45
        score_cap = min(score_cap, 0.3)
        reason = "seletor longo aumenta fragilidade"
    if _looks_generated(value):
        base -= 0.15
        score_cap = min(score_cap, 0.45)
        reason = "valor parece gerado dinamicamente"

    if len(value) > 500:
        return None

    score = max(0.0, min(score_cap, base))
    if score >= 0.7:
        strength = "strong"
    elif score >= 0.4:
        strength = "medium"
    else:
        strength = "weak"

    return SelectorCandidate(kind=key, value=value, score=score, strength=strength, reason=reason)


def _coerce_score(value: object) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            return 0.5
    return 0.5


def _looks_generated(value: str) -> bool:
    return bool(
        re.search(r"[a-f0-9]{8,}", value.lower())
        or re.search(r"\b\d{5,}\b", value)
        or re.search(r"(ember|react|vue|ng)-?\d+", value.lower())
    )


def _is_low_value_text(value: str) -> bool:
    normalized = re.sub(r"\s+", " ", value).strip().lower()
    if normalized in _LOW_VALUE_TEXTS:
        return True
    if not re.search(r"[a-zA-Z]", normalized):
        return True
    if len(normalized) <= 2:
        return True
    if len(value) > 40 and " " not in value.strip():
        return True
    return False
