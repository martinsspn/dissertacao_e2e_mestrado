from __future__ import annotations

import re
from dataclasses import dataclass
from urllib.parse import urljoin, urlsplit

from teste_prompt_e2e_semantico.application.selector_policy import best_selector_for, selector_priority_for
from teste_prompt_e2e_semantico.application.text_normalization import normalize_text
from teste_prompt_e2e_semantico.domain.models import (
    ContextElement,
    InteractionContext,
    NavigationGraph,
    NavigationTransition,
    PageEvidence,
    PageNode,
    SpecificationStep,
    StepContext,
    StructuredContext,
    UiElement,
)


_DYNAMIC_COUNTER = re.compile(r"\s*\(\d+\)\s*$")
_LABEL_FIELDS = ("text", "aria_label", "label", "placeholder", "value", "title")
_TRAILING_LABEL_PUNCTUATION = re.compile(r"[\s:;,.!?*]+$")
_CAMEL_ACRONYM_BOUNDARY = re.compile(r"([A-Z]+)([A-Z][a-z])")
_CAMEL_WORD_BOUNDARY = re.compile(r"([a-z0-9])([A-Z])")
_IDENTIFIER_SEPARATOR = re.compile(r"[-_.:]+")
_TRAILING_IDENTIFIER_NUMBER = re.compile(r"(?:\s+\d+)+$")
_MAX_PAGE_EVIDENCE_LENGTH = 120
_MIN_EXCERPT_EVIDENCE_WORDS = 3
_VERIFICATION_SUBJECT = re.compile(r"^\s*(?:the\s+)?(?:system|page|application|interface)\b", re.IGNORECASE)
_LEADING_USER_VERIFICATION = re.compile(
    r"^\s*(?:the\s+)?user\s+(?:verifies|checks|confirms)\s+(?:that|whether|if)\b",
    re.IGNORECASE,
)
_VERIFICATION_EXPRESSION = re.compile(
    r"\buser\s+(?:verifies|checks|confirms)\b|\b(?:is|are)\s+(?:displayed|shown|visible)\b",
    re.IGNORECASE,
)
_USER_ACTION = re.compile(
    r"\buser\s+(?:must\s+)?([A-Za-z]+)",
    re.IGNORECASE,
)
_PAGE_ENTRY_ACTIONS = {
    "access", "enter", "go", "navigate", "open", "redirect", "return", "visit",
}
_MAX_INTERACTIONS_PER_STEP = 4


@dataclass(frozen=True)
class _Candidate:
    control: UiElement
    destination_url: str
    transition: NavigationTransition | None = None


@dataclass(frozen=True)
class _EvidenceCandidate:
    evidence: PageEvidence
    specificity: tuple[int, int]
    source_priority: int


@dataclass(frozen=True)
class _ControlMatch:
    specificity: tuple[int, int]
    position: int
    label: str
    kind_priority: int


@dataclass(frozen=True)
class _MatchedCandidate:
    candidate: _Candidate
    match: _ControlMatch


@dataclass(frozen=True)
class _PageMatch:
    page: PageNode
    evidence: PageEvidence
    specificity: tuple[int, int]
    position: int


def select_structured_context(
    graph: NavigationGraph,
    base_url: str,
    requirements: list[SpecificationStep],
) -> StructuredContext:
    """Associate compact page interactions without making routes the primary filter."""
    candidates = _candidate_catalog(graph, base_url)
    current_page_url = base_url
    step_contexts = []

    for requirement_index, requirement in enumerate(requirements):
        verification_step = _is_verification_step(requirement.text)
        pure_verification_step = _is_pure_verification_step(requirement.text)
        page_matches = _matching_pages(graph.pages, requirement.text)
        if not page_matches and _contains_page_entry_action(requirement.text):
            next_requirement = (
                requirements[requirement_index + 1].text
                if requirement_index + 1 < len(requirements)
                else ""
            )
            page_matches = _page_matches_supported_by_next_interaction(
                graph.pages,
                candidates,
                requirement.text,
                next_requirement,
            )

        if pure_verification_step:
            # A verification consumes passive evidence from the active page and
            # never becomes an interaction with a homonymous control elsewhere.
            page_evidence = _select_page_evidence(
                graph.pages,
                [current_page_url],
                requirement.text,
            )
            step_contexts.append(
                StepContext(requirement_id=requirement.id, page_evidence=page_evidence)
            )
            continue

        active_scope = [current_page_url]
        matched_candidates = _matched_candidates_in_scope(
            candidates,
            requirement.text,
            active_scope,
        )
        if _contains_page_entry_action(requirement.text) or not matched_candidates:
            scope_urls = _unique_locations(
                [current_page_url, *(page_match.page.url for page_match in page_matches)]
            )
            matched_candidates = _matched_candidates_in_scope(
                candidates,
                requirement.text,
                scope_urls,
            )
        else:
            scope_urls = active_scope

        selected = _select_distinct_candidates(
            matched_candidates,
            current_page_url,
            scope_urls,
        )
        selected = _remove_incidental_links(selected, requirement.text)
        selected = _include_unique_form_companion(
            selected,
            candidates,
            requirement.text,
            scope_urls,
            current_page_url,
        )

        page_evidence = _page_evidence_for_action(
            graph.pages,
            requirement.text,
            verification_step,
            current_page_url,
            selected,
            page_matches,
        )
        interactions = tuple(
            _interaction_context(item, page_evidence)
            for item in selected[:_MAX_INTERACTIONS_PER_STEP]
        )
        step_contexts.append(
            StepContext(
                requirement_id=requirement.id,
                interactions=interactions,
                page_evidence=page_evidence,
            )
        )
        current_page_url = _next_page_url(
            current_page_url,
            requirement.text,
            selected,
            page_matches,
        )

    return StructuredContext(steps=step_contexts)


