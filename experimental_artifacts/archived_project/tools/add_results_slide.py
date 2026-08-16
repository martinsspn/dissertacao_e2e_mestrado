from __future__ import annotations

import re
import tempfile
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from generate_defense_deck import (
    AMBER,
    BLUE,
    GREEN,
    INK,
    LINE,
    MUTED,
    RED,
    TEAL,
    WHITE,
    footer,
    header,
    paragraph,
    rect,
    slide_xml,
    text_box,
)


PRESENTATION = Path("docs/apresentação gerador de prompt - atualizada 2026-07.pptm")
INSERT_AFTER = 15
NEW_SLIDE_NUMBER = 16


def theoretical_foundation_slide() -> list[str]:
    parts = header("Fundamentação Teórica", "robustez de locators")
    parts.extend([
        rect(10, 0.72, 1.18, 3.82, 4.92, WHITE, line=LINE),
        rect(11, 0.72, 1.18, 0.08, 4.92, BLUE, radius="rect"),
        text_box(12, 1.02, 1.45, 3.22, 0.4, paragraph("O que a literatura demonstra", 1450, BLUE, True, space_after=0), margin=0),
        text_box(
            13,
            1.02,
            2.05,
            3.16,
            3.5,
            paragraph("Locators podem quebrar quando a aplicação e o DOM evoluem.", 1120, INK, False, bullet=True, space_after=340)
            + paragraph("A estratégia de localização influencia a quantidade de quebras observada entre versões.", 1120, INK, False, bullet=True, space_after=340)
            + paragraph("Robustez é uma propriedade empírica: deve ser medida executando os mesmos testes em versões modificadas.", 1120, INK, True, bullet=True, space_after=0),
            margin=50_000,
        ),
        rect(20, 4.75, 1.18, 3.82, 4.92, WHITE, line=LINE),
        rect(21, 4.75, 1.18, 0.08, 4.92, TEAL, radius="rect"),
        text_box(22, 5.05, 1.45, 3.22, 0.4, paragraph("Recomendação do Playwright", 1450, TEAL, True, space_after=0), margin=0),
        text_box(
            23,
            5.05,
            2.05,
            3.16,
            3.5,
            paragraph("Priorizar atributos percebidos pelo usuário e contratos explícitos, como role, label e test id.", 1120, INK, False, bullet=True, space_after=340)
            + paragraph("Evitar cadeias CSS/XPath dependentes da estrutura do DOM.", 1120, INK, False, bullet=True, space_after=340)
            + paragraph("É orientação técnica oficial; isoladamente, não constitui prova experimental para esta pesquisa.", 1120, RED, True, bullet=True, space_after=0),
            margin=50_000,
        ),
        rect(30, 8.78, 1.18, 3.82, 4.92, "F7F8FA", line=LINE),
        rect(31, 8.78, 1.18, 0.08, 4.92, AMBER, radius="rect"),
        text_box(32, 9.08, 1.45, 3.22, 0.4, paragraph("Consequência metodológica", 1450, AMBER, True, space_after=0), margin=0),
        text_box(
            33,
            9.08,
            2.05,
            3.16,
            3.5,
            paragraph("A geração permite descrever quais locators foram produzidos.", 1120, INK, False, bullet=True, space_after=340)
            + paragraph("A execução na versão original mede executabilidade inicial.", 1120, INK, False, bullet=True, space_after=340)
            + paragraph("Somente mudanças controladas nas páginas permitirão comparar resiliência.", 1120, AMBER, True, bullet=True, space_after=0),
            margin=50_000,
        ),
        text_box(
            40,
            0.82,
            6.25,
            11.7,
            0.58,
            paragraph("Fontes: Hammoudi, Rothermel e Tonella (ICST 2016), DOI 10.1109/ICST.2016.16; Playwright, Locators e Best Practices, playwright.dev/docs.", 760, MUTED, False, align="ctr", space_after=0),
            margin=0,
        ),
        footer(9),
    ])
    return parts


