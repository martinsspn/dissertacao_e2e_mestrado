from __future__ import annotations

import re

from teste_prompt_e2e_semantico.domain.models import SpecificationStep


_BULLET_PREFIX = re.compile(r"^\s*(?:[-*+]\s+|\d+[.)]\s+)")
_SENTENCE_BOUNDARY = re.compile(r"(?<=[.!?])\s+")
_INLINE_SCENARIO_TITLE = re.compile(
    r"^\s*[^\n:.!?]{1,120}:\s+(?=(?:the\s+)?(?:user|system|page|application|interface)\b)",
    re.IGNORECASE,
)


def segment_specification(raw_text: str) -> list[SpecificationStep]:
    """Organize a specification into ordered textual steps without interpreting it."""
    lines = [_clean_line(line) for line in raw_text.splitlines()]
    lines = [line for line in lines if line and not line.endswith(":")]

    if len(lines) <= 1:
        paragraph = lines[0] if lines else raw_text
        fragments = _split_sentences(_strip_inline_scenario_title(paragraph))
    else:
        fragments = lines

    unique_fragments: list[str] = []
    seen: set[str] = set()
    for fragment in fragments:
        normalized = re.sub(r"\s+", " ", fragment).strip()
        identity = normalized.casefold()
        if normalized and identity not in seen:
            seen.add(identity)
            unique_fragments.append(normalized)

    return [SpecificationStep(id=f"R{index}", text=text) for index, text in enumerate(unique_fragments, start=1)]


def _clean_line(line: str) -> str:
    return _BULLET_PREFIX.sub("", line).strip()


def _split_sentences(text: str) -> list[str]:
    return [fragment.strip() for fragment in _SENTENCE_BOUNDARY.split(text.strip()) if fragment.strip()]


def _strip_inline_scenario_title(text: str) -> str:
    """Remove a descriptive ``Scenario title:`` prefix, not requirement text."""
    return _INLINE_SCENARIO_TITLE.sub("", text or "", count=1).strip()
