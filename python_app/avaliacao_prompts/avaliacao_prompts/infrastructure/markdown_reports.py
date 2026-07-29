from __future__ import annotations

from pathlib import Path
from statistics import mean

from avaliacao_prompts.domain.models import EvaluationReport


_RISK_LABELS = {
    "none": "não aplicável",
    "low": "baixo",
    "medium": "médio",
    "high": "alto",
}
_STATUS_LABELS = {
    "not_run": "não executado",
    "passed": "passou",
    "skipped": "ignorado por pré-condição",
    "failed": "falhou",
    "timed_out": "tempo esgotado",
    "syntax_error": "erro de sintaxe",
    "runtime_error": "erro em execução",
    "environment_error": "erro de ambiente",
}


class MarkdownEvaluationReportWriter:
    def write(self, output_path: Path, reports: list[EvaluationReport]) -> Path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(render_markdown_report(reports), encoding="utf-8")
        return output_path


def render_markdown_report(reports: list[EvaluationReport]) -> str:
    lines = [
        "# Relatório auxiliar de avaliação dos testes E2E",
        "",
        "> Este relatório é uma ferramenta não oficial de apoio à análise. As métricas automáticas são evidências; não constituem, isoladamente, uma avaliação de correção semântica.",
        "",
        "## Visão geral",
        "",
        *_summary_table(reports),
        "",
        "## Como interpretar",
        "",
        "- **Estrutura mínima** verifica apenas a presença de importação do Playwright, bloco de teste e asserção.",
        "- **Risco dos seletores** é uma heurística: seletores semânticos reduzem o risco; XPath e esperas fixas elevam o risco.",
        "- **Cobertura pelo grafo** indica se URLs e textos de locators foram encontrados nas evidências coletadas. Uma ausência é um ponto para revisão, não prova de erro.",
        "- **Rubrica humana** deve receber notas de 0 (não atende), 1 (atende parcialmente) ou 2 (atende completamente).",
        "",
    ]
    for index, report in enumerate(reports, start=1):
        lines.extend(_report_section(index, report))
    return "\n".join(lines).rstrip() + "\n"


def _summary_table(reports: list[EvaluationReport]) -> list[str]:
    total = len(reports)
    minimum_structure = sum(_has_minimum_structure(report) for report in reports)
    with_assertion = sum(report.static_analysis.has_expect_assertion for report in reports)
    with_fixed_wait = sum(report.static_analysis.uses_wait_for_timeout for report in reports)
    risk_counts = {
        risk: sum(report.static_analysis.selector_risk == risk for report in reports)
        for risk in ("low", "medium", "high", "none")
    }
    graph_reports = [report.graph_conformance for report in reports if report.graph_conformance is not None]
    measured_inputs = [report.prompt_metrics for report in reports if report.prompt_metrics is not None]
    execution_counts = {
        status: sum(report.execution.status == status for report in reports)
        for status in ("passed", "skipped", "failed", "timed_out", "syntax_error", "runtime_error", "environment_error", "not_run")
    }
    rows = [
        ("Testes analisados", str(total)),
        ("Com estrutura mínima reconhecida", _fraction(minimum_structure, total)),
        ("Com pelo menos uma asserção", _fraction(with_assertion, total)),
        ("Com espera fixa `waitForTimeout`", _fraction(with_fixed_wait, total)),
        (
            "Risco dos seletores",
            f"baixo: {risk_counts['low']}; médio: {risk_counts['medium']}; alto: {risk_counts['high']}; não aplicável: {risk_counts['none']}",
        ),
        (
            "Resultado da execução",
            "; ".join(
                f"{_STATUS_LABELS[status]}: {count}"
                for status, count in execution_counts.items()
                if count
            ),
        ),
    ]
    if measured_inputs:
        rows.append(
            (
                "Tamanho médio da entrada da LLM",
                f"{mean(item.character_count for item in measured_inputs):.0f} caracteres; "
                f"{mean(item.line_count for item in measured_inputs):.1f} linhas".replace(".", ","),
            )
        )
    if graph_reports:
        rows.extend(
            [
                ("Cobertura média de URLs no grafo", _percentage(mean(item.graph_url_coverage for item in graph_reports))),
                ("Cobertura média de textos no grafo", _percentage(mean(item.locator_text_coverage for item in graph_reports))),
            ]
        )
    else:
        rows.append(("Conformidade com o grafo", "não analisada"))
    return _table(("Indicador", "Resultado"), rows)


