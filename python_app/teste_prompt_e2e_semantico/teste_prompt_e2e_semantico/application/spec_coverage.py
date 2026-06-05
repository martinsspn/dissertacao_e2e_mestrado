from __future__ import annotations

import re

from teste_prompt_e2e_semantico.application.text_normalization import matching_terms, normalize_spec, normalize_text
from teste_prompt_e2e_semantico.domain.models import (
    CoverageEvidence,
    PathCandidate,
    RequirementCoverage,
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
    score = (supported + (partial * 0.5)) / max(1, len(requirements))

    warnings: list[str] = []
    if missing:
        warnings.append("Ha requisitos sem evidencia concreta no grafo; alto risco de alucinacao se forem exigidos no teste.")
    if partial:
        warnings.append("Ha requisitos parcialmente cobertos; use apenas paginas/transicoes evidenciadas.")
    if not paths:
        warnings.append("Nenhum caminho candidato foi encontrado para esta especificacao.")

    return SpecCoverageReport(
        overall_status=_overall_status(score, missing),
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
    terms = _coverage_terms(text)
    evidence = _collect_evidence(terms, pages, transitions, paths)
    confidence = evidence[0].score if evidence else 0.0
    status = _requirement_status(text, evidence)
    return RequirementCoverage(
        text=text,
        terms=terms,
        status=status,
        confidence=round(confidence, 3),
        evidence=evidence[:4],
        warning=_warning_for_status(status),
    )


def _coverage_terms(text: str) -> list[str]:
    raw_terms = normalize_spec(text).terms
    terms = [term for term in raw_terms if term not in _GENERIC_TERMS]
    expanded: list[str] = []
    for term in terms:
        expanded.append(term)
        expanded.extend(_TERM_SYNONYMS.get(term, []))
    return _dedupe(expanded)


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
                },
            )
        )
    return items


def _path_evidence(terms: list[str], paths: list[PathCandidate]) -> list[CoverageEvidence]:
    items: list[CoverageEvidence] = []
    for path in paths:
        step_matches: list[str] = []
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
            step_matches.extend(matching_terms(terms, text))
        score = len(set(step_matches)) / max(1, len(terms))
        if score <= 0:
            continue
        final_url = path.steps[-1].target_url if path.steps else ""
        items.append(
            CoverageEvidence(
                kind="candidate_path",
                label=path.id,
                score=round(min(score, 1.0), 3),
                details={
                    "final_url": final_url,
                    "steps": len(path.steps),
                    "matched_terms": sorted(set(step_matches)),
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


def _requirement_status(text: str, evidence: list[CoverageEvidence]) -> str:
    if not evidence:
        return "missing"
    best = evidence[0]
    has_transition_or_path = any(item.kind in {"transition", "candidate_path"} and item.score >= 0.5 for item in evidence)
    if best.score >= 0.7 and (best.kind != "page" or has_transition_or_path or _is_assertion_requirement(text)):
        return "supported"
    if best.kind == "page" and best.score >= 0.85:
        return "supported"
    if best.score >= 0.4 or has_transition_or_path:
        return "partial"
    return "missing"


def _is_assertion_requirement(text: str) -> bool:
    normalized = normalize_text(text)
    return any(term in normalized for term in ("validar", "verificar", "exibe", "exibida", "visivel", "aberta"))


def _overall_status(score: float, missing: int) -> str:
    if score >= 0.8 and missing == 0:
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