def _candidate_catalog(graph: NavigationGraph, base_url: str) -> list[_Candidate]:
    catalog: dict[tuple[str, ...], _Candidate] = {}

    for control in graph.ui_elements:
        if control.kind == "feedback":
            continue
        transition = _find_transition_for(control, graph.transitions)
        destination = _destination_for(control, transition, base_url)
        candidate = _Candidate(control=control, destination_url=destination, transition=transition)
        catalog.setdefault(_candidate_identity(candidate), candidate)

    for transition in graph.transitions:
        control = _control_from_transition(transition)
        if not _has_comparable_label(control):
            continue
        candidate = _Candidate(
            control=control,
            destination_url=transition.target.get("url", ""),
            transition=transition,
        )
        catalog.setdefault(_candidate_identity(candidate), candidate)

    return list(catalog.values())


def _find_transition_for(
    control: UiElement,
    transitions: list[NavigationTransition],
) -> NavigationTransition | None:
    for transition in transitions:
        if not _same_location(control.page_url, transition.source.get("url", "")):
            continue
        if _same_control(control.element, transition.element):
            return transition
    return None


def _same_control(first: dict[str, str], second: dict[str, str]) -> bool:
    for key in ("data_testid", "id"):
        first_value = _phrase(first.get(key, ""))
        second_value = _phrase(second.get(key, ""))
        if first_value and first_value == second_value:
            return True

    first_tag = _phrase(first.get("tag", ""))
    second_tag = _phrase(second.get("tag", ""))
    first_href = _phrase(first.get("href", ""))
    second_href = _phrase(second.get("href", ""))
    if first_href and first_href == second_href and first_tag == second_tag:
        return True

    first_name = _phrase(first.get("name", ""))
    second_name = _phrase(second.get("name", ""))
    first_value = _phrase(first.get("value", "") or first.get("label", ""))
    second_value = _phrase(second.get("value", "") or second.get("label", ""))
    if (
        first_name
        and first_name == second_name
        and first_value
        and first_value == second_value
        and _phrase(first.get("input_type", "")) == _phrase(second.get("input_type", ""))
    ):
        return True

    first_text = _phrase(first.get("text", ""))
    second_text = _phrase(second.get("text", ""))
    if first_text and first_text == second_text and first_tag == second_tag:
        first_aria = _phrase(first.get("aria_label", ""))
        second_aria = _phrase(second.get("aria_label", ""))
        return bool(first_href or (first_aria and first_aria == second_aria))
    return False


def _control_from_transition(transition: NavigationTransition) -> UiElement:
    kind = transition.interaction_kind or _kind_from_element(transition.element)
    return UiElement(
        page_url=transition.source.get("url", ""),
        kind=kind,
        suggested_operation=_operation_for(kind),
        element=transition.element,
        selectors=transition.selectors,
    )


def _destination_for(
    control: UiElement,
    transition: NavigationTransition | None,
    base_url: str,
) -> str:
    if transition is not None and transition.target.get("url"):
        return transition.target["url"]
    destination = control.element.get("href", "")
    if (
        not destination
        and control.suggested_operation == "click"
        and control.element.get("input_type", "").casefold() == "submit"
    ):
        destination = control.element.get("form_action", "")
    return urljoin(control.page_url or base_url, destination) if destination else ""


def _match_control(requirement: str, control: UiElement) -> _ControlMatch | None:
    exact_match = _exact_control_match(requirement, control)
    if exact_match is not None:
        return exact_match
    return _action_control_match(requirement, control)