def related_work_slide() -> list[str]:
    parts = header("Trabalhos Relacionados", "evolução de páginas e locators")
    studies = [
        (10, 0.72, "Hammoudi et al. (2016)", "Taxonomia baseada em 453 versões e 1.065 quebras de testes record/replay. Evidencia diferentes causas de quebra durante a evolução.", BLUE),
        (20, 4.76, "Leotta et al. (2015)", "Em seis aplicações, multi-locators apresentaram cerca de 30% menos quebras que o melhor locator individual comparado.", TEAL),
        (30, 8.80, "Leotta et al. (2016)", "No benchmark do estudo, Robula+ reduziu a fragilidade em 90% ante XPath absoluto e em 63% ante Selenium IDE.", AMBER),
    ]
    for shape_id, x, title, body, accent in studies:
        parts.extend([
            rect(shape_id, x, 1.30, 3.82, 3.72, WHITE, line=LINE),
            rect(shape_id + 1, x, 1.30, 3.82, 0.16, accent, radius="rect"),
            text_box(shape_id + 2, x + 0.28, 1.72, 3.25, 0.42, paragraph(title, 1420, accent, True, space_after=0), margin=0),
            text_box(shape_id + 3, x + 0.28, 2.42, 3.25, 1.82, paragraph(body, 1080, INK, False, space_after=0), margin=35_000),
        ])
    parts.extend([
        rect(50, 0.72, 5.27, 11.9, 0.82, "EEF8F6", line=TEAL),
        text_box(51, 0.98, 5.45, 11.35, 0.42, paragraph("Delimitação: esses estudos mostram que a estratégia de locator importa sob evolução; não provam que getByRole sempre supera CSS ou XPath.", 1050, TEAL, True, align="ctr", space_after=0), margin=0),
        text_box(
            52,
            0.82,
            6.28,
            11.7,
            0.58,
            paragraph("DOIs: 10.1109/ICST.2016.16 · 10.1109/ICST.2015.7102611 · 10.1002/smr.1771", 780, MUTED, False, align="ctr", space_after=0),
            margin=0,
        ),
        footer(10),
    ])
    return parts

STALE_CLAIMS = {
    "ppt/slides/slide8.xml": {
        "Testes gerados com especificação em linguagem natural e contexto estruturado do grafo devem apresentar maior aderência conceitual, menor alucinação de rotas/seletores e maior robustez técnica do que testes gerados apenas com a especificação textual.":
            "Hipótese a ser testada: o contexto estruturado pode alterar aderência, rotas/seletores inventados e robustez técnica; cada efeito exige medição própria.",
    },
    "ppt/slides/slide11.xml": {
        "Reduz dependência do conhecimento genérico da LLM":
            "Fornece à LLM evidências observadas além da especificação textual",
    },
    "ppt/slides/slide13.xml": {
        "Objetivo: medir o impacto do contexto. Não se pressupõe que a segunda condição seja superior.":
            "Mesma configuração nas duas condições: ChatGPT 5.6 Sol, inteligência média. Objetivo: medir somente o impacto do contexto.",
    },
    "ppt/slides/slide14.xml": {
        "A comparação final com a mesma LLM ainda será executada; artefatos-piloto não são resultados finais.":
            "Comparação executada: 24 testes, sendo 12 baseline e 12 com contexto estruturado.",
    },
    "ppt/slides/slide15.xml": {
        "waitForTimeout e seletores de risco são sinalizados.":
            "XPath, waitForTimeout e tipos de locator são contabilizados separadamente.",
    },
    "ppt/slides/slide17.xml": {
        "O benefício à LLM é uma hipótese experimental, não uma conclusão antecipada.":
            "O contexto aumentou a proporção de getBy* e a cobertura textual no grafo; a taxa de aprovação permaneceu igual e a resiliência ainda não foi testada.",
        "O contexto melhorou o grounding estático, mas não elevou a taxa de aprovação nesta amostra.":
            "O contexto aumentou a proporção de getBy* e a cobertura textual no grafo; a taxa de aprovação permaneceu igual e a resiliência ainda não foi testada.",
        "O vínculo por etapa melhora a rastreabilidade entre especificação, interface e prompt.":
            "O vínculo explícito por etapa permite rastrear especificação, evidência da interface e trecho do prompt.",
    },
    "ppt/slides/slide18.xml": {
        "Evidências para reduzir rotas e seletores inventados":
            "Evidências para identificar rotas e seletores não fundamentados",
    },
    "ppt/slides/slide20.xml": {
        "Executar a comparação controlada especificação pura × contexto estruturado.":
            "Repetir a comparação em execuções independentes para medir estabilidade e flakiness.",
        "Executar Playwright com traces e classificação de falhas.":
            "Ampliar a execução Playwright com traces e classificação semiautomática de falhas.",
        "Avaliar detecção de defeitos com versões mutantes da aplicação.":
            "Modificar controladamente as páginas e reexecutar os mesmos testes para medir resiliência.",
    },
    "ppt/slides/slide21.xml": {
        "O projeto implementa um pipeline reprodutível que transforma evidências observadas da interface em contexto estruturado por etapa; o efeito sobre os testes da LLM será medido sem pressupor superioridade.":
            "O projeto implementa um pipeline reprodutível de contexto estruturado por etapa. A geração e a execução inicial foram medidas; a resiliência será avaliada após mudanças controladas nas páginas.",
    },
}


