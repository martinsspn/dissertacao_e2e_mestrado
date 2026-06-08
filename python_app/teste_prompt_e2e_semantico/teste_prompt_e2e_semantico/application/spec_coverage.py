from __future__ import annotations

from dataclasses import dataclass
import re

from teste_prompt_e2e_semantico.application.text_normalization import matching_terms, normalize_spec, normalize_text
from teste_prompt_e2e_semantico.domain.models import (
    CoverageEvidence,
    PathCandidate,
    RequirementCoverage,
    RequirementFacet,
    ScoredPage,
    ScoredTransition,
    SpecCoverageReport,
    SpecPlan,
)


_GENERIC_TERMS = {
    "acessa",
    "acessar",
    "aberta",
    "abrir",
    "adicionar",
    "area",
    "ate",
    "botao",
    "campo",
    "clica",
    "clicar",
    "corretamente",
    "dados",
    "depois",
    "detalhes",
    "deve",
    "digitando-a",
    "disponivel",
    "disponiveis",
    "exibe",
    "exibida",
    "ficou",
    "fluxo",
    "foi",
    "formulario",
    "item",
    "itens",
    "link",
    "lista",
    "localiza",
    "menu",
    "navega",
    "navegar",
    "novamente",
    "pagina",
    "partir",
    "preenche",
    "produto",
    "sistema",
    "usuario",
    "valida",
    "validar",
    "verifica",
    "verificar",
    "visivel",
    "visualizar",
}

_SPLIT_CONNECTORS = re.compile(
    r"\s+e\s+(?=(?:acessar|abrir|adicionar|clicar|clica|confirmar|confirma|localizar|localiza|"
    r"navegar|navega|preencher|preenche|validar|verificar|visualizar)\b)",
    re.IGNORECASE,
)

_TERM_SYNONYMS = {
    "adicionado": ["added"],
    "automaticamente": ["automatically"],
    "cartao": ["card", "cards"],
    "carrinho": ["cart", "shopping"],
    "catalogo": ["catalog", "category"],
    "categoria": ["category"],
    "comparacao": ["compare", "comparison", "compareproducts"],
    "compras": ["shopping", "cart"],
    "computadores": ["computers"],
    "contato": ["contact", "contactus"],
    "descricao": ["description"],
    "digitais": ["digital"],
    "dolares": ["dollars"],
    "livro": ["book", "books"],
    "livros": ["books", "book"],
    "nome": ["name"],
    "notificacao": ["notification", "bar"],
    "opcoes": ["options"],
    "preco": ["price"],
    "presente": ["gift"],
    "primeiro": ["first"],
    "quantidade": ["quantity", "qty"],
    "registro": ["register", "registration"],
    "registra": ["register", "registration"],
    "senha": ["password"],
    "sobrenome": ["last", "name"],
    "sucesso": ["success", "successful"],
    "valido": ["valid"],
}

_ACTION_FACETS = {
    "click": {
        "triggers": ["clica", "clicar", "seleciona", "selecionar"],
        "terms": ["click", "select"],
        "weight": 1.15,
    },
    "fill": {
        "triggers": ["digita", "digitar", "informa", "informar", "preenche", "preencher"],
        "terms": ["fill", "input", "type"],
        "weight": 1.25,
    },
    "add": {
        "triggers": ["adiciona", "adicionar", "inclui", "incluir"],
        "terms": ["add", "cart"],
        "weight": 1.35,
    },
    "remove": {
        "triggers": ["exclui", "excluir", "remove", "remover"],
        "terms": ["delete", "remove"],
        "weight": 1.35,
    },
    "confirm": {
        "triggers": ["confirma", "confirmar", "conclui", "concluir", "finaliza", "finalizar"],
        "terms": ["checkout", "confirm", "continue", "submit"],
        "weight": 1.25,
    },
    "assertion": {
        "triggers": ["exibe", "exibir", "valida", "validar", "verifica", "verificar"],
        "terms": ["display", "visible"],
        "weight": 1.2,
    },
    "search": {
        "triggers": ["busca", "buscar", "localiza", "localizar", "procura", "procurar"],
        "terms": ["find", "search"],
        "weight": 1.15,
    },
    "register": {
        "triggers": ["cadastra", "cadastrar", "registra", "registrar"],
        "terms": ["register", "registration"],
        "weight": 1.35,
    },
    "compare": {
        "triggers": ["compara", "comparar"],
        "terms": ["compare", "comparison", "compareproducts"],
        "weight": 1.25,
    },
    "navigation": {
        "triggers": ["acessa", "acessar", "abrir", "navega", "navegar", "visita", "visitar", "visualizar"],
        "terms": ["click", "href", "navigate", "open"],
        "weight": 1.0,
    },
}