def _exact_control_match(requirement: str, control: UiElement) -> _ControlMatch | None:
    requirement_phrase = _phrase(requirement)
    if not requirement_phrase:
        return None
    padded_requirement = f" {requirement_phrase} "
    matches = []
    for label in _labels(control):
        if f" {label} " not in padded_requirement:
            continue
        if not _literal_label_is_explicit(requirement, control, label):
            continue
        matches.append(
            _ControlMatch(
                specificity=(len(label.split()), len(label)),
                position=_normalized_phrase_position(requirement, label),
                label=label,
                kind_priority=0,
            )
        )
    if not matches:
        return None
    return min(
        matches,
        key=lambda item: (
            -item.specificity[0],
            -item.specificity[1],
            item.position,
            item.label,
        ),
    )


def _action_control_match(requirement: str, control: UiElement) -> _ControlMatch | None:
    action_match = _USER_ACTION.search(requirement or "")
    if action_match is None:
        return None
    action_word = _phrase(action_match.group(1))
    action_forms = _word_base_forms(action_word)
    requirement_tokens = re.findall(r"[a-z0-9]+", normalize_text(requirement or ""))
    matches = []

    for label in _labels(control):
        label_tokens = label.split()
        if not label_tokens or label_tokens[0] not in action_forms:
            continue
        if not _tokens_are_ordered_subsequence(label_tokens, requirement_tokens):
            continue
        matches.append(
            _ControlMatch(
                specificity=(len(label_tokens), len(label)),
                position=action_match.start(1),
                label=label,
                kind_priority=1,
            )
        )

    input_type = control.element.get("input_type", "").casefold()
    form_phrase = _form_identity_phrase(control.element.get("form_action", ""))
    if (
        "submit" in action_forms
        and input_type == "submit"
        and form_phrase
        and re.search(
            rf"(?<![a-z0-9]){re.escape(form_phrase)}(?![a-z0-9])",
            _phrase(requirement),
        )
    ):
        label = max(_labels(control), key=lambda value: (len(value.split()), len(value)), default="submit")
        matches.append(
            _ControlMatch(
                specificity=(len(label.split()), len(label)),
                position=action_match.start(1),
                label=label,
                kind_priority=2,
            )
        )

    if not matches:
        return None
    return min(
        matches,
        key=lambda item: (
            item.kind_priority,
            -item.specificity[0],
            -item.specificity[1],
            item.label,
        ),
    )


def _literal_label_is_explicit(requirement: str, control: UiElement, normalized_label: str) -> bool:
    """Avoid incidental matches such as `Search` in `search results`.

    Multiword labels remain case-insensitive. A one-word UI label is accepted only
    when the same written form occurs in the specification. This deliberately
    favors missing context over attaching a generic control to the wrong step.
    """
    raw_labels = (
        written_label
        for label, written_label in _label_variants(control)
        if label == normalized_label
    )
    if len(normalized_label.split()) > 1:
        return any(
            _multiword_label_is_explicit(requirement, raw_label)
            for raw_label in raw_labels
            if raw_label
        )
    return any(
        re.search(rf"(?<![A-Za-z0-9]){re.escape(raw_label)}(?![A-Za-z0-9])", requirement) is not None
        or _case_insensitive_ui_reference(requirement, raw_label)
        for raw_label in raw_labels
        if raw_label
    )


def _case_insensitive_ui_reference(requirement: str, raw_label: str) -> bool:
    """Accept `email field` while rejecting incidental text such as `search results`."""
    return re.search(
        rf"(?<![A-Za-z0-9]){re.escape(raw_label)}(?![A-Za-z0-9])"
        r"\s+(?:field|input|textbox|button|link|menu|option|checkbox|radio|control)\b",
        requirement or "",
        flags=re.IGNORECASE,
    ) is not None


def _multiword_label_is_explicit(requirement: str, raw_label: str) -> bool:
    boundary_pattern = rf"(?<![A-Za-z0-9]){re.escape(raw_label)}(?![A-Za-z0-9])"
    if re.search(boundary_pattern, requirement) is not None:
        return True
    for match in re.finditer(boundary_pattern, requirement, flags=re.IGNORECASE):
        previous = re.search(r"([A-Za-z0-9]+)\s*$", requirement[:match.start()])
        # `Shopping cart` in `Update shopping cart` is not the explicitly named
        # control. A normal lowercase article/preposition does not block a match.
        if previous is not None and previous.group(1)[:1].isupper():
            continue
        return True
    return False


def _normalized_phrase_position(requirement: str, normalized_label: str) -> int:
    normalized_requirement = _phrase(requirement)
    match = re.search(
        rf"(?<![a-z0-9]){re.escape(normalized_label)}(?![a-z0-9])",
        normalized_requirement,
    )
    return match.start() if match is not None else len(normalized_requirement)