def metric_row(
    shape_id: int,
    y: float,
    label: str,
    baseline: str,
    structured: str,
    highlight: bool = False,
) -> list[str]:
    fill = "EEF8F6" if highlight else "F7F8FA"
    return [
        rect(shape_id, 0.75, y, 7.25, 0.58, fill, line=LINE, radius="rect"),
        text_box(
            shape_id + 1,
            0.95,
            y + 0.13,
            3.0,
            0.27,
            paragraph(label, 1080, INK, highlight, space_after=0),
            margin=0,
            anchor="ctr",
        ),
        text_box(
            shape_id + 2,
            4.15,
            y + 0.13,
            1.35,
            0.27,
            paragraph(baseline, 1120, BLUE, True, align="ctr", space_after=0),
            margin=0,
            anchor="ctr",
        ),
        text_box(
            shape_id + 3,
            5.78,
            y + 0.13,
            1.85,
            0.27,
            paragraph(structured, 1120, TEAL, True, align="ctr", space_after=0),
            margin=0,
            anchor="ctr",
        ),
    ]


def comparison_results_slide() -> list[str]:
    parts = header(
        "Resultados da geração e execução inicial",
        "ChatGPT 5.6 Sol | inteligência média",
    )

    parts.extend([
        rect(10, 0.72, 1.08, 11.9, 0.75, "EEF8F6", line=TEAL),
        text_box(11, 0.98, 1.25, 11.35, 0.34, paragraph("ETAPA 1 — testes gerados e executados somente na versão atual da aplicação", 1190, TEAL, True, align="ctr", space_after=0), margin=0),
    ])

    parts.extend([
        rect(20, 0.72, 2.05, 7.68, 3.55, WHITE, line=LINE),
        text_box(21, 0.98, 2.28, 3.1, 0.30, paragraph("MEDIDAS OBSERVADAS", 1160, MUTED, True, space_after=0), margin=0),
        text_box(22, 4.50, 2.28, 1.38, 0.30, paragraph("Baseline", 1080, BLUE, True, align="ctr", space_after=0), margin=0),
        text_box(23, 6.28, 2.28, 1.70, 0.30, paragraph("Estruturado", 1080, TEAL, True, align="ctr", space_after=0), margin=0),
        rect(24, 0.92, 2.78, 7.28, 0.52, "F7F8FA", radius="rect"),
        text_box(25, 1.08, 2.92, 3.15, 0.22, paragraph("Arquivos sem erro de sintaxe", 930, INK, False, space_after=0), margin=0),
        text_box(26, 4.48, 2.89, 1.46, 0.25, paragraph("12/12", 1050, BLUE, True, align="ctr", space_after=0), margin=0),
        text_box(27, 6.26, 2.89, 1.74, 0.25, paragraph("12/12", 1050, TEAL, True, align="ctr", space_after=0), margin=0),
        text_box(28, 1.08, 3.50, 3.15, 0.22, paragraph("Aprovados na versão atual", 930, INK, False, space_after=0), margin=0),
        text_box(29, 4.48, 3.47, 1.46, 0.25, paragraph("7/12", 1050, BLUE, True, align="ctr", space_after=0), margin=0),
        text_box(30, 6.26, 3.47, 1.74, 0.25, paragraph("7/12", 1050, TEAL, True, align="ctr", space_after=0), margin=0),
        rect(31, 0.92, 3.89, 7.28, 0.52, "F7F8FA", radius="rect"),
        text_box(32, 1.08, 4.03, 3.15, 0.22, paragraph("Locators getBy* / total", 930, INK, False, space_after=0), margin=0),
        text_box(33, 4.37, 4.00, 1.68, 0.25, paragraph("81/164 (49,4%)", 950, BLUE, True, align="ctr", space_after=0), margin=0),
        text_box(34, 6.15, 4.00, 1.94, 0.25, paragraph("115/158 (72,8%)", 950, TEAL, True, align="ctr", space_after=0), margin=0),
        text_box(35, 1.08, 4.61, 3.15, 0.22, paragraph("Textos localizados no grafo", 930, INK, False, space_after=0), margin=0),
        text_box(36, 4.48, 4.58, 1.46, 0.25, paragraph("88,2%", 1050, BLUE, True, align="ctr", space_after=0), margin=0),
        text_box(37, 6.26, 4.58, 1.74, 0.25, paragraph("96,5%", 1050, TEAL, True, align="ctr", space_after=0), margin=0),
    ])

    parts.extend([
        rect(50, 8.62, 2.05, 4.0, 3.55, "F7F8FA", line=LINE),
        text_box(51, 8.92, 2.28, 3.42, 0.30, paragraph("INTERPRETAÇÃO PERMITIDA", 1160, TEAL, True, space_after=0), margin=0),
        text_box(
            52,
            8.92,
            2.87,
            3.38,
            2.75,
            paragraph("O contexto alterou características mensuráveis do código gerado.", 990, INK, False, bullet=True, space_after=280)
            + paragraph("A taxa inicial de aprovação permaneceu igual: 7/12.", 990, INK, False, bullet=True, space_after=280)
            + paragraph("Estes dados não medem nem comprovam resiliência a mudanças.", 990, RED, True, bullet=True, space_after=0),
            margin=35_000,
        ),
    ])

    parts.extend([
        rect(60, 0.72, 5.88, 11.9, 0.82, "FFF8E8", line=AMBER, radius="roundRect"),
        text_box(
            61,
            0.98,
            6.04,
            11.4,
            0.42,
            paragraph(
                "ETAPA 2 — modificar controladamente as páginas e reexecutar os testes para medir quebras, manutenção e resiliência.",
                1080,
                AMBER,
                True,
                align="ctr",
                space_after=0,
            ),
            margin=0,
        ),
        footer(NEW_SLIDE_NUMBER),
    ])
    return parts