_TARGET_HINTS = {
    "area",
    "categoria",
    "category",
    "menu",
    "pagina",
    "secao",
    "tela",
}

_DATA_HINTS = {
    "email",
    "nome",
    "password",
    "preco",
    "quantidade",
    "qty",
    "senha",
    "sobrenome",
    "valor",
}

_AMBIGUITY_HINTS = {
    "anterior",
    "confirmar",
    "continuar",
    "concluir",
    "dados",
    "novamente",
    "processo",
}

_CRITICAL_FACETS = {"object", "target_state", "assertion", "data_binding"}

_CONTRADICTORY_ACTIONS = {
    "add": {"delete", "remove", "removed"},
    "remove": {"add", "added"},
    "register": {"login", "signin", "sign in"},
}


@dataclass(frozen=True)
class _AlignmentResult:
    status: str
    fit_score: float
    support_type: str
    alignment_cost: float
    unsupported_facets: list[str]


def analyze_spec_coverage(
    spec: SpecPlan,
    pages: list[ScoredPage],
    transitions: list[ScoredTransition],
    paths: list[PathCandidate],
) -> SpecCoverageReport:
    requirements = [
        _analyze_requirement(requirement, pages, transitions, paths)
        for requirement in _extract_requirements(spec.raw_text)
    ]
    requirements = [coverage for coverage in requirements if coverage.terms]

    if not requirements:
        requirements = [
            _analyze_requirement(spec.raw_text, pages, transitions, paths),
        ]

    supported = sum(1 for item in requirements if item.status == "supported")
    partial = sum(1 for item in requirements if item.status == "partial")
    missing = sum(1 for item in requirements if item.status == "missing")
    score = sum(item.fit_score for item in requirements) / max(1, len(requirements))

    warnings: list[str] = []
    if missing:
        warnings.append("Ha requisitos sem evidencia concreta no grafo; alto risco de alucinacao se forem exigidos no teste.")
    if partial:
        warnings.append("Ha requisitos parcialmente cobertos; use apenas paginas/transicoes evidenciadas.")
    if not paths:
        warnings.append("Nenhum caminho candidato foi encontrado para esta especificacao.")

    return SpecCoverageReport(
        overall_status=_overall_status(score, partial, missing),
        coverage_score=round(score, 3),
        supported_requirements=supported,
        partial_requirements=partial,
        missing_requirements=missing,
        requirements=requirements,
        warnings=warnings,
    )


def _extract_requirements(raw_text: str) -> list[str]:
    requirements: list[str] = []
    for line in raw_text.splitlines():
        line = line.strip(" -\t")
        if not line or line.endswith(":"):
            continue
        for sentence in re.split(r"(?<=[.!?])\s+", line):
            sentence = sentence.strip(" .;")
            if not sentence:
                continue
            parts = _SPLIT_CONNECTORS.split(sentence)
            # re.split keeps connector verbs because of the lookahead group.
            rebuilt: list[str] = []
            index = 0
            while index < len(parts):
                part = parts[index].strip(" ,;")
                if part:
                    rebuilt.append(part)
                index += 1
            requirements.extend(rebuilt)
    return _dedupe(requirements)


def _analyze_requirement(
    text: str,
    pages: list[ScoredPage],
    transitions: list[ScoredTransition],
    paths: list[PathCandidate],
) -> RequirementCoverage:
    facets = _extract_facets(text)
    terms = _dedupe([term for facet in facets for term in facet.terms])
    if not terms:
        terms = _coverage_terms(text)
    evidence = _collect_evidence(terms, pages, transitions, paths)
    alignment = _align_facets(text, facets, evidence)
    confidence = max(alignment.fit_score, evidence[0].score if evidence else 0.0)
    return RequirementCoverage(
        text=text,
        terms=terms,
        facets=facets,
        status=alignment.status,
        confidence=round(confidence, 3),
        fit_score=alignment.fit_score,
        support_type=alignment.support_type,
        alignment_cost=alignment.alignment_cost,
        unsupported_facets=alignment.unsupported_facets,
        evidence=evidence[:4],
        warning=_warning_for_status(alignment.status),
    )


def _coverage_terms(text: str) -> list[str]:
    raw_terms = normalize_spec(text).terms
    terms = [term for term in raw_terms if term not in _GENERIC_TERMS]
    expanded: list[str] = []
    for term in terms:
        expanded.append(term)
        expanded.extend(_TERM_SYNONYMS.get(term, []))
    return _dedupe(expanded)