def _word_base_forms(word: str) -> set[str]:
    word = _phrase(word)
    if not word:
        return set()
    forms = {word}
    if len(word) > 4 and word.endswith("ies"):
        forms.add(word[:-3] + "y")
    if len(word) > 4 and word.endswith("es"):
        forms.add(word[:-2])
    if len(word) > 3 and word.endswith("s"):
        forms.add(word[:-1])
    if len(word) > 4 and word.endswith("ed"):
        forms.add(word[:-2])
    if len(word) > 5 and word.endswith("ing"):
        forms.add(word[:-3])
    return forms


def _tokens_are_ordered_subsequence(expected: list[str], actual: list[str]) -> bool:
    if not expected:
        return False
    expected_index = 0
    for token in actual:
        expected_token = expected[expected_index]
        if expected_token in _word_base_forms(token):
            expected_index += 1
            if expected_index == len(expected):
                return True
    return False


def _form_identity_phrase(form_action: str) -> str:
    path = urlsplit(form_action or "").path.strip("/")
    return _phrase(path.replace("-", " "))


def _labels(control: UiElement) -> list[str]:
    labels = []
    for value, _ in _label_variants(control):
        if len(value) >= 2 and value not in labels:
            labels.append(value)
    return labels


def _label_variants(control: UiElement) -> list[tuple[str, str]]:
    variants = []
    for field in _LABEL_FIELDS:
        raw_value = _written_label(control.element.get(field, ""))
        normalized = _phrase(raw_value)
        if normalized and (normalized, raw_value) not in variants:
            variants.append((normalized, raw_value))
    for field in ("id", "name"):
        readable = _readable_identifier(control.element.get(field, ""))
        normalized = _phrase(readable)
        if normalized and (normalized, readable) not in variants:
            variants.append((normalized, readable))
    return variants


def _written_label(value: str) -> str:
    without_counter = _DYNAMIC_COUNTER.sub("", value or "").strip()
    return _TRAILING_LABEL_PUNCTUATION.sub("", without_counter).strip()


def _readable_identifier(value: str) -> str:
    identifier = (value or "").strip()
    if not identifier or len(identifier) < 2:
        return ""
    separated = _CAMEL_ACRONYM_BOUNDARY.sub(r"\1 \2", identifier)
    separated = _CAMEL_WORD_BOUNDARY.sub(r"\1 \2", separated)
    separated = _IDENTIFIER_SEPARATOR.sub(" ", separated)
    separated = _TRAILING_IDENTIFIER_NUMBER.sub("", separated)
    readable = " ".join(separated.split()).strip()
    if not readable or not re.search(r"[A-Za-z]{2,}", readable):
        return ""
    return readable


def _matched_candidates_in_scope(
    candidates: list[_Candidate],
    requirement: str,
    scope_urls: list[str],
) -> list[_MatchedCandidate]:
    matches = []
    for candidate in candidates:
        if best_selector_for(candidate.control) is None:
            continue
        if not _candidate_is_in_scope(candidate, scope_urls):
            continue
        if not _radio_option_is_explicit(requirement, candidate.control):
            continue
        control_match = _match_control(requirement, candidate.control)
        if control_match is not None:
            matches.append(_MatchedCandidate(candidate, control_match))
    return matches


def _radio_option_is_explicit(requirement: str, control: UiElement) -> bool:
    """Do not choose an arbitrary radio value from a group-only reference."""
    if (
        control.kind != "radio"
        and control.element.get("input_type", "").casefold() != "radio"
    ):
        return True

    group_name = _phrase(control.element.get("name", ""))
    for field in ("label", "text", "value", "aria_label", "title"):
        written_option = _written_label(control.element.get(field, ""))
        normalized_option = _phrase(written_option)
        if (
            len(normalized_option) < 2
            or normalized_option == group_name
        ):
            continue
        if re.search(
            rf"(?<![A-Za-z0-9]){re.escape(written_option)}(?![A-Za-z0-9])",
            requirement or "",
            flags=re.IGNORECASE,
        ):
            return True
    return False


def _select_distinct_candidates(
    matches: list[_MatchedCandidate],
    current_page_url: str,
    scope_urls: list[str],
) -> list[_MatchedCandidate]:
    by_label: dict[str, list[_MatchedCandidate]] = {}
    for item in matches:
        by_label.setdefault(_label_group_key(item.match.label), []).append(item)

    selected = [
        min(
            group,
            key=lambda item: _matched_selection_key(item, current_page_url, scope_urls),
        )
        for group in by_label.values()
    ]
    selected.sort(key=lambda item: _interaction_order_key(item, scope_urls))
    return selected[:_MAX_INTERACTIONS_PER_STEP]


def _label_group_key(label: str) -> str:
    tokens = label.split()
    if len(tokens) != 1:
        return label
    return min(_word_base_forms(tokens[0]), key=lambda value: (len(value), value))


