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
INSERT_AFTER = 16
DISPLAYED_SLIDE_NUMBER = 17
SLIDE_MARKER = "Resultados com páginas modificadas"

STALE_REPLACEMENTS = {
    "ppt/slides/slide18.xml": {
        "O contexto aumentou a proporção de getBy* e a cobertura textual no grafo; a taxa de aprovação permaneceu igual e a resiliência ainda não foi testada.":
            "A rodada exploratória de páginas modificadas favoreceu o contexto estruturado apenas na troca do botão de busca; o resultado ainda não permite generalização.",
    },
    "ppt/slides/slide21.xml": {
        "Modificar controladamente as páginas e reexecutar os mesmos testes para medir resiliência.":
            "Ampliar as mutações para mais componentes e repetições, controlando dependências entre cenários.",
    },
    "ppt/slides/slide22.xml": {
        "O projeto implementa um pipeline reprodutível de contexto estruturado por etapa. A geração e a execução inicial foram medidas; a resiliência será avaliada após mudanças controladas nas páginas.":
            "O projeto implementa um pipeline reprodutível de contexto estruturado por etapa. A geração, a execução inicial e uma rodada exploratória com páginas modificadas foram avaliadas, sem afirmar superioridade geral.",
    },
}


def resilience_results_slide() -> list[str]:
    parts = header(
        SLIDE_MARKER,
        "ChatGPT 5.6 Sol | inteligência média | rodada exploratória de mutações controladas",
    )

    parts.extend([
        rect(10, 0.72, 1.02, 11.9, 0.72, "EEF8F6", line=TEAL),
        text_box(
            11,
            0.93,
            1.17,
            11.48,
            0.36,
            paragraph(
                "Rodada inicial: 12 cenários → 4 elegíveis → 8 mutações → 5 pares válidos   |   Rodada adicional: 3 mudanças de atributo → 2 pares válidos",
                970,
                TEAL,
                True,
                align="ctr",
                space_after=0,
            ),
            margin=0,
        ),
    ])

    parts.extend([
        rect(20, 0.72, 1.97, 4.06, 3.78, WHITE, line=LINE),
        rect(21, 0.72, 1.97, 4.06, 0.10, BLUE, radius="rect"),
        text_box(22, 1.00, 2.24, 3.50, 0.34, paragraph("MUTAÇÕES APLICADAS", 1190, BLUE, True, space_after=0), margin=0),
        text_box(
            23,
            1.00,
            2.72,
            3.48,
            2.70,
            paragraph("Rodada inicial", 880, BLUE, True, space_after=130)
            + paragraph("3× inserir elemento antes do controle", 820, INK, False, bullet=True, space_after=105)
            + paragraph("1× envolver campo em novo contêiner", 820, INK, False, bullet=True, space_after=105)
            + paragraph("3× trocar input por button", 820, INK, False, bullet=True, space_after=105)
            + paragraph("1× alterar id de “Add to cart”", 820, INK, False, bullet=True, space_after=180)
            + paragraph("Rodada adicional", 880, TEAL, True, space_after=130)
            + paragraph("alterar id do campo de busca", 820, INK, False, bullet=True, space_after=105)
            + paragraph("alterar classe do campo de busca", 820, INK, False, bullet=True, space_after=105)
            + paragraph("alterar classe do botão de busca", 820, INK, False, bullet=True, space_after=0),
            margin=35_000,
        ),
    ])

    parts.extend([
        rect(30, 4.98, 1.97, 4.08, 3.78, WHITE, line=LINE),
        rect(31, 4.98, 1.97, 4.08, 0.10, TEAL, radius="rect"),
        text_box(32, 5.26, 2.24, 3.50, 0.34, paragraph("RESULTADOS OBSERVADOS", 1190, TEAL, True, space_after=0), margin=0),
        rect(33, 5.24, 2.78, 3.56, 1.15, "F7F8FA", line=LINE),
        text_box(34, 5.43, 2.90, 3.18, 0.88, paragraph("Estrutura: inserir elemento / contêiner", 820, INK, True, align="ctr", space_after=90) + paragraph("2/2: ambos passaram", 970, GREEN, True, align="ctr", space_after=80) + paragraph("input → button: baseline 0/3 | estruturado 3/3", 800, TEAL, True, align="ctr", space_after=0), margin=0),
        rect(35, 5.24, 4.10, 3.56, 1.35, "EEF8F6", line=TEAL),
        text_box(36, 5.43, 4.22, 3.18, 1.08, paragraph("Classe do campo: ambos passaram", 830, GREEN, True, align="ctr", space_after=100) + paragraph("Classe do botão: baseline falhou; estruturado passou", 830, TEAL, True, align="ctr", space_after=100) + paragraph("Id do campo: mutação inválida — quebrou o autocomplete da página", 790, RED, True, align="ctr", space_after=0), margin=0),
        text_box(37, 5.24, 5.51, 3.56, 0.18, paragraph("3 mutações iniciais não eram aplicáveis ao par.", 740, MUTED, False, align="ctr", space_after=0), margin=0),
    ])

    parts.extend([
        rect(40, 9.26, 1.97, 3.36, 3.78, "F7F8FA", line=LINE),
        rect(41, 9.26, 1.97, 3.36, 0.10, AMBER, radius="rect"),
        text_box(42, 9.53, 2.24, 2.84, 0.34, paragraph("POR QUE HOUVE DIFERENÇA?", 1120, AMBER, True, space_after=0), margin=0),
        text_box(
            43,
            9.53,
            2.74,
            2.82,
            2.60,
            paragraph("Baseline dependia de input.search-box-button.", 850, INK, False, bullet=True, space_after=190)
            + paragraph("Trocar a tag ou a classe impediu esse locator de encontrar o botão.", 850, RED, False, bullet=True, space_after=190)
            + paragraph("O estruturado usava papel “button” e nome “Search”, que foram preservados.", 850, TEAL, True, bullet=True, space_after=190)
            + paragraph("Mudar uma classe não usada pelos locators não causou quebra.", 850, INK, False, bullet=True, space_after=0),
            margin=35_000,
        ),
    ])

    parts.extend([
        rect(50, 0.72, 5.98, 11.9, 0.72, "FFF8E8", line=AMBER, radius="roundRect"),
        text_box(
            51,
            0.94,
            6.10,
            11.46,
            0.45,
            paragraph(
                "Limite: mudanças concentradas no controle de busca, uma repetição e amostra pequena. A primeira rodada teve p = 0,25; os resultados são descritivos e não comprovam superioridade geral.",
                850,
                AMBER,
                True,
                align="ctr",
                space_after=0,
            ),
            margin=0,
        ),
        footer(DISPLAYED_SLIDE_NUMBER),
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


def update_presentation(path: Path = PRESENTATION) -> None:
    with ZipFile(path, "r") as source:
        existing = [
            name
            for name in source.namelist()
            if re.fullmatch(r"ppt/slides/slide\d+\.xml", name)
            and SLIDE_MARKER.encode("utf-8") in source.read(name)
        ]
        if existing:
            replacement = {existing[0]: slide_xml(resilience_results_slide()).encode("utf-8")}
            for name, substitutions in STALE_REPLACEMENTS.items():
                replacement[name] = _replace_text(source.read(name), substitutions)
            _rewrite(path, source, replacement)
            return

        slide_numbers = [
            int(match.group(1))
            for name in source.namelist()
            if (match := re.fullmatch(r"ppt/slides/slide(\d+)\.xml", name))
        ]
        old_count = len(slide_numbers)
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
        override = (
            f'<Override PartName="/ppt/slides/slide{new_slide_file_number}.xml" '
            'ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
        )
        content_types = content_types.replace("</Types>", override + "</Types>")

        app_properties = source.read("docProps/app.xml").decode("utf-8")
        app_properties = app_properties.replace(
            f"<Slides>{old_count}</Slides>", f"<Slides>{old_count + 1}</Slides>"
        )

        replacements: dict[str, bytes] = {
            "ppt/presentation.xml": presentation.encode("utf-8"),
            "ppt/_rels/presentation.xml.rels": relationships.encode("utf-8"),
            "[Content_Types].xml": content_types.encode("utf-8"),
            "docProps/app.xml": app_properties.encode("utf-8"),
        }
        for name, substitutions in STALE_REPLACEMENTS.items():
            replacements[name] = _replace_text(source.read(name), substitutions)
        for position in range(INSERT_AFTER + 1, old_count + 1):
            name = f"ppt/slides/slide{position}.xml"
            replacements[name] = _set_footer_number(
                source.read(name).decode("utf-8"), position + 1
            ).encode("utf-8")

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

        replacements[new_slide_name] = slide_xml(resilience_results_slide()).encode("utf-8")
        replacements[new_slide_rels_name] = new_slide_rels
        _rewrite(path, source, replacements)


def _replace_text(data: bytes, substitutions: dict[str, str]) -> bytes:
    text = data.decode("utf-8")
    for old, new in substitutions.items():
        text = text.replace(old, new)
    return text.encode("utf-8")


def _rewrite(path: Path, source: ZipFile, replacements: dict[str, bytes]) -> None:
    with tempfile.NamedTemporaryFile(dir=path.parent, suffix=".pptm", delete=False) as temporary:
        temporary_path = Path(temporary.name)
    try:
        with ZipFile(temporary_path, "w", ZIP_DEFLATED) as target:
            written = set()
            for item in source.infolist():
                target.writestr(item, replacements.get(item.filename, source.read(item.filename)))
                written.add(item.filename)
            for name, data in replacements.items():
                if name not in written:
                    target.writestr(name, data)
        temporary_path.replace(path)
    finally:
        temporary_path.unlink(missing_ok=True)


if __name__ == "__main__":
    update_presentation()
    print(f"Slide de mutações inserido/atualizado em: {PRESENTATION}")