def _extract_facets(text: str) -> list[RequirementFacet]:
    terms = _coverage_terms(text)
    facets: list[RequirementFacet] = []
    action = _action_facet(text)

    object_terms = _object_terms(terms, action)
    if action is not None and (object_terms or action.text == "assertion"):
        facets.append(action)

    if object_terms:
        facets.append(RequirementFacet("object", " ".join(object_terms[:4]), object_terms, 1.5))

    if _has_target_hint(text) and object_terms:
        facets.append(RequirementFacet("target_state", " ".join(object_terms[:4]), object_terms, 1.3))

    if _is_assertion_requirement(text):
        assertion_terms = object_terms or terms
        facets.append(RequirementFacet("assertion", "estado observavel esperado", assertion_terms, 1.25))

    data_terms = [term for term in terms if term in _DATA_HINTS or _looks_like_data_term(term)]
    if data_terms:
        facets.append(RequirementFacet("data_binding", " ".join(data_terms), data_terms, 0.9))

    if not facets and terms:
        facets.append(RequirementFacet("object", " ".join(terms[:4]), terms, 1.0))

    return facets


def _action_facet(text: str) -> RequirementFacet | None:
    normalized = normalize_text(text)
    for action, config in _ACTION_FACETS.items():
        triggers = config["triggers"]
        if any(re.search(rf"\b{re.escape(trigger)}\b", normalized) for trigger in triggers):
            terms = list(config["terms"])
            return RequirementFacet("action", action, terms, float(config["weight"]))
    return None


def _object_terms(terms: list[str], action: RequirementFacet | None) -> list[str]:
    action_terms = set(action.terms if action else [])
    return [term for term in terms if term not in action_terms and not _is_target_hint_term(term)]


def _has_target_hint(text: str) -> bool:
    normalized_terms = set(normalize_spec(text).terms)
    return bool(normalized_terms.intersection(_TARGET_HINTS))


def _looks_like_data_term(term: str) -> bool:
    return bool(re.search(r"\d", term)) or "@" in term or term.startswith("$")


def _is_target_hint_term(term: str) -> bool:
    if term in _TARGET_HINTS:
        return True
    return any(term in synonyms for hint, synonyms in _TERM_SYNONYMS.items() if hint in _TARGET_HINTS)


def _collect_evidence(
    terms: list[str],
    pages: list[ScoredPage],
    transitions: list[ScoredTransition],
    paths: list[PathCandidate],
) -> list[CoverageEvidence]:
    evidence: list[CoverageEvidence] = []
    evidence.extend(_page_evidence(terms, pages))
    evidence.extend(_transition_evidence(terms, transitions))
    evidence.extend(_path_evidence(terms, paths))
    evidence.sort(key=lambda item: item.score, reverse=True)
    return [item for item in evidence if item.score >= 0.25]


def _page_evidence(terms: list[str], pages: list[ScoredPage]) -> list[CoverageEvidence]:
    items: list[CoverageEvidence] = []
    for scored in pages:
        page = scored.page
        strong_text = " ".join([page.url, page.title, page.h1])
        weak_text = page.visible_text_excerpt
        strong_matches = matching_terms(terms, strong_text)
        weak_matches = matching_terms(terms, weak_text)
        score = _weighted_score(terms, strong_matches, weak_matches, 0.8, 0.35)
        if score <= 0:
            continue
        items.append(
            CoverageEvidence(
                kind="page",
                label=page.h1 or page.title or page.url,
                score=round(score, 3),
                details={
                    "url": page.url,
                    "matched_terms": sorted(set(strong_matches + weak_matches)),
                    "support_type": "indirect",
                    "justification": "Pagina contem termos da faceta; use como evidencia de estado observavel.",
                },
            )
        )
    return items


def _transition_evidence(terms: list[str], transitions: list[ScoredTransition]) -> list[CoverageEvidence]:
    items: list[CoverageEvidence] = []
    for scored in transitions:
        transition = scored.transition
        element = transition.element
        strong_text = " ".join(
            [
                element.get("text", ""),
                element.get("aria_label", ""),
                element.get("href", ""),
                transition.target.get("url", ""),
                transition.target.get("title", ""),
            ]
        )
        weak_text = " ".join([transition.action, transition.interaction_kind])
        strong_matches = matching_terms(terms, strong_text)
        weak_matches = matching_terms(terms, weak_text)
        score = _weighted_score(terms, strong_matches, weak_matches, 0.95, 0.2)
        if score <= 0:
            continue
        items.append(
            CoverageEvidence(
                kind="transition",
                label=element.get("text") or transition.target.get("title") or transition.target.get("url", ""),
                score=round(score, 3),
                details={
                    "source_url": transition.source.get("url", ""),
                    "target_url": transition.target.get("url", ""),
                    "action": transition.action,
                    "matched_terms": sorted(set(strong_matches + weak_matches)),
                    "support_type": "direct",
                    "justification": "Transicao do grafo sustenta uma acao ou mudanca de estado do requisito.",
                },
            )
        )
    return items


