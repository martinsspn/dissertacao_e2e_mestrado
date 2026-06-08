from __future__ import annotations

import json

from teste_prompt_e2e_semantico.domain.models import (
    PathCandidate,
    PathStep,
    RelevantGraphContext,
    ScoredPage,
    ScoredTransition,
    SelectorCandidate,
    SpecPlan,
)


def build_structured_prompt(spec: SpecPlan, base_url: str, context: RelevantGraphContext) -> str:
    graph_context = _compact_graph_context(context)
    payload = {
        "base_url": base_url.rstrip("/"),
        "specification_title": spec.title,
        "specification": spec.raw_text.strip(),
        "context_quality": _context_quality(graph_context),
        "specification_coverage": _compact_coverage(context),
        "graph_context": graph_context,
    }

    return "\n".join(
        [
            "# Prompt Para Geracao De Teste E2E Playwright",
            "",
            "## Papel Da LLM",
            "",
            (
                "Voce e uma especialista em testes E2E com Playwright. Gere um teste TypeScript robusto, "
                "legivel e fiel a especificacao em linguagem natural."
            ),
            "",
            "## Objetivo",
            "",
            (
                "Gerar um arquivo .spec.ts usando a especificacao do usuario e o contexto do grafo navegacional. "
                "O grafo foi selecionado por similaridade textual e qualidade de seletores; use-o como fonte de "
                "verdade para paginas, transicoes e elementos disponiveis, mas escolha o fluxo mais coerente com a especificacao."
            ),
            "",
            "## Regras Obrigatorias",
            "",
            "- Retorne apenas o codigo TypeScript do teste, sem Markdown.",
            "- Importe `test` e `expect` de `@playwright/test`.",
            "- Comece pela `base_url` fornecida nos dados estruturados.",
            "- Nao invente rotas, textos ou seletores quando houver alternativa no grafo.",
            "- Prefira locators semanticos do Playwright: `getByRole`, `getByLabel`, `getByPlaceholder` e `getByText`.",
            "- Use atributos estaveis como `data-testid`, `data-test`, `id` ou `name` quando forem a melhor opcao disponivel.",
            "- Evite XPath, `nth-child`, classes de layout e seletores longos, exceto como ultimo recurso.",
            "- Inclua assercoes observaveis que comprovem que a especificacao foi atendida.",
            "- Evite `waitForTimeout`; prefira esperas por estado visivel, URL, resposta ou elemento esperado.",
            "- Se houver multiplos caminhos candidatos, escolha o mais coerente com a especificacao e com seletores fortes.",
            "- Se os caminhos candidatos forem insuficientes, use as paginas e transicoes relevantes para compor o menor fluxo valido.",
            "- Trate transicoes com acao `reload` como evidencias de pagina, nao como passos preferenciais de interacao.",
            "- Use `specification_coverage` como gate de conformance: priorize requisitos `supported`, trate `partial` e `potentially_covered` como lacunas explicitas e nao invente passos `missing`.",
            "- Respeite as facetas em `specification_coverage.requirements[].facets`: verbo, objeto, estado alvo, dados e assercao precisam estar sustentados por evidencia do grafo.",
            "- Quando houver requisitos `missing`, gere apenas o teste suportado pelo grafo e inclua assercoes observaveis para as partes cobertas.",
            "",
            "## Politica De Seletores",
            "",
            "Prioridade recomendada:",
            "",
            "1. `getByRole(role, { name })` quando role/nome acessivel estiverem disponiveis.",
            "2. `getByLabel`, `getByPlaceholder` ou `getByText` para elementos claramente identificaveis.",
            "3. Locators por atributos estaveis (`data-testid`, `data-test`, `id`, `name`).",
            "4. CSS curto e especifico quando nao houver seletor semantico.",
            "5. XPath ou seletores estruturais apenas se nao houver alternativa melhor.",
            "",
            "## Dados Estruturados",
            "",
            "```json",
            json.dumps(payload, indent=2, ensure_ascii=False),
            "```",
            "",
            "## Auto-Verificacao Antes De Responder",
            "",
            "- O teste cobre a especificacao em linguagem natural?",
            "- O fluxo escolhido existe ou e suportado pelo grafo navegacional?",
            "- Os seletores escolhidos sao os mais robustos entre as opcoes disponiveis?",
            "- Ha assercoes suficientes para validar o resultado esperado?",
            "- O codigo final pode ser salvo diretamente como `.spec.ts`?",
            "",
        ]
    )


def _compact_graph_context(context: RelevantGraphContext) -> dict[str, object]:
    return {
        "candidate_paths": [_compact_path(path) for path in context.paths],
        "relevant_pages": [_compact_page(page) for page in context.pages],
        "relevant_transitions": [_compact_transition(transition) for transition in context.transitions],
    }


