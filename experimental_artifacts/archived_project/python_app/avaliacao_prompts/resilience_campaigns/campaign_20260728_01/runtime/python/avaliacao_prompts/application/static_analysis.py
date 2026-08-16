from __future__ import annotations

import re

from avaliacao_prompts.domain.models import SelectorRisk, StaticAnalysisResult


_PLAYWRIGHT_IMPORT = re.compile(r"from\s+['\"]@playwright/test['\"]")
_TEST_BLOCK = re.compile(r"\btest(?:\.\w+)?\s*\(")
_EXPECT_CALL = re.compile(r"\bexpect\s*\(")
_GOTO_URL = re.compile(r"\bpage\.goto\s*\(\s*(['\"`])(?P<url>[^'\"`]+)\1")
_SEMANTIC_LOCATOR = re.compile(r"\bgetBy(?:Role|Label|Placeholder|Text|AltText|Title|TestId)\s*\(")
_LOCATOR = re.compile(r"\b(?:page|frame|locator)\.locator\s*\(")
_STRING_ARG = re.compile(r"(['\"`])(?P<value>[^'\"`]{2,160})\1")
_ACTION = re.compile(r"\.(?:click|fill|check|uncheck|selectOption|press|type|hover)\s*\(")
_XPATH_MARKERS = re.compile(r"xpath=|/HTML\[|(['\"`])\s*//[A-Za-z]|\(\s*//", re.IGNORECASE)


def analyze_static_test_source(source: str) -> StaticAnalysisResult:
    goto_urls = _unique(_GOTO_URL.findall(source), tuple_index=1)
    locator_texts = _extract_locator_texts(source)
    semantic_locator_count = len(_SEMANTIC_LOCATOR.findall(source))
    css_locator_count = len(_LOCATOR.findall(source))
    locator_count = semantic_locator_count + css_locator_count
    xpath_count = len(_XPATH_MARKERS.findall(source))
    uses_wait_for_timeout = "waitForTimeout" in source

    return StaticAnalysisResult(
        has_playwright_import=bool(_PLAYWRIGHT_IMPORT.search(source)),
        has_test_block=bool(_TEST_BLOCK.search(source)),
        has_expect_assertion=bool(_EXPECT_CALL.search(source)),
        uses_wait_for_timeout=uses_wait_for_timeout,
        goto_urls=goto_urls,
        locator_texts=locator_texts,
        locator_count=locator_count,
        semantic_locator_count=semantic_locator_count,
        xpath_count=xpath_count,
        action_count=len(_ACTION.findall(source)),
        selector_risk=_selector_risk(locator_count, semantic_locator_count, xpath_count, uses_wait_for_timeout),
    )


def _extract_locator_texts(source: str) -> list[str]:
    texts: list[str] = []
    for call in re.finditer(r"\b(?:getBy\w+|locator)\s*\((?P<args>[^;\n]+)", source):
        for match in _STRING_ARG.finditer(call.group("args")):
            value = match.group("value").strip()
            if _is_meaningful_locator_text(value):
                texts.append(value)
    return _unique(texts)


def _is_meaningful_locator_text(value: str) -> bool:
    normalized = re.sub(r"\s+", " ", value).strip().lower()
    if len(normalized) < 2:
        return False
    if normalized in {"button", "link", "textbox", "dialog", "heading", "main", "form"}:
        return False
    return not normalized.startswith(("#", ".", "[", "xpath=", "//", "/html["))


def _selector_risk(
    locator_count: int,
    semantic_locator_count: int,
    xpath_count: int,
    uses_wait_for_timeout: bool,
) -> SelectorRisk:
    if locator_count == 0:
        return "none"
    if xpath_count > 0 or uses_wait_for_timeout:
        return "high"
    if semantic_locator_count / max(1, locator_count) >= 0.6:
        return "low"
    return "medium"


def _unique(values: list[object], tuple_index: int | None = None) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        item = value[tuple_index] if tuple_index is not None and isinstance(value, tuple) else value
        text = str(item).strip()
        if text and text not in seen:
            seen.add(text)
            result.append(text)
    return result
