from __future__ import annotations

import json

from teste_prompt_e2e_semantico.domain.models import (
    ContextElement,
    ObservedResult,
    PageEvidence,
    SpecificationStep,
    SpecPlan,
    StructuredContext,
)


def build_structured_prompt(
    spec: SpecPlan,
    base_url: str,
    requirements: list[SpecificationStep],
    context: StructuredContext,
) -> str:
    parts = [
        "# Geracao de teste E2E Playwright",
        "",
        "Gere um teste TypeScript Playwright fiel a especificacao.",
        "",
        "Regras:",
        "- Retorne um unico bloco de codigo `typescript`, sem texto fora dele; o conteudo interno deve ser um arquivo Playwright `.spec.ts` completo e executavel por `npx playwright test`.",
        "- Importe `test` e `expect` de `@playwright/test`.",
        f"- Inicie com `await page.goto('{base_url.rstrip('/')}/')`; use URLs literais tambem em `toHaveURL`, sem regex ou links Markdown.",
        "- Nao derive rotas do texto de links, produtos ou titulos. Use `toHaveURL` somente quando a URL exata estiver na base ou no contexto; sem URL observada, confirme a pagina por elementos visiveis.",
        "- Use locators Playwright legiveis e unicos no modo estrito; evite XPath, indices e `waitForTimeout`.",
        "- Cada valor `locator_playwright=...` e uma expressao TypeScript Playwright completa e executavel. Copie a expressao sem aspas adicionais e aplique a acao nela, por exemplo `await page.getByRole('button', { name: 'Search', exact: true }).click()` ou `await page.getByLabel('Email:', { exact: true }).fill(valor)`.",
        "- Nunca passe uma expressao `page.getBy*` ou `page.locator` como argumento de `page.click`, `page.fill` ou `page.selectOption`; chame `.click()`, `.fill()` ou `.selectOption()` diretamente no locator.",
        "- Nao use no codigo a notacao descritiva de `controle=...` nem invente engines como `role_name:`, `label:`, `id:`, `tag=` ou `text:`. Somente os valores de `locator_playwright=...` sao locators copiaveis.",
        "- Quando o contexto fornecer `locator_playwright`, preserve esse locator; nao o substitua por um locator generico baseado apenas em papel e nome.",
        "- Quando varios itens ou variantes compartilharem a mesma acao, relacione o controle escolhido ao nome visivel do item antes do clique e reutilize esse nome nas verificacoes posteriores; nao trate o titulo da pagina agrupadora como nome do item sem confirmar essa igualdade. Se o nome exato nao puder ser observado, verifique apenas a propriedade explicitada pela especificacao, sem inventar um rotulo.",
        "- Inclua assercoes observaveis que comprovem o resultado esperado.",
        "- O contexto é apenas um guia: combine-o com a especificacao e sua experiencia para navegar, localizar elementos e executar as acoes.",
        "- Caso seja possível acessar a aplicação, entre nela e interaja validando o fluxo e os resultados e utilizando as informações obtidas nessa interação em conjunto do contexto e a especificacao e seu conhecimento de playwright para fazer o teste ts; caso contrario, use a especificacao, o contexto observado e seu conhecimento de Playwright sem afirmar que executou acoes.",
        "",
        f"Especificacao `{spec.title}` em etapas:",
        *[f"{index}. {item.text}" for index, item in enumerate(requirements, start=1)],
        "",
        "Contexto estruturado por etapa:",
        *_context_lines(context),
        "",
        "Use as informacoes observadas quando forem aplicaveis, sem limitar o teste a elas.",
        "`pagina_evidencia` nao comprova uma transicao ate a pagina.",
        "Sem contexto, siga a especificacao e interaja normalmente com a pagina; nao trate inferencias como fatos observados.",
    ]
    return "\n".join(parts).strip() + "\n"


def _context_lines(context: StructuredContext) -> list[str]:
    if context.item_count == 0:
        return [
            "- Nenhum controle ou resultado correspondente foi observado para esta especificacao; "
            "nenhuma evidencia literal de pagina foi encontrada."
        ]

    lines = []
    missing = []
    for index, step in enumerate(context.steps, start=1):
        if not step.interactions and step.page_evidence is None:
            missing.append(str(index))
            continue
        lines.append(f"Etapa {index} ({step.requirement_id}):")
        interaction_count = len(step.interactions)
        interaction_pages = {
            interaction.control.page_url
            for interaction in step.interactions
        }
        shared_interaction_page = interaction_count > 1 and len(interaction_pages) == 1
        if shared_interaction_page:
            lines.append(f"- pagina={next(iter(interaction_pages))}")
        for interaction_index, interaction in enumerate(step.interactions, start=1):
            suffix = f"_{interaction_index}" if interaction_count > 1 else ""
            lines.extend(
                _control_lines(
                    interaction.control,
                    suffix,
                    include_page=not shared_interaction_page,
                )
            )
            if interaction.observed_result is not None:
                lines.extend(_result_lines(interaction.observed_result, suffix))
        if step.page_evidence is not None:
            lines.extend(_page_evidence_lines(step.page_evidence))
    if missing:
        lines.append(f"Etapas sem contexto observado: {', '.join(missing)}.")
    return lines