def _path_evidence(terms: list[str], paths: list[PathCandidate]) -> list[CoverageEvidence]:
    items: list[CoverageEvidence] = []
    for path in paths:
        step_matches: list[str] = []
        matched_steps = 0
        for step in path.steps:
            text = " ".join(
                [
                    step.source_url,
                    step.target_url,
                    step.action,
                    step.interaction_kind,
                    step.element.get("text", ""),
                    step.element.get("href", ""),
                    step.element.get("aria_label", ""),
                ]
            )
            matches = matching_terms(terms, text)
            if matches:
                matched_steps += 1
            step_matches.extend(matches)
        score = len(set(step_matches)) / max(1, len(terms))
        if score <= 0:
            continue
        final_url = path.steps[-1].target_url if path.steps else ""
        detour_ratio = 1 - (matched_steps / max(1, len(path.steps)))
        items.append(
            CoverageEvidence(
                kind="candidate_path",
                label=path.id,
                score=round(min(score, 1.0), 3),
                details={
                    "final_url": final_url,
                    "steps": len(path.steps),
                    "matched_terms": sorted(set(step_matches)),
                    "detour_ratio": round(detour_ratio, 3),
                    "support_type": "direct" if detour_ratio <= 0.5 else "partial",
                    "justification": "Caminho candidato alinha termos do requisito a uma rota navegacional.",
                },
            )
        )
    return items


def _weighted_score(
    terms: list[str],
    strong_matches: list[str],
    weak_matches: list[str],
    strong_weight: float,
    weak_weight: float,
) -> float:
    if not terms:
        return 0.0
    strong = len(set(strong_matches)) / len(terms)
    weak = len(set(weak_matches)) / len(terms)
    return min(1.0, (strong * strong_weight) + (weak * weak_weight))


def _align_facets(text: str, facets: list[RequirementFacet], evidence: list[CoverageEvidence]) -> _AlignmentResult:
    if not facets or not evidence:
        return _AlignmentResult("missing", 0.0, "absent", 1.0, [facet.kind for facet in facets])

    total_weight = sum(facet.weight for facet in facets)
    unsupported: list[str] = []
    weighted_support = 0.0
    contradiction = False

    for facet in facets:
        support = max((_facet_support(facet, item) for item in evidence), default=0.0)
        weighted_support += facet.weight * support
        if facet.required and support < 0.45:
            unsupported.append(facet.kind)
        if facet.kind == "action" and _has_action_contradiction(facet.text, evidence):
            contradiction = True

    detour_penalty = _detour_penalty(evidence)
    ambiguity_penalty = 0.08 if _is_ambiguous(text) else 0.0
    unsupported_cost = sum(facet.weight for facet in facets if facet.kind in unsupported)
    alignment_cost = max(0.0, (total_weight - weighted_support) + unsupported_cost + detour_penalty + ambiguity_penalty)
    reference_cost = max(total_weight * 1.2, 1.0)
    fit_score = max(0.0, min(1.0, 1 - (alignment_cost / reference_cost)))

    unsupported_critical = _CRITICAL_FACETS.intersection(unsupported)
    has_direct_evidence = any(
        item.kind in {"transition", "candidate_path"}
        and item.details.get("support_type") == "direct"
        for item in evidence
    )

    if contradiction:
        status = "missing"
        support_type = "contradictory"
        fit_score = 0.0
    elif fit_score >= 0.85 and not unsupported_critical:
        status = "supported"
        support_type = "direct" if has_direct_evidence else "indirect"
    elif fit_score >= 0.45:
        status = "partial"
        support_type = "potentially_covered" if _is_ambiguous(text) else "partial"
    else:
        status = "missing"
        support_type = "absent"

    return _AlignmentResult(
        status=status,
        fit_score=round(fit_score, 3),
        support_type=support_type,
        alignment_cost=round(alignment_cost, 3),
        unsupported_facets=unsupported,
    )