def _remove_incidental_links(
    selected: list[_MatchedCandidate],
    requirement: str,
) -> list[_MatchedCandidate]:
    """Discard generic links that merely repeat an object named in the step.

    Product tags such as ``book`` and ``digital`` are legitimate controls in the
    graph, but mentioning those words does not necessarily ask the user to follow
    those links. Two deterministic rules keep the selector conservative:

    * a link whose label is a strict subset of a more specific selected label is
      discarded (``book`` versus ``Health Book`` and ``Register`` versus
      ``Register button``);
    * when the step already contains a local non-link interaction, an unrelated
      one-word link is retained only if the step also expresses page-entry intent.

    Routes are deliberately not consulted by either rule.
    """
    if len(selected) < 2:
        return selected

    label_tokens = {
        id(item): _canonical_label_tokens(item.match.label)
        for item in selected
    }
    filtered = []
    for item in selected:
        if item.candidate.control.kind not in {"link", "anchor"}:
            filtered.append(item)
            continue
        tokens = label_tokens[id(item)]
        is_strict_subset = any(
            tokens
            and len(tokens) < len(other_tokens)
            and _tokens_are_ordered_subsequence(tokens, other_tokens)
            for other in selected
            if other is not item
            for other_tokens in (label_tokens[id(other)],)
        )
        if not is_strict_subset:
            filtered.append(item)

    has_local_interaction = any(
        item.candidate.control.kind not in {"link", "anchor"}
        for item in filtered
    )
    if has_local_interaction and not _contains_page_entry_action(requirement):
        filtered = [
            item
            for item in filtered
            if item.candidate.control.kind not in {"link", "anchor"}
            or len(_canonical_label_tokens(item.match.label)) > 1
        ]
    return filtered


def _canonical_label_tokens(label: str) -> list[str]:
    return [
        min(_word_base_forms(token), key=lambda value: (len(value), value))
        for token in label.split()
    ]


def _matched_selection_key(
    item: _MatchedCandidate,
    current_page_url: str,
    scope_urls: list[str],
) -> tuple[object, ...]:
    page_url = item.candidate.control.page_url
    return (
        0 if _same_location(page_url, current_page_url) else 1,
        _location_position(page_url, scope_urls),
        item.match.kind_priority,
        selector_priority_for(item.candidate.control),
        -item.match.specificity[0],
        -item.match.specificity[1],
        _candidate_identity(item.candidate),
    )


def _interaction_order_key(
    item: _MatchedCandidate,
    scope_urls: list[str],
) -> tuple[object, ...]:
    operation_priority = {
        "fill": 0,
        "selectOption": 1,
        "check": 2,
        "click": 3,
    }
    return (
        item.match.position,
        _location_position(item.candidate.control.page_url, scope_urls),
        operation_priority.get(item.candidate.control.suggested_operation, 4),
        item.match.kind_priority,
        _candidate_identity(item.candidate),
    )


def _include_unique_form_companion(
    selected: list[_MatchedCandidate],
    candidates: list[_Candidate],
    requirement: str,
    scope_urls: list[str],
    current_page_url: str,
) -> list[_MatchedCandidate]:
    if len(selected) >= _MAX_INTERACTIONS_PER_STEP:
        return selected
    selected_identities = {_candidate_identity(item.candidate) for item in selected}
    additions = []

    for item in selected:
        element = item.candidate.control.element
        if item.match.kind_priority != 1 or element.get("input_type", "").casefold() != "submit":
            continue
        form_action = element.get("form_action", "")
        form_method = element.get("form_method", "")
        if not form_action:
            continue
        companions = [
            candidate
            for candidate in candidates
            if candidate.control.kind == "text_input"
            if _same_location(candidate.control.page_url, item.candidate.control.page_url)
            if candidate.control.element.get("form_action", "") == form_action
            if candidate.control.element.get("form_method", "") == form_method
            if best_selector_for(candidate.control) is not None
            if _candidate_identity(candidate) not in selected_identities
            if _candidate_is_in_scope(candidate, scope_urls)
        ]
        unique_companions = {
            _candidate_identity(candidate): candidate
            for candidate in companions
        }
        if len(unique_companions) != 1:
            continue
        companion = next(iter(unique_companions.values()))
        label = max(
            _labels(companion.control),
            key=lambda value: (len(value.split()), len(value)),
            default="form input",
        )
        additions.append(
            _MatchedCandidate(
                candidate=companion,
                match=_ControlMatch(
                    specificity=(len(label.split()), len(label)),
                    position=item.match.position,
                    label=f"form:{label}",
                    kind_priority=3,
                ),
            )
        )
        selected_identities.add(_candidate_identity(companion))

    combined = [*selected, *additions]
    combined.sort(key=lambda item: _interaction_order_key(item, scope_urls))
    return combined[:_MAX_INTERACTIONS_PER_STEP]