def _control_lines(
    control: ContextElement,
    suffix: str = "",
    *,
    include_page: bool = True,
) -> list[str]:
    lines = [
        f"- controle{suffix}={_element_label(control.element)}",
        f"- operacao{suffix}={control.action or control.interaction_kind}",
    ]
    if include_page:
        lines.insert(0, f"- pagina{suffix}={control.page_url}")
    # A form action describes where the browser may submit data; it is not an
    # observed navigation.  Only links expose a destination in the prompt.
    if control.destination_url and control.element.get("href"):
        lines.append(f"- destino{suffix}={control.destination_url}")
    if control.selector is not None:
        lines.append(f"- locator_playwright{suffix}={_selector_expression(control)}")
    return lines


def _selector_expression(control: ContextElement) -> str:
    selector = control.selector
    if selector is None:
        return ""
    kind = selector.kind.casefold()
    value = _typescript_literal(selector.value)

    if kind in {"role_name", "role_name_exact"}:
        role = _accessible_role(control)
        return (
            f"page.getByRole({_typescript_literal(role)}, "
            f"{{ name: {value}, exact: true }})"
        )
    if kind in {"data-testid", "testid"}:
        return f"page.getByTestId({value})"
    if kind == "data-test":
        return _attribute_locator("data-test", selector.value)
    if kind in {"aria_label", "label"}:
        return f"page.getByLabel({value}, {{ exact: true }})"
    if kind == "id":
        return _attribute_locator("id", selector.value)
    if kind == "name":
        return _attribute_locator("name", selector.value)
    if kind == "placeholder":
        return f"page.getByPlaceholder({value}, {{ exact: true }})"
    if kind == "text":
        expression = f"page.getByText({value}, {{ exact: true }})"
        if control.element.get("tag", "").casefold() == "a":
            # Menus responsivos podem repetir o mesmo link no DOM. A política
            # continua sem nth/index numérico, mas torna o locator executável
            # no modo estrito escolhendo a primeira ocorrência observável.
            return expression + ".first()"
        return expression
    if kind == "href":
        return _attribute_locator("href", selector.value, tag="a")
    if kind == "role":
        return f"page.getByRole({value})"
    if kind == "css":
        return f"page.locator({value})"
    raise ValueError(
        f"Tipo de seletor sem tradução Playwright segura: {selector.kind!r}"
    )


def _accessible_role(control: ContextElement) -> str:
    tag = control.element.get("tag", "").casefold()
    input_type = control.element.get("input_type", "").casefold()
    if tag == "a":
        return "link"
    if tag == "button" or (tag == "input" and input_type in {"button", "submit", "reset"}):
        return "button"
    role = control.element.get("role", "").strip()
    if role:
        return role
    return control.interaction_kind


def _attribute_locator(attribute: str, value: str, *, tag: str = "") -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    css = f'{tag}[{attribute}="{escaped}"]'
    return f"page.locator({_typescript_literal(css)})"


def _typescript_literal(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def _result_lines(result: ObservedResult, suffix: str = "") -> list[str]:
    lines = [f"- resultado_observado{suffix}={result.text}"]
    if result.element_id:
        lines.append(
            f"- locator_playwright_resultado{suffix}="
            f"{_attribute_locator('id', result.element_id)}"
        )
    elif result.role:
        lines.append(
            f"- locator_playwright_resultado{suffix}="
            f"page.getByRole({_typescript_literal(result.role)})"
        )
    return lines


def _page_evidence_lines(evidence: PageEvidence) -> list[str]:
    return [
        f"- pagina_evidencia={evidence.page_url}",
        f"- evidencia_pagina={evidence.source}:{evidence.text}",
    ]


def _element_label(element: dict[str, str]) -> str:
    fields = [
        f"{key}={element[key]}"
        for key in (
            "tag", "text", "title", "label", "data_testid", "id", "name", "input_type",
            "value", "href", "role", "aria_label", "placeholder", "form_action", "form_method",
        )
        if element.get(key)
    ]
    return ", ".join(fields) or "elemento sem identificacao textual"