def _insert_after_nth_slide(presentation_xml: str, slide_entry: str, index: int) -> str:
    matches = list(re.finditer(r"<p:sldId\b[^>]*/>", presentation_xml))
    if len(matches) < index:
        raise RuntimeError("A apresentação não possui slides suficientes para a inserção.")
    position = matches[index - 1].end()
    return presentation_xml[:position] + slide_entry + presentation_xml[position:]


def _set_footer_number(xml: str, new_number: int) -> str:
    pattern = re.compile(r'(name="Slide Number".*?<a:t>)\d+(</a:t>)', re.DOTALL)
    updated, count = pattern.subn(rf"\g<1>{new_number}\g<2>", xml, count=1)
    return updated if count else xml


def _replace_stale_claims(name: str, data: bytes) -> bytes:
    replacements = STALE_CLAIMS.get(name)
    if not replacements:
        return data
    text = data.decode("utf-8")
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text.encode("utf-8")


def refresh_stale_claims(path: Path = PRESENTATION) -> None:
    with ZipFile(path, "r") as source:
        results_slide_name = next(
            (
                name
                for name in source.namelist()
                if re.fullmatch(r"ppt/slides/slide\d+\.xml", name)
                and (
                    b"Resultados: baseline" in source.read(name)
                    or b"Resultados da gera" in source.read(name)
                )
            ),
            None,
        )
        with tempfile.NamedTemporaryFile(dir=path.parent, suffix=".pptm", delete=False) as temporary:
            temporary_path = Path(temporary.name)
        try:
            with ZipFile(temporary_path, "w", ZIP_DEFLATED) as target:
                for item in source.infolist():
                    data = source.read(item.filename)
                    if item.filename == results_slide_name:
                        data = slide_xml(comparison_results_slide()).encode("utf-8")
                    elif item.filename == "ppt/slides/slide9.xml":
                        data = slide_xml(theoretical_foundation_slide()).encode("utf-8")
                    elif item.filename == "ppt/slides/slide10.xml":
                        data = slide_xml(related_work_slide()).encode("utf-8")
                    target.writestr(item, _replace_stale_claims(item.filename, data))
            temporary_path.replace(path)
        finally:
            temporary_path.unlink(missing_ok=True)