def _facet_support(facet: RequirementFacet, evidence: CoverageEvidence) -> float:
    matched_terms = set(str(term) for term in evidence.details.get("matched_terms", []))
    term_score = _semantic_term_score(facet.terms, matched_terms)
    if term_score <= 0 and facet.kind not in {"action", "assertion"}:
        return 0.0

    direct_multiplier = {
        "page": {
            "action": 0.25,
            "assertion": 0.9,
            "data_binding": 0.55,
            "object": 0.8,
            "target_state": 1.0,
        },
        "transition": {
            "action": 1.0,
            "assertion": 0.65,
            "data_binding": 0.75,
            "object": 0.95,
            "target_state": 0.85,
        },
        "candidate_path": {
            "action": 0.9,
            "assertion": 0.7,
            "data_binding": 0.7,
            "object": 0.85,
            "target_state": 0.9,
        },
    }
    multiplier = direct_multiplier.get(evidence.kind, {}).get(facet.kind, 0.5)

    if facet.kind == "action":
        if facet.text == "assertion" and evidence.kind == "page":
            return 0.8
        if _action_supported_by_evidence(facet.text, evidence):
            term_score = max(term_score, 0.85)
        elif facet.text == "navigation" and evidence.kind == "page":
            term_score = max(term_score, 0.55)

    if facet.kind == "assertion" and evidence.kind == "page":
        term_score = max(term_score, min(evidence.score, 0.85))

    return min(1.0, max(term_score, evidence.score * 0.75) * multiplier)


def _semantic_term_score(terms: list[str], matched_terms: set[str]) -> float:
    if not terms:
        return 0.0
    families = _term_families(terms)
    matched = 0
    for family in families:
        if family.intersection(matched_terms):
            matched += 1
    return matched / max(1, len(families))


def _term_families(terms: list[str]) -> list[set[str]]:
    remaining = set(terms)
    families: list[set[str]] = []
    while remaining:
        term = remaining.pop()
        family = {term}
        family.update(_TERM_SYNONYMS.get(term, []))
        for source, synonyms in _TERM_SYNONYMS.items():
            if term in synonyms:
                family.add(source)
                family.update(synonyms)
        normalized_family = family.intersection(set(terms))
        remaining.difference_update(normalized_family)
        families.append(normalized_family or {term})
    return families


def _action_supported_by_evidence(action: str, evidence: CoverageEvidence) -> bool:
    text = _evidence_text(evidence)
    action_terms = set(_ACTION_FACETS.get(action, {}).get("terms", []))
    if any(term in text for term in action_terms):
        return True
    if action in {"navigation", "click"} and evidence.kind in {"transition", "candidate_path"}:
        return "click" in text or "href" in text
    return False


def _has_action_contradiction(action: str, evidence: list[CoverageEvidence]) -> bool:
    contradictions = _CONTRADICTORY_ACTIONS.get(action, set())
    if not contradictions:
        return False
    for item in evidence:
        if item.score < 0.4:
            continue
        text = _evidence_text(item)
        if any(term in text for term in contradictions):
            return True
    return False


def _evidence_text(evidence: CoverageEvidence) -> str:
    detail_values = " ".join(str(value) for value in evidence.details.values())
    return normalize_text(" ".join([evidence.kind, evidence.label, detail_values]))


def _detour_penalty(evidence: list[CoverageEvidence]) -> float:
    path_penalties = [
        float(item.details.get("detour_ratio", 0.0)) * 0.35
        for item in evidence
        if item.kind == "candidate_path"
    ]
    return min(path_penalties) if path_penalties else 0.0


def _is_ambiguous(text: str) -> bool:
    terms = set(normalize_spec(text).terms)
    return bool(terms.intersection(_AMBIGUITY_HINTS))


def _is_assertion_requirement(text: str) -> bool:
    normalized = normalize_text(text)
    return any(term in normalized for term in ("validar", "verificar", "exibe", "exibida", "visivel", "aberta"))


def _overall_status(score: float, partial: int, missing: int) -> str:
    if score >= 0.8 and partial == 0 and missing == 0:
        return "supported"
    if score >= 0.4:
        return "partial"
    return "low_coverage"


def _warning_for_status(status: str) -> str:
    if status == "missing":
        return "Nao ha evidencia suficiente no grafo para gerar este passo sem risco de invencao."
    if status == "partial":
        return "Ha evidencia parcial; gere o teste com cautela e prefira assercoes suportadas pelo grafo."
    return ""


def _dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        key = normalize_text(value)
        if key in seen:
            continue
        seen.add(key)
        result.append(value)
    return result
