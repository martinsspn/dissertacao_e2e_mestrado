from __future__ import annotations

import re

from teste_prompt_e2e_semantico.domain.models import NavigationTransition, SelectorCandidate, UiElement


_PRIORITY = (
    "data-testid",
    "data-test",
    "testid",
    "aria_label",
    "label",
    "id",
    "name",
    "placeholder",
    "role_name",
    "text",
    "href",
    "role",
    "css",
)
_REJECTED = ("xpath", "nth", "index")
_DYNAMIC_COUNTER = re.compile(r"\s*\(\d+\)\s*$")


def best_selector_for(control: NavigationTransition | UiElement) -> SelectorCandidate | None:
    """Choose one selector by a fixed, documented priority order."""
    selectors = _flatten_selectors(control.selectors)
    text = control.element.get("text", "")
    if _DYNAMIC_COUNTER.search(text):
        for key, value in selectors:
            if key.casefold() in {"data-testid", "data-test", "testid", "aria_label", "id", "name"}:
                return SelectorCandidate(kind=key, value=value)

        # A destination alone is not necessarily unique: after an AJAX
        # update, header, notification and menu links may share the same href.
        # For links whose only varying part is a final counter, expose the
        # counter-free accessible name and require an exact role/name match.
        tag = control.element.get("tag", "").casefold()
        if tag == "a" or control.kind.casefold() == "link":
            stable_name = _DYNAMIC_COUNTER.sub("", text).strip()
            if stable_name:
                return SelectorCandidate(kind="role_name_exact", value=stable_name)

        for key, value in selectors:
            if key.casefold() == "href":
                return SelectorCandidate(kind=key, value=value)
    for marker in _PRIORITY:
        for key, value in selectors:
            normalized_key = key.casefold()
            if marker in normalized_key and not any(item in normalized_key for item in _REJECTED):
                return SelectorCandidate(kind=key, value=value)
    return _selector_from_element(control)


def selector_priority_for(control: NavigationTransition | UiElement) -> int:
    """Return the fixed selector-policy position used to break equivalent matches."""
    selector = best_selector_for(control)
    if selector is None:
        return len(_PRIORITY) + 1
    normalized_kind = selector.kind.casefold()
    for index, marker in enumerate(_PRIORITY):
        if marker in normalized_kind:
            return index
    return len(_PRIORITY)


def _flatten_selectors(selectors: dict[str, object]) -> list[tuple[str, str]]:
    flattened: list[tuple[str, str]] = []
    for key, value in selectors.items():
        if isinstance(value, str) and value.strip():
            flattened.append((key, value.strip()))
        elif isinstance(value, (int, float, bool)):
            flattened.append((key, str(value)))
        elif isinstance(value, list):
            flattened.extend(
                (f"{key}[{index}]", item.strip())
                for index, item in enumerate(value)
                if isinstance(item, str) and item.strip()
            )
        elif isinstance(value, dict):
            flattened.extend(
                (f"{key}.{child_key}", str(child_value).strip())
                for child_key, child_value in value.items()
                if child_value is not None and str(child_value).strip()
            )
    return flattened


def _selector_from_element(control: NavigationTransition | UiElement) -> SelectorCandidate | None:
    element = control.element
    for key in ("aria_label", "label", "id", "name", "placeholder"):
        value = element.get(key, "").strip()
        if value:
            return SelectorCandidate(kind=key, value=value)

    tag = element.get("tag", "").casefold()
    input_type = element.get("input_type", "").casefold()
    accessible_name = element.get("value", "").strip()
    # A value-only generic button can occur many times on the same page (for
    # example, product-list "Add to cart" buttons). Submit controls are tied to
    # one form and remain useful when no stable attribute exists.
    if tag == "input" and input_type == "submit" and accessible_name:
        return SelectorCandidate(kind="role_name", value=accessible_name)

    for key in ("text", "href", "role"):
        value = element.get(key, "").strip()
        if value:
            return SelectorCandidate(kind=key, value=value)
    return None