def _interaction_context(
    item: _MatchedCandidate,
    page_evidence: PageEvidence | None,
) -> InteractionContext:
    control = item.candidate.control
    observed_result = item.candidate.transition.observed_result if item.candidate.transition else None
    if (
        observed_result is not None
        and page_evidence is not None
        and normalize_text(observed_result.text) == normalize_text(page_evidence.text)
    ):
        observed_result = None
    return InteractionContext(
        control=ContextElement(
            page_url=control.page_url,
            action=control.suggested_operation,
            interaction_kind=control.kind,
            element=_compact_element(control.element),
            selector=best_selector_for(control),
            destination_url=(
                item.candidate.destination_url
                if control.suggested_operation == "click"
                else ""
            ),
        ),
        observed_result=observed_result,
    )


def _page_evidence_for_action(
    pages: list[PageNode],
    requirement: str,
    verification_step: bool,
    current_page_url: str,
    selected: list[_MatchedCandidate],
    page_matches: list[_PageMatch],
) -> PageEvidence | None:
    if verification_step:
        evidence_urls = _unique_locations(
            [
                *(
                    item.candidate.destination_url
                    for item in reversed(selected)
                    if item.candidate.destination_url
                ),
                *(page_match.page.url for page_match in reversed(page_matches)),
                current_page_url,
            ]
        )
        return _select_page_evidence(pages, evidence_urls, requirement)
    if _contains_page_entry_action(requirement) and page_matches:
        authoritative_destination = _last_authoritative_destination(selected)
        if authoritative_destination:
            matching_destination = [
                page_match
                for page_match in page_matches
                if _same_location(page_match.page.url, authoritative_destination)
            ]
            return (
                max(matching_destination, key=lambda item: item.position).evidence
                if matching_destination
                else None
            )
        return max(page_matches, key=lambda item: item.position).evidence
    return None


def _next_page_url(
    current_page_url: str,
    requirement: str,
    selected: list[_MatchedCandidate],
    page_matches: list[_PageMatch],
) -> str:
    next_page_url = current_page_url
    authoritative_destination = ""
    for item in selected:
        if (
            item.candidate.control.suggested_operation == "click"
            and item.candidate.destination_url
        ):
            next_page_url = item.candidate.destination_url
            if _candidate_has_authoritative_destination(item.candidate):
                authoritative_destination = item.candidate.destination_url

    selected_source_urls = _unique_locations(
        [item.candidate.control.page_url for item in selected]
    )
    if (
        not authoritative_destination
        and selected_source_urls
        and not any(_same_location(current_page_url, url) for url in selected_source_urls)
        and len(selected_source_urls) == 1
    ):
        next_page_url = selected_source_urls[0]

    if (
        not authoritative_destination
        and _contains_page_entry_action(requirement)
        and page_matches
    ):
        next_page_url = max(page_matches, key=lambda item: item.position).page.url
    return next_page_url


def _last_authoritative_destination(selected: list[_MatchedCandidate]) -> str:
    destination = ""
    for item in selected:
        if _candidate_has_authoritative_destination(item.candidate):
            destination = item.candidate.destination_url
    return destination


def _candidate_has_authoritative_destination(candidate: _Candidate) -> bool:
    return bool(
        candidate.destination_url
        and (
            candidate.transition is not None
            and candidate.transition.target.get("url")
            or candidate.control.element.get("href")
        )
    )


def _contains_page_entry_action(requirement: str) -> bool:
    return any(
        _word_base_forms(token) & _PAGE_ENTRY_ACTIONS
        for token in re.findall(r"[A-Za-z]+", requirement or "")
    )


def _matching_pages(pages: list[PageNode], requirement: str) -> list[_PageMatch]:
    raw_matches = []
    for page in pages:
        for candidate in _page_evidence_candidates(page, requirement):
            if candidate.evidence.source not in {"h1", "title"}:
                continue
            raw_matches.append(
                _PageMatch(
                    page=page,
                    evidence=candidate.evidence,
                    specificity=candidate.specificity,
                    position=_normalized_phrase_position(requirement, _phrase(candidate.evidence.text)),
                )
            )

    locations_by_text: dict[str, set[str]] = {}
    for item in raw_matches:
        locations_by_text.setdefault(_phrase(item.evidence.text), set()).add(_location_key(item.page.url))

    unique_matches = [
        item
        for item in raw_matches
        if len(locations_by_text[_phrase(item.evidence.text)]) == 1
    ]
    by_location: dict[str, list[_PageMatch]] = {}
    for item in unique_matches:
        by_location.setdefault(_location_key(item.page.url), []).append(item)
    selected = [
        min(
            group,
            key=lambda item: (
                item.position,
                0 if item.evidence.source == "h1" else 1,
                -item.specificity[0],
                -item.specificity[1],
            ),
        )
        for group in by_location.values()
    ]
    return sorted(selected, key=lambda item: (item.position, item.page.url))