def update_presentation(path: Path = PRESENTATION) -> None:
    with ZipFile(path, "r") as source:
        names = source.namelist()
        slide_numbers = [
            int(match.group(1))
            for name in names
            if (match := re.fullmatch(r"ppt/slides/slide(\d+)\.xml", name))
        ]
        new_slide_file_number = max(slide_numbers) + 1

        presentation = source.read("ppt/presentation.xml").decode("utf-8")
        slide_ids = [int(value) for value in re.findall(r'<p:sldId id="(\d+)"', presentation)]
        new_slide_id = max(slide_ids) + 1

        relationships = source.read("ppt/_rels/presentation.xml.rels").decode("utf-8")
        relationship_ids = [int(value) for value in re.findall(r'Id="rId(\d+)"', relationships)]
        new_relationship_id = max(relationship_ids) + 1

        slide_entry = f'<p:sldId id="{new_slide_id}" r:id="rId{new_relationship_id}"/>'
        presentation = _insert_after_nth_slide(presentation, slide_entry, INSERT_AFTER)

        relationship = (
            f'<Relationship Id="rId{new_relationship_id}" '
            'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" '
            f'Target="slides/slide{new_slide_file_number}.xml"/>'
        )
        relationships = relationships.replace("</Relationships>", relationship + "</Relationships>")

        content_types = source.read("[Content_Types].xml").decode("utf-8")
        slide_override = (
            f'<Override PartName="/ppt/slides/slide{new_slide_file_number}.xml" '
            'ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
        )
        content_types = content_types.replace("</Types>", slide_override + "</Types>")

        app_properties = source.read("docProps/app.xml").decode("utf-8")
        old_count = len(slide_numbers)
        app_properties = app_properties.replace(f"<Slides>{old_count}</Slides>", f"<Slides>{old_count + 1}</Slides>")

        replacements: dict[str, bytes] = {
            "ppt/presentation.xml": presentation.encode("utf-8"),
            "ppt/_rels/presentation.xml.rels": relationships.encode("utf-8"),
            "[Content_Types].xml": content_types.encode("utf-8"),
            "docProps/app.xml": app_properties.encode("utf-8"),
        }
        for slide_number in range(2, old_count + 1):
            name = f"ppt/slides/slide{slide_number}.xml"
            displayed_number = slide_number if slide_number <= INSERT_AFTER else slide_number + 1
            replacements[name] = _set_footer_number(
                source.read(name).decode("utf-8"), displayed_number
            ).encode("utf-8")
        for name in STALE_CLAIMS:
            replacements[name] = _replace_stale_claims(
                name, replacements.get(name, source.read(name))
            )

        new_slide_name = f"ppt/slides/slide{new_slide_file_number}.xml"
        new_slide_rels_name = f"ppt/slides/_rels/slide{new_slide_file_number}.xml.rels"
        new_slide_rels = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" '
            'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" '
            'Target="../slideLayouts/slideLayout1.xml"/>'
            "</Relationships>"
        ).encode("utf-8")

        with tempfile.NamedTemporaryFile(dir=path.parent, suffix=".pptm", delete=False) as temporary:
            temporary_path = Path(temporary.name)
        try:
            with ZipFile(temporary_path, "w", ZIP_DEFLATED) as target:
                for item in source.infolist():
                    target.writestr(item, replacements.get(item.filename, source.read(item.filename)))
                target.writestr(new_slide_name, slide_xml(comparison_results_slide()).encode("utf-8"))
                target.writestr(new_slide_rels_name, new_slide_rels)
            temporary_path.replace(path)
        finally:
            temporary_path.unlink(missing_ok=True)


if __name__ == "__main__":
    with ZipFile(PRESENTATION, "r") as current:
        already_inserted = any(
            (
                b"Resultados: baseline" in current.read(name)
                or b"Resultados da gera" in current.read(name)
            )
            for name in current.namelist()
            if re.fullmatch(r"ppt/slides/slide\d+\.xml", name)
        )
    if already_inserted:
        refresh_stale_claims()
        print(f"Textos relacionados aos resultados atualizados em: {PRESENTATION}")
    else:
        update_presentation()
        print(f"Slide de resultados inserido em: {PRESENTATION}")