def _report_section(index: int, report: EvaluationReport) -> list[str]:
    case = report.case
    analysis = report.static_analysis
    graph = report.graph_conformance
    prompt = report.prompt_metrics
    execution = report.execution
    lines = [
        f"## {index}. {_escape(case.spec_id)}",
        "",
        *_table(
            ("Identificação", "Valor"),
            [
                ("Abordagem", case.approach),
                ("Arquivo de teste", f"`{_escape_code(str(case.test_file))}`"),
                ("URL base", case.base_url),
                ("Entrada da LLM", f"`{_escape_code(str(case.prompt_file))}`" if case.prompt_file else "não localizada/informada"),
            ],
        ),
        "",
        "### Leitura rápida",
        "",
        _finding(_has_minimum_structure(report), "Estrutura mínima do Playwright reconhecida", "Estrutura mínima incompleta; revise importação, bloco `test` e asserção"),
        _finding(analysis.has_expect_assertion, "O teste contém asserção", "Nenhuma asserção foi identificada"),
        _finding(not analysis.uses_wait_for_timeout, "Não usa espera fixa", "Usa `waitForTimeout`, o que aumenta a fragilidade"),
        f"- **Risco estimado dos seletores:** {_RISK_LABELS[analysis.selector_risk]}.",
    ]
    if graph is None:
        lines.append("- **Conformidade com o grafo:** não analisada nesta execução.")
    else:
        lines.extend(
            [
                f"- **URLs fundamentadas no grafo:** {_percentage(graph.graph_url_coverage)}.",
                f"- **Textos de locators fundamentados no grafo:** {_percentage(graph.locator_text_coverage)}.",
            ]
        )
    lines.extend(
        [
            "",
            "### Estrutura e seletores",
            "",
            *_table(
                ("Métrica", "Resultado", "Leitura"),
                [
                    ("Importa `@playwright/test`", _yes_no(analysis.has_playwright_import), "necessário para execução"),
                    ("Possui bloco `test(...)`", _yes_no(analysis.has_test_block), "estrutura do caso de teste"),
                    ("Possui `expect(...)`", _yes_no(analysis.has_expect_assertion), "indício de verificação do resultado"),
                    ("Ações de usuário", str(analysis.action_count), "cliques, preenchimentos e ações similares"),
                    ("Locators", str(analysis.locator_count), "total identificado estaticamente"),
                    ("Locators semânticos", str(analysis.semantic_locator_count), "role, label, texto, placeholder etc."),
                    ("XPath", str(analysis.xpath_count), "valores maiores que zero merecem revisão"),
                    (
                        "Espera fixa",
                        _yes_no(analysis.uses_wait_for_timeout),
                        "presente; merece revisão" if analysis.uses_wait_for_timeout else "ausente",
                    ),
                ],
            ),
            "",
            "### Evidências encontradas no código",
            "",
            "**URLs usadas em `page.goto`:**",
            "",
            *_items(analysis.goto_urls, "nenhuma URL literal identificada"),
            "",
            "**Textos extraídos dos locators:**",
            "",
            *_items(analysis.locator_texts, "nenhum texto de locator identificado"),
            "",
        ]
    )
    if graph is not None:
        lines.extend(
            [
                "### Pontos para revisão contra o grafo",
                "",
                "**URLs não encontradas:**",
                "",
                *_items(graph.unknown_urls, "nenhuma"),
                "",
                "**Textos de locators não encontrados:**",
                "",
                *_items(graph.unknown_locator_texts, "nenhum"),
                "",
            ]
        )
    lines.extend(
        [
            "### Prompt e execução",
            "",
            *_table(
                ("Item", "Resultado"),
                [
                    ("Tamanho da entrada", f"{prompt.character_count} caracteres; {prompt.line_count} linhas" if prompt else "não disponível"),
                    ("Estado da execução", _STATUS_LABELS[execution.status]),
                    ("Duração", f"{execution.duration_seconds:.3f} s" if execution.duration_seconds is not None else "não disponível"),
                    ("Tipo de erro", execution.error_type or "não informado"),
                    ("Mensagem", execution.error_message_excerpt or "não informada"),
                ],
            ),
            "",
            "### Rubrica para avaliação humana",
            "",
            *_human_review_table(report),
            "",
            f"**Classificação da falha:** {report.human_review.failure_classification or 'não preenchida'}",
            "",
            f"**Observações:** {report.human_review.notes or '_preencher durante a análise_'}",
            "",
            "---",
            "",
        ]
    )
    return lines


def _human_review_table(report: EvaluationReport) -> list[str]:
    review = report.human_review
    return _table(
        ("Critério", "Pergunta orientadora", "Nota (0–2)"),
        [
            ("Fluxo correto", "Executa os passos principais pedidos?", _score(review.flow_correctness)),
            ("Alvo correto", "Interage com os elementos esperados?", _score(review.target_correctness)),
            ("Asserção correta", "Valida o resultado especificado?", _score(review.assertion_correctness)),
            ("Aderência ao grafo", "Usa evidências disponíveis no contexto?", _score(review.graph_adherence)),
            ("Robustez prática", "Seletores e esperas são aceitáveis?", _score(review.practical_robustness)),
            ("Utilidade geral", "Exige pouca ou nenhuma correção manual?", _score(review.overall_usefulness)),
        ],
    )


def _table(headers: tuple[str, ...], rows: list[tuple[str, ...]]) -> list[str]:
    return [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
        *("| " + " | ".join(_escape(cell) for cell in row) + " |" for row in rows),
    ]


def _items(values: list[str], empty_message: str) -> list[str]:
    return [f"- `{_escape_code(value)}`" for value in values] or [f"- _{empty_message}_"]


def _finding(ok: bool, success: str, failure: str) -> str:
    return f"- {'✅' if ok else '⚠️'} {success if ok else failure}."


def _has_minimum_structure(report: EvaluationReport) -> bool:
    item = report.static_analysis
    return item.has_playwright_import and item.has_test_block and item.has_expect_assertion


def _fraction(value: int, total: int) -> str:
    return f"{value} de {total} ({_percentage(value / total if total else 0.0)})"


def _percentage(value: float) -> str:
    return f"{value * 100:.1f}%".replace(".", ",")


def _yes_no(value: bool) -> str:
    return "sim" if value else "não"


def _score(value: int | None) -> str:
    return str(value) if value is not None else "—"


def _escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def _escape_code(value: str) -> str:
    return value.replace("`", "\\`")