def _page_matches_supported_by_next_interaction(
    pages: list[PageNode],
    candidates: list[_Candidate],
    page_entry_requirement: str,
    next_requirement: str,
) -> list[_PageMatch]:
    """Resolve an underspecified page only when the following action disambiguates it.

    A step such as ``opens a Camera product`` does not contain the complete H1,
    but the next step may name a control that exists on only one matching page.
    This is a deterministic look-ahead over observed artifacts: no route is
    synthesized and ambiguous destinations remain without context.
    """
    if not next_requirement:
        return []

    control_page_urls = _unique_locations(
        [
            candidate.control.page_url
            for candidate in candidates
            if best_selector_for(candidate.control) is not None
            and _match_control(next_requirement, candidate.control) is not None
        ]
    )
    matches = []
    for page in pages:
        if not any(_same_location(page.url, url) for url in control_page_urls):
            continue
        evidence = _partially_matching_page_evidence(page, page_entry_requirement)
        if evidence is not None:
            matches.append(evidence)

    locations = {_location_key(item.page.url) for item in matches}
    return matches if len(locations) == 1 else []


def _partially_matching_page_evidence(
    page: PageNode,
    requirement: str,
) -> _PageMatch | None:
    requirement_tokens = {
        token.casefold(): match.start()
        for match in re.finditer(r"[A-Za-z0-9]+", requirement or "")
        for token in (match.group(0),)
        if len(token) >= 3
    }
    candidates = []
    for source_priority, (source, value) in enumerate((("h1", page.h1), ("title", page.title))):
        text = " ".join((value or "").split()).strip()
        if not text or len(text) > _MAX_PAGE_EVIDENCE_LENGTH:
            continue
        shared = [
            token
            for token in re.findall(r"[A-Za-z0-9]+", text)
            if token.casefold() in requirement_tokens and len(token) >= 3
        ]
        if not shared:
            continue
        normalized_shared = " ".join(token.casefold() for token in shared)
        candidates.append(
            (
                source_priority,
                _PageMatch(
                    page=page,
                    evidence=PageEvidence(page_url=page.url, source=source, text=text),
                    specificity=(len(shared), len(normalized_shared)),
                    position=min(requirement_tokens[token.casefold()] for token in shared),
                ),
            )
        )
    if not candidates:
        return None
    return min(
        candidates,
        key=lambda item: (
            item[0],
            -item[1].specificity[0],
            -item[1].specificity[1],
        ),
    )[1]


def _select_page_evidence(
    pages: list[PageNode],
    page_urls: list[str],
    requirement: str,
) -> PageEvidence | None:
    candidates = []
    for page_priority, page_url in enumerate(page_urls):
        for page in pages:
            if not _same_location(page.url, page_url):
                continue
            candidates.extend(
                (page_priority, candidate)
                for candidate in _page_evidence_candidates(page, requirement)
            )
    if not candidates:
        return None
    _, selected = min(
        candidates,
        key=lambda item: (
            item[0],
            item[1].source_priority,
            -item[1].specificity[0],
            -item[1].specificity[1],
            item[1].evidence.text.casefold(),
        ),
    )
    return selected.evidence


def _page_evidence_candidates(page: PageNode, requirement: str) -> list[_EvidenceCandidate]:
    requirement_phrase = _phrase(requirement)
    padded_requirement = f" {requirement_phrase} "
    candidates = []
    for source_priority, (source, value) in enumerate((("h1", page.h1), ("title", page.title))):
        text = " ".join((value or "").split()).strip()
        phrase = _phrase(text)
        if (
            phrase
            and len(text) <= _MAX_PAGE_EVIDENCE_LENGTH
            and f" {phrase} " in padded_requirement
            and _page_field_is_explicit(requirement, text, phrase)
        ):
            candidates.append(
                _EvidenceCandidate(
                    evidence=PageEvidence(page_url=page.url, source=source, text=text),
                    specificity=(len(phrase.split()), len(phrase)),
                    source_priority=source_priority,
                )
            )

    excerpt_match = _longest_literal_excerpt_match(requirement, page.visible_text_excerpt)
    if excerpt_match:
        phrase = _phrase(excerpt_match)
        candidates.append(
            _EvidenceCandidate(
                evidence=PageEvidence(page_url=page.url, source="visible_text_excerpt", text=excerpt_match),
                specificity=(len(phrase.split()), len(phrase)),
                source_priority=2,
            )
        )
    return candidates


def _page_field_is_explicit(requirement: str, text: str, normalized_text: str) -> bool:
    if len(normalized_text.split()) > 1:
        return True
    written_text = _written_label(text)
    return bool(
        written_text
        and re.search(
            rf"(?<![A-Za-z0-9]){re.escape(written_text)}(?![A-Za-z0-9])",
            requirement,
        )
    )