def _compact_path(path: PathCandidate) -> dict[str, object]:
    return {
        "path_id": path.id,
        "score": round(path.score, 3),
        "steps": [_compact_step(step) for step in path.steps],
    }


def _compact_step(step: PathStep) -> dict[str, object]:
    return {
        "source_url": step.source_url,
        "target_url": step.target_url,
        "action": step.action,
        "interaction_kind": step.interaction_kind,
        "element": _non_empty_dict(step.element),
        "recommended_selectors": [_compact_selector(selector) for selector in step.recommended_selectors[:2]],
    }


def _compact_page(scored_page: ScoredPage) -> dict[str, object]:
    page = scored_page.page
    return {
        "url": page.url,
        "title": page.title,
        "h1": page.h1,
        "visible_text_excerpt": _truncate(page.visible_text_excerpt, 500),
        "interactive_count": page.interactive_count,
        "relevance_score": round(scored_page.score, 3),
        "matched_terms": scored_page.matched_terms,
    }


def _compact_transition(scored_transition: ScoredTransition) -> dict[str, object]:
    transition = scored_transition.transition
    return {
        "source": transition.source,
        "target": transition.target,
        "action": transition.action,
        "interaction_kind": transition.interaction_kind,
        "element": _non_empty_dict(transition.element),
        "relevance_score": round(scored_transition.score, 3),
        "matched_terms": scored_transition.matched_terms,
        "recommended_selectors": [
            _compact_selector(selector) for selector in scored_transition.selector_candidates[:3]
        ],
    }


def _compact_selector(selector: SelectorCandidate) -> dict[str, object]:
    return {
        "kind": selector.kind,
        "value": selector.value,
        "score": round(selector.score, 3),
        "strength": selector.strength,
        "reason": selector.reason,
    }


def _compact_coverage(context: RelevantGraphContext) -> dict[str, object]:
    coverage = context.coverage
    if coverage is None:
        return {
            "overall_status": "unknown",
            "coverage_score": 0.0,
            "requirements": [],
            "warnings": ["Cobertura da especificacao nao calculada."],
        }
    return {
        "overall_status": coverage.overall_status,
        "coverage_score": coverage.coverage_score,
        "summary": {
            "supported": coverage.supported_requirements,
            "partial": coverage.partial_requirements,
            "missing": coverage.missing_requirements,
        },
        "requirements": [
            {
                "text": requirement.text,
                "terms": requirement.terms,
                "facets": [
                    {
                        "kind": facet.kind,
                        "text": facet.text,
                        "terms": facet.terms,
                        "weight": round(facet.weight, 3),
                        "required": facet.required,
                    }
                    for facet in requirement.facets
                ],
                "status": requirement.status,
                "confidence": requirement.confidence,
                "fit_score": requirement.fit_score,
                "support_type": requirement.support_type,
                "alignment_cost": requirement.alignment_cost,
                "unsupported_facets": requirement.unsupported_facets,
                "warning": requirement.warning,
                "evidence": [
                    {
                        "kind": evidence.kind,
                        "label": evidence.label,
                        "score": round(evidence.score, 3),
                        "details": evidence.details,
                    }
                    for evidence in requirement.evidence
                ],
            }
            for requirement in coverage.requirements
        ],
        "warnings": coverage.warnings,
    }


def _context_quality(graph_context: dict[str, object]) -> dict[str, object]:
    paths = graph_context["candidate_paths"]
    transitions = graph_context["relevant_transitions"]
    selector_strengths = {"strong": 0, "medium": 0, "weak": 0}
    reload_transitions = 0
    for transition in transitions:
        if transition["action"] == "reload":
            reload_transitions += 1
        for selector in transition["recommended_selectors"]:
            strength = selector.get("strength")
            if strength in selector_strengths:
                selector_strengths[strength] += 1

    warnings: list[str] = []
    if not paths:
        warnings.append("Nenhum caminho candidato acionavel foi encontrado; use transicoes relevantes como evidencia.")
    if selector_strengths["strong"] == 0 and selector_strengths["medium"] == 0:
        warnings.append("O contexto possui poucos seletores robustos; prefira assercoes por texto/titulo/URL.")
    if reload_transitions:
        warnings.append("Algumas transicoes relevantes sao reloads; elas indicam paginas, nao interacoes preferenciais.")

    return {
        "candidate_paths": len(paths),
        "relevant_transitions": len(transitions),
        "selector_strength_distribution": selector_strengths,
        "warnings": warnings,
    }


def _non_empty_dict(value: dict[str, object]) -> dict[str, object]:
    return {key: item for key, item in value.items() if item not in ("", None, [], {})}


def _truncate(value: str, max_length: int) -> str:
    normalized = " ".join(value.split())
    if len(normalized) <= max_length:
        return normalized
    return normalized[:max_length].rstrip() + "..."