def _longest_literal_excerpt_match(requirement: str, excerpt: str) -> str:
    """Extract an exact short span; the complete diagnostic excerpt is never sent."""
    excerpt = " ".join((excerpt or "").split()).strip()
    requirement_tokens = re.findall(r"[A-Za-z0-9]+", requirement or "")
    if not excerpt or len(requirement_tokens) < _MIN_EXCERPT_EVIDENCE_WORDS:
        return ""

    for size in range(len(requirement_tokens), _MIN_EXCERPT_EVIDENCE_WORDS - 1, -1):
        for start in range(0, len(requirement_tokens) - size + 1):
            tokens = requirement_tokens[start:start + size]
            if len(" ".join(tokens)) > _MAX_PAGE_EVIDENCE_LENGTH:
                continue
            pattern = r"(?<![A-Za-z0-9])" + r"[^A-Za-z0-9]+".join(
                re.escape(token) for token in tokens
            ) + r"(?![A-Za-z0-9])"
            match = re.search(pattern, excerpt, flags=re.IGNORECASE)
            if match is None:
                continue
            observed_span = match.group(0).strip()
            if _phrase(observed_span) == _phrase(excerpt):
                return ""
            return observed_span
    return ""


def _is_verification_step(requirement: str) -> bool:
    return bool(
        _VERIFICATION_SUBJECT.search(requirement or "")
        or _VERIFICATION_EXPRESSION.search(requirement or "")
    )


def _is_pure_verification_step(requirement: str) -> bool:
    """Return true only when verification is the leading intent of the step."""
    return bool(
        _VERIFICATION_SUBJECT.search(requirement or "")
        or _LEADING_USER_VERIFICATION.search(requirement or "")
    )


def _candidate_is_in_scope(candidate: _Candidate, scope_urls: list[str]) -> bool:
    """Use the active page and pages explicitly identified by their UI evidence."""
    return any(
        _same_location(candidate.control.page_url, page_url)
        for page_url in scope_urls
    )


def _unique_locations(urls: list[str]) -> list[str]:
    unique = []
    seen = set()
    for url in urls:
        if not url:
            continue
        location = _location_key(url)
        if location in seen:
            continue
        seen.add(location)
        unique.append(url)
    return unique


def _location_position(url: str, scope_urls: list[str]) -> int:
    for index, scope_url in enumerate(scope_urls):
        if _same_location(url, scope_url):
            return index
    return len(scope_urls)


def _candidate_identity(candidate: _Candidate) -> tuple[str, ...]:
    element = candidate.control.element
    return (
        _location_key(candidate.control.page_url),
        element.get("tag", "").casefold(),
        element.get("id", "").casefold(),
        element.get("name", "").casefold(),
        element.get("href", "").casefold(),
        _phrase(element.get("text") or element.get("value") or element.get("label") or ""),
    )


def _has_comparable_label(control: UiElement) -> bool:
    return bool(_labels(control))


def _compact_element(element: dict[str, str]) -> dict[str, str]:
    allowed = (
        "tag", "text", "title", "label", "data_testid", "id", "name", "input_type",
        "value", "href", "role", "aria_label", "placeholder", "form_action", "form_method",
    )
    compact = {key: element[key] for key in allowed if element.get(key)}
    if "text" in compact:
        compact["text"] = _DYNAMIC_COUNTER.sub("", compact["text"]).strip()
    return compact


def _kind_from_element(element: dict[str, str]) -> str:
    tag = element.get("tag", "").casefold()
    input_type = element.get("input_type", "").casefold()
    if tag in {"textarea"} or (tag == "input" and input_type in {"", "text", "search", "email", "number"}):
        return "text_input"
    if tag == "select":
        return "select"
    if input_type in {"checkbox", "radio"}:
        return input_type
    if tag == "a":
        return "link"
    if tag == "button" or input_type in {"button", "submit"}:
        return "button"
    return "control"


def _operation_for(kind: str) -> str:
    if kind == "text_input":
        return "fill"
    if kind == "select":
        return "selectOption"
    if kind in {"checkbox", "radio"}:
        return "check"
    if kind in {"link", "anchor", "button", "button_like"}:
        return "click"
    return "interact"


def _phrase(value: str) -> str:
    without_counter = _DYNAMIC_COUNTER.sub("", normalize_text(value or "")).strip()
    return " ".join(re.findall(r"[a-z0-9]+", without_counter))


def _same_location(first: str, second: str) -> bool:
    return _location_key(first) == _location_key(second)


def _location_key(value: str) -> str:
    parsed = urlsplit((value or "").rstrip("/"))
    return f"{parsed.scheme.casefold()}://{parsed.netloc.casefold()}{parsed.path.rstrip('/')}"
