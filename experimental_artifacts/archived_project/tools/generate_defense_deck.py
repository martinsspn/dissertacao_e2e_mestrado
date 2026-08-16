from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape
from zipfile import ZIP_DEFLATED, ZipFile


OUT = Path("docs/apresentacao_defesa_mestrado_prompt_e2e_semantico.pptx")

NS_A = "http://schemas.openxmlformats.org/drawingml/2006/main"
NS_R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS_P = "http://schemas.openxmlformats.org/presentationml/2006/main"

SLIDE_W = 13_333_333
SLIDE_H = 7_500_000

BG = "F7F6F2"
INK = "1F2937"
MUTED = "667085"
TEAL = "0F766E"
BLUE = "2563EB"
AMBER = "F59E0B"
GREEN = "16A34A"
RED = "DC2626"
VIOLET = "7C3AED"
WHITE = "FFFFFF"
LINE = "D0D5DD"


def emu(inches: float) -> int:
    return int(inches * 914400)


def clean(text: str) -> str:
    return escape(text, {"'": "&apos;", '"': "&quot;"})


def rpr(size: int, color: str = INK, bold: bool = False, font: str = "Aptos") -> str:
    b = ' b="1"' if bold else ""
    return (
        f'<a:rPr lang="pt-BR" sz="{size}"{b}>'
        f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
        f'<a:latin typeface="{font}"/><a:cs typeface="{font}"/>'
        f"</a:rPr>"
    )


def paragraph(
    text: str,
    size: int = 2400,
    color: str = INK,
    bold: bool = False,
    bullet: bool = False,
    level: int = 0,
    align: str = "l",
    space_after: int = 600,
) -> str:
    mar_l = 360000 + level * 260000 if bullet else 0
    indent = -220000 if bullet else 0
    bullet_xml = '<a:buChar char="•"/>' if bullet else ""
    return (
        f'<a:p><a:pPr algn="{align}" marL="{mar_l}" indent="{indent}" '
        f'spAft="{space_after}">{bullet_xml}</a:pPr>'
        f"<a:r>{rpr(size, color, bold)}<a:t>{clean(text)}</a:t></a:r>"
        f'<a:endParaRPr lang="pt-BR" sz="{size}"/></a:p>'
    )


def text_box(
    shape_id: int,
    x: float,
    y: float,
    w: float,
    h: float,
    paragraphs_xml: str,
    name: str = "Text Box",
    fill: str | None = None,
    line: str | None = None,
    radius: str = "rect",
    margin: int = 80_000,
    anchor: str = "t",
) -> str:
    fill_xml = (
        f'<a:solidFill><a:srgbClr val="{fill}"/></a:solidFill>' if fill else "<a:noFill/>"
    )
    line_xml = (
        f'<a:ln w="11000"><a:solidFill><a:srgbClr val="{line}"/></a:solidFill></a:ln>'
        if line
        else "<a:ln><a:noFill/></a:ln>"
    )
    return f"""
    <p:sp>
      <p:nvSpPr>
        <p:cNvPr id="{shape_id}" name="{clean(name)}"/>
        <p:cNvSpPr txBox="1"/>
        <p:nvPr/>
      </p:nvSpPr>
      <p:spPr>
        <a:xfrm><a:off x="{emu(x)}" y="{emu(y)}"/><a:ext cx="{emu(w)}" cy="{emu(h)}"/></a:xfrm>
        <a:prstGeom prst="{radius}"><a:avLst/></a:prstGeom>
        {fill_xml}
        {line_xml}
      </p:spPr>
      <p:txBody>
        <a:bodyPr wrap="square" anchor="{anchor}" lIns="{margin}" tIns="{margin}" rIns="{margin}" bIns="{margin}"/>
        <a:lstStyle/>
        {paragraphs_xml}
      </p:txBody>
    </p:sp>
    """


def rect(
    shape_id: int,
    x: float,
    y: float,
    w: float,
    h: float,
    fill: str,
    name: str = "Rectangle",
    line: str | None = None,
    radius: str = "roundRect",
) -> str:
    line_xml = (
        f'<a:ln w="11000"><a:solidFill><a:srgbClr val="{line}"/></a:solidFill></a:ln>'
        if line
        else "<a:ln><a:noFill/></a:ln>"
    )
    return f"""
    <p:sp>
      <p:nvSpPr><p:cNvPr id="{shape_id}" name="{clean(name)}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
      <p:spPr>
        <a:xfrm><a:off x="{emu(x)}" y="{emu(y)}"/><a:ext cx="{emu(w)}" cy="{emu(h)}"/></a:xfrm>
        <a:prstGeom prst="{radius}"><a:avLst/></a:prstGeom>
        <a:solidFill><a:srgbClr val="{fill}"/></a:solidFill>
        {line_xml}
      </p:spPr>
    </p:sp>
    """


def line_shape(shape_id: int, x1: float, y1: float, x2: float, y2: float, color: str = LINE) -> str:
    x = min(x1, x2)
    y = min(y1, y2)
    w = abs(x2 - x1)
    h = abs(y2 - y1)
    flip_h = ' flipH="1"' if x2 < x1 else ""
    flip_v = ' flipV="1"' if y2 < y1 else ""
    return f"""
    <p:cxnSp>
      <p:nvCxnSpPr><p:cNvPr id="{shape_id}" name="Line"/><p:cNvCxnSpPr/><p:nvPr/></p:nvCxnSpPr>
      <p:spPr>
        <a:xfrm{flip_h}{flip_v}><a:off x="{emu(x)}" y="{emu(y)}"/><a:ext cx="{emu(w)}" cy="{emu(h)}"/></a:xfrm>
        <a:prstGeom prst="line"><a:avLst/></a:prstGeom>
        <a:ln w="22000"><a:solidFill><a:srgbClr val="{color}"/></a:solidFill><a:tailEnd type="triangle"/></a:ln>
      </p:spPr>
    </p:cxnSp>
    """


def header(title: str, subtitle: str | None = None) -> list[str]:
    parts = [
        rect(2, 0, 0, 13.333, 0.22, TEAL, "Header Bar", radius="rect"),
        text_box(
            3,
            0.55,
            0.42,
            8.5,
            0.52,
            paragraph(title, 2450, TEAL, True, space_after=0),
            name="Slide Title",
            margin=0,
        ),
    ]
    if subtitle:
        parts.append(
            text_box(
                4,
                9.05,
                0.45,
                3.65,
                0.45,
                paragraph(subtitle, 1050, MUTED, False, align="r", space_after=0),
                name="Subtitle",
                margin=0,
            )
        )
    return parts


def footer(slide_no: int) -> str:
    return text_box(
        900,
        11.75,
        7.08,
        1.0,
        0.25,
        paragraph(str(slide_no), 900, MUTED, False, align="r", space_after=0),
        name="Slide Number",
        margin=0,
    )


def bullet_block(items: list[str], size: int = 1750, color: str = INK) -> str:
    return "".join(paragraph(item, size, color, bullet=True, space_after=430) for item in items)


def card(shape_id: int, x: float, y: float, w: float, h: float, title: str, body: list[str], accent: str) -> str:
    xml = rect(shape_id, x, y, w, h, WHITE, line=LINE, radius="roundRect")
    xml += rect(shape_id + 1, x, y, 0.08, h, accent, radius="rect")
    content = paragraph(title, 1500, accent, True, space_after=360)
    content += bullet_block(body, 1120, INK)
    xml += text_box(shape_id + 2, x + 0.12, y + 0.1, w - 0.22, h - 0.18, content, margin=60_000)
    return xml


def simple_slide(title: str, bullets: list[str], subtitle: str | None = None) -> list[str]:
    parts = header(title, subtitle)
    parts.append(
        text_box(
            10,
            0.75,
            1.38,
            11.7,
            5.25,
            bullet_block(bullets, 1850),
            name="Bullets",
            fill=WHITE,
            line=LINE,
            margin=180_000,
        )
    )
    return parts


def title_slide() -> list[str]:
    return [
        rect(2, 0, 0, 13.333, 7.5, BG, radius="rect"),
        rect(3, 0, 0, 13.333, 0.28, TEAL, radius="rect"),
        rect(4, 0.65, 1.0, 1.35, 0.12, AMBER, radius="rect"),
        text_box(
            5,
            0.65,
            1.25,
            11.5,
            1.55,
            paragraph("Geração de Prompts Semânticos para Testes E2E", 3500, TEAL, True, space_after=200)
            + paragraph("com apoio de grafo navegacional", 2500, INK, False, space_after=0),
            margin=0,
        ),
        text_box(
            6,
            0.68,
            3.2,
            10.8,
            1.35,
            paragraph("Apresentação de defesa de mestrado", 1650, MUTED, False, space_after=280)
            + paragraph("Nome do discente | Orientador(a) | Programa de Pós-Graduação", 1350, INK, False, space_after=180)
            + paragraph("Universidade | 2026", 1250, MUTED, False, space_after=0),
            margin=0,
        ),
        rect(7, 0.68, 5.45, 3.15, 0.78, WHITE, line=LINE),
        text_box(
            8,
            0.82,
            5.57,
            2.85,
            0.48,
            paragraph("Problema: LLMs alucinam rotas, seletores e fluxos.", 1050, INK, False, space_after=0),
            margin=0,
        ),
        rect(9, 4.05, 5.45, 3.75, 0.78, WHITE, line=LINE),
        text_box(
            10,
            4.19,
            5.57,
            3.45,
            0.48,
            paragraph("Proposta: grounding semântico via grafo da aplicação.", 1050, INK, False, space_after=0),
            margin=0,
        ),
    ]


def agenda_slide() -> list[str]:
    items = [
        ("1", "Problema e objetivos", TEAL),
        ("2", "Fundamentação e trabalhos relacionados", BLUE),
        ("3", "Proposta e arquitetura", AMBER),
        ("4", "Metodologia de avaliação", VIOLET),
        ("5", "Resultados, contribuições e conclusão", GREEN),
    ]
    parts = header("Roteiro da Defesa")
    x = 0.8
    y = 1.35
    for i, (num, label, color) in enumerate(items):
        parts.append(rect(20 + i * 4, x, y + i * 0.95, 0.58, 0.58, color, radius="ellipse"))
        parts.append(
            text_box(
                21 + i * 4,
                x,
                y + i * 0.95 + 0.09,
                0.58,
                0.25,
                paragraph(num, 1300, WHITE, True, align="ctr", space_after=0),
                margin=0,
            )
        )
        parts.append(
            text_box(
                22 + i * 4,
                x + 0.82,
                y + i * 0.95 + 0.02,
                9.2,
                0.46,
                paragraph(label, 1750, INK, False, space_after=0),
                margin=0,
            )
        )
    return parts


def research_questions_slide() -> list[str]:
    parts = header("Perguntas de Pesquisa e Hipótese")
    parts.append(
        text_box(
            10,
            0.75,
            1.18,
            5.9,
            5.75,
            paragraph("Perguntas de pesquisa", 1600, TEAL, True, space_after=420)
            + bullet_block(
                [
                    "RQ1: prompts enriquecidos reduzem alucinações de rotas, seletores e elementos?",
                    "RQ2: o ranking aumenta a aderência ao fluxo especificado?",
                    "RQ3: a política de seletores favorece testes mais robustos e legíveis?",
                    "RQ4: qual o custo prático em tamanho, tempo e intervenção manual?",
                ],
                1180,
            ),
            fill=WHITE,
            line=LINE,
            margin=150_000,
        )
    )
    parts.append(
        text_box(
            20,
            7.0,
            1.18,
            5.55,
            5.75,
            paragraph("Hipótese", 1600, AMBER, True, space_after=460)
            + paragraph(
                "Testes gerados com especificação em linguagem natural e contexto semântico do grafo devem apresentar maior aderência conceitual, menor alucinação de rotas/seletores e maior robustez técnica do que testes gerados apenas com a especificação textual.",
                1500,
                INK,
                False,
                space_after=0,
            ),
            fill=WHITE,
            line=LINE,
            margin=170_000,
        )
    )
    return parts


def flow_slide() -> list[str]:
    parts = header("Visão Geral da Proposta", "pipeline proposto")
    steps = [
        ("Aplicação web", TEAL),
        ("Crawljax", BLUE),
        ("Grafo Neo4j", AMBER),
        ("Especificação em LN", VIOLET),
        ("Ranking + coverage", GREEN),
        ("Prompt semântico", TEAL),
        ("LLM", BLUE),
        ("Teste Playwright", AMBER),
        ("Avaliação", VIOLET),
    ]
    x0, y0 = 0.55, 1.35
    for i, (label, color) in enumerate(steps):
        row = 0 if i < 5 else 1
        col = i if i < 5 else i - 5
        x = x0 + col * 2.5
        y = y0 + row * 2.15
        parts.append(rect(20 + i * 5, x, y, 1.95, 0.85, WHITE, line=color))
        parts.append(
            text_box(
                21 + i * 5,
                x + 0.08,
                y + 0.22,
                1.8,
                0.28,
                paragraph(label, 1050, INK, True, align="ctr", space_after=0),
                margin=0,
            )
        )
        if i in {0, 1, 2, 3, 5, 6, 7}:
            parts.append(line_shape(22 + i * 5, x + 1.95, y + 0.43, x + 2.42, y + 0.43, LINE))
    parts.append(line_shape(80, 10.45, 1.78, 10.45, 3.5, LINE))
    parts.append(line_shape(81, 10.45, 3.5, 0.75, 3.5, LINE))
    parts.append(
        text_box(
            90,
            0.85,
            5.85,
            11.4,
            0.55,
            paragraph(
                "A LLM gera código, mas a fonte de verdade sobre rotas, elementos e seletores é o contexto extraído da aplicação.",
                1350,
                MUTED,
                False,
                align="ctr",
                space_after=0,
            ),
            margin=0,
        )
    )
    return parts


def architecture_slide() -> list[str]:
    parts = header("Arquitetura da Solução")
    parts.append(card(10, 0.65, 1.25, 2.9, 2.0, "Crawler", ["Exploração via Crawljax", "Coleta de páginas, textos, elementos e transições"], TEAL))
    parts.append(card(20, 3.85, 1.25, 2.9, 2.0, "Grafo", ["Persistência no Neo4j", "PageState e NAVIGATES_TO", "Base auditável"], BLUE))
    parts.append(card(30, 7.05, 1.25, 2.9, 2.0, "Gerador", ["Normalização textual", "Ranking de evidências", "Prompt estruturado"], AMBER))
    parts.append(card(40, 10.25, 1.25, 2.55, 2.0, "Avaliação", ["Análise estática", "Conformidade com grafo", "Rubrica humana"], VIOLET))
    for i, x in enumerate([3.55, 6.75, 9.95]):
        parts.append(line_shape(70 + i, x, 2.25, x + 0.27, 2.25, LINE))
    parts.append(
        text_box(
            80,
            1.2,
            4.1,
            10.9,
            1.45,
            paragraph("Decisão de escopo", 1550, TEAL, True, align="ctr", space_after=320)
            + paragraph(
                "A contribuição central é o prompt semântico, auditável e fundamentado no grafo. A geração totalmente autônoma de testes fica como extensão experimental.",
                1500,
                INK,
                False,
                align="ctr",
                space_after=0,
            ),
            fill=WHITE,
            line=LINE,
            margin=140_000,
        )
    )
    return parts


def graph_slide() -> list[str]:
    parts = header("Grafo Navegacional", "Demo Web Shop")
    metrics = [("36", "páginas/estados", TEAL), ("83", "transições", BLUE), ("5", "especificações", AMBER)]
    for i, (value, label, color) in enumerate(metrics):
        x = 0.85 + i * 4.05
        parts.append(rect(10 + i * 5, x, 1.15, 3.25, 1.4, WHITE, line=LINE))
        parts.append(
            text_box(
                11 + i * 5,
                x,
                1.33,
                3.25,
                0.38,
                paragraph(value, 2600, color, True, align="ctr", space_after=0),
                margin=0,
            )
        )
        parts.append(
            text_box(
                12 + i * 5,
                x,
                1.92,
                3.25,
                0.25,
                paragraph(label, 1050, MUTED, False, align="ctr", space_after=0),
                margin=0,
            )
        )
    parts.append(
        text_box(
            40,
            0.75,
            3.0,
            5.9,
            3.25,
            paragraph("O que é armazenado", 1500, TEAL, True, space_after=360)
            + bullet_block(["URLs e títulos de páginas", "Textos visíveis", "Elementos e atributos", "Seletores disponíveis", "Transições entre estados"], 1300),
            fill=WHITE,
            line=LINE,
            margin=150_000,
        )
    )
    parts.append(
        text_box(
            50,
            6.95,
            3.0,
            5.65,
            3.25,
            paragraph("Por que isso importa", 1500, AMBER, True, space_after=360)
            + bullet_block(["Permite rastrear evidências usadas no prompt", "Reduz dependência do conhecimento genérico da LLM", "Explicita lacunas quando o crawler não descobriu um fluxo"], 1300),
            fill=WHITE,
            line=LINE,
            margin=150_000,
        )
    )
    return parts


def coverage_slide() -> list[str]:
    parts = header("Specification Coverage", "gate de conformance")
    parts.append(
        text_box(
            10,
            0.75,
            1.1,
            11.85,
            0.85,
            paragraph(
                "A camada estima, antes da geração do teste, se cada requisito da especificação está sustentado por evidências do grafo.",
                1500,
                INK,
                False,
                align="ctr",
                space_after=0,
            ),
            fill=WHITE,
            line=LINE,
            margin=120_000,
        )
    )
    rows = [
        ("fluxo_downloads_digitais", "supported", 0.926, GREEN),
        ("fluxo_contato", "supported", 0.918, GREEN),
        ("fluxo_computadores_desktops", "partial", 0.442, AMBER),
        ("fluxo_cartao_presente_comparacao", "partial", 0.434, AMBER),
        ("user_registration_book_purchase", "low_coverage", 0.191, RED),
    ]
    y = 2.25
    for i, (name, status, score, color) in enumerate(rows):
        yy = y + i * 0.68
        parts.append(text_box(30 + i * 5, 0.95, yy, 3.7, 0.26, paragraph(name, 900, INK, False, space_after=0), margin=0))
        parts.append(rect(31 + i * 5, 4.9, yy + 0.02, 4.7, 0.22, "E5E7EB", radius="rect"))
        parts.append(rect(32 + i * 5, 4.9, yy + 0.02, 4.7 * score, 0.22, color, radius="rect"))
        parts.append(text_box(33 + i * 5, 9.9, yy - 0.01, 1.05, 0.26, paragraph(f"{score:.3f}", 900, color, True, align="r", space_after=0), margin=0))
        parts.append(text_box(34 + i * 5, 11.15, yy - 0.01, 1.25, 0.26, paragraph(status, 850, MUTED, False, align="r", space_after=0), margin=0))
    parts.append(
        text_box(
            80,
            0.95,
            6.1,
            11.4,
            0.55,
            paragraph(
                "Ponto para defender: quando há baixa cobertura, o sistema não deve estimular a LLM a inventar o fluxo; a lacuna vira evidência metodológica.",
                1250,
                MUTED,
                False,
                align="ctr",
                space_after=0,
            ),
            margin=0,
        )
    )
    return parts


def methodology_slide() -> list[str]:
    parts = header("Metodologia Experimental")
    parts.append(card(10, 0.7, 1.25, 5.75, 2.25, "Baseline", ["Prompt com especificação em linguagem natural", "Regras gerais de Playwright", "Sem evidências estruturadas da aplicação"], BLUE))
    parts.append(card(20, 6.85, 1.25, 5.75, 2.25, "Proposta", ["Prompt com páginas, transições e caminhos", "Seletores recomendados", "Coverage da especificação e avisos de lacuna"], TEAL))
    parts.append(line_shape(45, 6.48, 2.38, 6.78, 2.38, LINE))
    parts.append(
        text_box(
            50,
            0.95,
            4.35,
            11.3,
            1.3,
            paragraph("Controle experimental", 1500, AMBER, True, align="ctr", space_after=300)
            + paragraph(
                "Para cada especificação, gerar testes com a mesma LLM e comparar executabilidade, aderência ao grafo, risco de seletores e avaliação humana.",
                1350,
                INK,
                False,
                align="ctr",
                space_after=0,
            ),
            fill=WHITE,
            line=LINE,
            margin=130_000,
        )
    )
    return parts


def metrics_slide() -> list[str]:
    parts = header("Métricas de Avaliação")
    parts.append(card(10, 0.7, 1.2, 3.8, 4.9, "Automáticas", ["Import correto", "Bloco test(...)", "Presença de expect", "Ações de usuário", "Ausência de waitForTimeout"], TEAL))
    parts.append(card(25, 4.85, 1.2, 3.8, 4.9, "Conformidade", ["URLs presentes no grafo", "Textos fundamentados", "Seletores recomendados", "Itens possivelmente inventados"], BLUE))
    parts.append(card(40, 9.0, 1.2, 3.6, 4.9, "Humanas", ["Fluxo correto", "Alvo correto", "Asserção correta", "Robustez prática", "Utilidade geral"], AMBER))
    return parts


def failure_slide() -> list[str]:
    parts = header("Classificação de Falhas", "passou/falhou não basta")
    parts.append(
        text_box(
            10,
            0.85,
            1.15,
            11.6,
            0.9,
            paragraph(
                "Um teste pode falhar por revelar um comportamento ausente na aplicação. Por isso, a avaliação separa qualidade do teste, comportamento observado e causa provável da falha.",
                1350,
                INK,
                False,
                align="ctr",
                space_after=0,
            ),
            fill=WHITE,
            line=LINE,
            margin=130_000,
        )
    )
    parts.append(card(20, 0.8, 2.45, 2.8, 2.35, "application_failure", ["Teste conceitualmente correto", "Aplicação não exibiu o resultado esperado"], GREEN))
    parts.append(card(30, 3.85, 2.45, 2.8, 2.35, "generated_test_failure", ["Fluxo errado", "Seletor, rota ou asserção inventada"], RED))
    parts.append(card(40, 6.9, 2.45, 2.8, 2.35, "environment_failure", ["Rede, container, dependência", "Instabilidade externa"], BLUE))
    parts.append(card(50, 9.95, 2.45, 2.55, 2.35, "inconclusive", ["Evidência insuficiente", "Causa não separável"], AMBER))
    return parts


def results_slide() -> list[str]:
    parts = header("Resultados", "estrutura sugerida")
    parts.append(
        text_box(
            10,
            0.75,
            1.2,
            11.8,
            0.7,
            paragraph("Preencher com os resultados finais após gerar e avaliar os testes baseline e semantic_prompt.", 1350, MUTED, False, align="ctr", space_after=0),
            fill=WHITE,
            line=LINE,
            margin=100_000,
        )
    )
    labels = [("Executáveis", 0.0, BLUE), ("Com expect", 0.0, TEAL), ("URLs desconhecidas", 0.0, RED), ("Seletores alto risco", 0.0, AMBER)]
    for i, (label, _, color) in enumerate(labels):
        x = 0.95 + i * 3.0
        parts.append(rect(20 + i * 4, x, 2.45, 2.45, 2.15, WHITE, line=LINE))
        parts.append(text_box(21 + i * 4, x + 0.15, 2.75, 2.15, 0.3, paragraph(label, 1000, INK, True, align="ctr", space_after=0), margin=0))
        parts.append(text_box(22 + i * 4, x + 0.15, 3.35, 2.15, 0.45, paragraph("baseline  ×  proposta", 950, color, False, align="ctr", space_after=0), margin=0))
        parts.append(rect(23 + i * 4, x + 0.35, 4.05, 1.75, 0.16, "E5E7EB", radius="rect"))
    parts.append(
        text_box(
            60,
            1.0,
            5.55,
            11.2,
            0.65,
            paragraph("Na fala: interpretar os números. Não mostrar apenas tabela; explicar o que mudou na qualidade do teste gerado.", 1200, MUTED, False, align="ctr", space_after=0),
            margin=0,
        )
    )
    return parts


def contributions_slide() -> list[str]:
    parts = header("Contribuições da Pesquisa")
    parts.append(card(10, 0.7, 1.2, 3.8, 4.95, "Científicas", ["Grounding semântico para testes E2E", "Grafo navegacional como contexto estruturado", "Coverage da especificação como evidência"], TEAL))
    parts.append(card(25, 4.85, 1.2, 3.8, 4.95, "Técnicas", ["Pipeline Crawljax + Neo4j + Python", "Ranking de páginas, transições e caminhos", "Política de seletores e avaliação"], BLUE))
    parts.append(card(40, 9.0, 1.2, 3.6, 4.95, "Práticas", ["Apoio à criação inicial de testes", "Menos rotas e seletores inventados", "Maior auditabilidade do prompt"], AMBER))
    return parts


def final_slide() -> list[str]:
    return [
        rect(2, 0, 0, 13.333, 7.5, BG, radius="rect"),
        rect(3, 0, 0, 13.333, 0.28, TEAL, radius="rect"),
        text_box(4, 1.1, 1.35, 11.2, 0.85, paragraph("Considerações Finais", 2900, TEAL, True, align="ctr", space_after=0), margin=0),
        text_box(
            5,
            1.25,
            2.65,
            10.85,
            1.35,
            paragraph(
                "A pesquisa propõe uma forma de tornar a geração de testes E2E por LLMs mais fundamentada, auditável e aderente à aplicação real.",
                1750,
                INK,
                False,
                align="ctr",
                space_after=0,
            ),
            fill=WHITE,
            line=LINE,
            margin=150_000,
        ),
        text_box(6, 1.2, 5.25, 10.9, 0.45, paragraph("Obrigado!", 2400, TEAL, True, align="ctr", space_after=0), margin=0),
        text_box(7, 1.2, 5.85, 10.9, 0.35, paragraph("À disposição para perguntas.", 1350, MUTED, False, align="ctr", space_after=0), margin=0),
    ]


SLIDES: list[tuple[str, list[str]]] = [
    ("Capa", title_slide()),
    ("Roteiro da Defesa", agenda_slide()),
    ("Contextualização", simple_slide("Contextualização", ["Testes E2E validam fluxos completos de uso em aplicações web.", "Eles são importantes, mas caros de escrever, revisar e manter.", "LLMs ajudam na geração de código, mas não conhecem necessariamente a interface real.", "Sem contexto, o teste pode parecer plausível e ainda assim não representar o sistema."])),
    ("Problema Prático", simple_slide("Problema Prático", ["LLMs podem inventar rotas que não existem na aplicação.", "Podem usar seletores frágeis ou inexistentes.", "Podem escolher textos e elementos que não aparecem na interface.", "Podem gerar fluxos incompatíveis com a navegação real.", "A qualidade passa a depender fortemente do prompt escrito manualmente."])),
    ("Problema de Pesquisa", simple_slide("Problema de Pesquisa", ["Como fornecer contexto estruturado, extraído automaticamente da aplicação, para apoiar LLMs na geração de testes E2E mais aderentes à interface real?", "A questão central não é apenas gerar código, mas condicionar a geração por evidências verificáveis da aplicação."])),
    ("Justificativa", simple_slide("Justificativa", ["Reduzir alucinações em código de teste gerado por IA.", "Apoiar a criação inicial de suítes de regressão E2E.", "Melhorar a rastreabilidade entre especificação, interface e teste.", "Favorecer seletores mais robustos e legíveis.", "Aumentar a auditabilidade do processo de geração."])),
    ("Objetivos", simple_slide("Objetivos", ["Objetivo geral: propor e avaliar um pipeline de geração de prompts semânticos para orientar LLMs na criação de testes E2E Playwright.", "Objetivos específicos: explorar a aplicação, persistir um grafo, ranquear evidências, estimar cobertura da especificação, montar prompts e avaliar os testes gerados."])),
    ("Perguntas e Hipótese", research_questions_slide()),
    ("Fundamentação Teórica", simple_slide("Fundamentação Teórica", ["Testes E2E e automação com Playwright.", "Web crawling e modelagem de estados navegacionais.", "LLMs para geração de código e testes.", "Grounding e recuperação de contexto para reduzir alucinação.", "Robustez de seletores em testes de interface."])),
    ("Trabalhos Relacionados", simple_slide("Trabalhos Relacionados", ["Geração automática de testes para aplicações web.", "Uso de LLMs para geração de código e testes.", "Ferramentas de crawling e descoberta de estados.", "Técnicas de RAG/grounding aplicadas à engenharia de software.", "Lacuna explorada: combinar grafo navegacional semântico com geração de prompts auditáveis para E2E."])),
    ("Visão Geral", flow_slide()),
    ("Arquitetura", architecture_slide()),
    ("Grafo Navegacional", graph_slide()),
    ("Prompt Semântico", simple_slide("Prompt Semântico", ["Inclui a especificação original em linguagem natural.", "Fornece páginas, transições e caminhos candidatos relevantes.", "Apresenta seletores recomendados e distribuição de força dos seletores.", "Inclui avisos de qualidade e cobertura da especificação.", "Instrui a LLM a não inventar rotas, textos ou seletores quando houver evidência no grafo."])),
    ("Specification Coverage", coverage_slide()),
    ("Política de Seletores", simple_slide("Política de Seletores", ["Priorizar locators semânticos: getByRole, getByLabel, getByPlaceholder e getByText.", "Usar atributos estáveis, como id, name, data-testid e data-test, quando forem a melhor opção.", "Aceitar CSS curto e específico quando não houver alternativa semântica.", "Evitar XPath, nth-child, classes de layout e seletores longos.", "Classificar risco dos seletores para apoiar a avaliação."])),
    ("Metodologia", methodology_slide()),
    ("Base Experimental", simple_slide("Base Experimental", ["Aplicação alvo atual: Demo Web Shop.", "Grafo explorado: 36 páginas/estados e 83 transições.", "Cinco especificações representativas em linguagem natural.", "Fluxos avaliados: contato, downloads digitais, computadores/desktops, cartão presente/comparação, registro e compra de livro.", "Mesma LLM deve ser usada nas abordagens baseline e proposta."])),
    ("Métricas", metrics_slide()),
    ("Falhas", failure_slide()),
    ("Resultados", results_slide()),
    ("Discussão", simple_slide("Discussão", ["O grafo não substitui a LLM, mas condiciona sua geração com evidências da aplicação.", "Coverage baixo não é apenas uma falha: é informação sobre lacuna do crawler ou da especificação.", "A avaliação separa código executável, aderência semântica e causa provável de falha.", "A abordagem é útil mesmo quando impede que um fluxo não sustentado seja inventado."])),
    ("Contribuições", contributions_slide()),
    ("Limitações e Ameaças", simple_slide("Limitações e Ameaças à Validade", ["O crawler pode não descobrir todos os fluxos relevantes.", "Um único site alvo limita a generalização.", "Diferentes LLMs podem produzir resultados distintos.", "Especificações ambíguas prejudicam o alinhamento semântico.", "A análise estática baseada em padrões textuais pode deixar passar casos complexos.", "A avaliação humana pode introduzir subjetividade."])),
    ("Trabalhos Futuros", simple_slide("Trabalhos Futuros", ["Avaliar mais aplicações e domínios.", "Comparar diferentes LLMs.", "Executar testes com Playwright de forma controlada e coletar traces.", "Evoluir a análise estática para parser TypeScript.", "Melhorar a extração semântica do crawler.", "Investigar geração semiautônoma com validação iterativa."])),
    ("Final", final_slide()),
]


def slide_xml(shapes: list[str]) -> str:
    body = "\n".join(shapes)
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="{NS_A}" xmlns:r="{NS_R}" xmlns:p="{NS_P}">
  <p:cSld>
    <p:bg><p:bgPr><a:solidFill><a:srgbClr val="{BG}"/></a:solidFill><a:effectLst/></p:bgPr></p:bg>
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
      {body}
    </p:spTree>
  </p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sld>
"""


def content_types(slide_count: int) -> str:
    slide_overrides = "\n".join(
        f'<Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
        for i in range(1, slide_count + 1)
    )
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>
  <Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>
  <Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>
  <Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>
  {slide_overrides}
</Types>
"""


def root_rels() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>
"""


def presentation_xml(slide_count: int) -> str:
    ids = "\n".join(f'<p:sldId id="{255 + i}" r:id="rId{i}"/>' for i in range(1, slide_count + 1))
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presentation xmlns:a="{NS_A}" xmlns:r="{NS_R}" xmlns:p="{NS_P}" saveSubsetFonts="1">
  <p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId{slide_count + 1}"/></p:sldMasterIdLst>
  <p:sldIdLst>{ids}</p:sldIdLst>
  <p:sldSz cx="{SLIDE_W}" cy="{SLIDE_H}" type="wide"/>
  <p:notesSz cx="6858000" cy="9144000"/>
  <p:defaultTextStyle>
    <a:defPPr><a:defRPr lang="pt-BR"/></a:defPPr>
  </p:defaultTextStyle>
</p:presentation>
"""


def presentation_rels(slide_count: int) -> str:
    rels = [
        f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{i}.xml"/>'
        for i in range(1, slide_count + 1)
    ]
    rels.append(
        f'<Relationship Id="rId{slide_count + 1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>'
    )
    rels.append(
        f'<Relationship Id="rId{slide_count + 2}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="theme/theme1.xml"/>'
    )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">\n'
        + "\n".join(rels)
        + "\n</Relationships>\n"
    )


def slide_rels() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>
</Relationships>
"""


def slide_master_xml() -> str:
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldMaster xmlns:a="{NS_A}" xmlns:r="{NS_R}" xmlns:p="{NS_P}">
  <p:cSld><p:spTree>
    <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
    <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
  </p:spTree></p:cSld>
  <p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/>
  <p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst>
  <p:txStyles><p:titleStyle/><p:bodyStyle/><p:otherStyle/></p:txStyles>
</p:sldMaster>
"""


def slide_master_rels() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="../theme/theme1.xml"/>
</Relationships>
"""


def slide_layout_xml() -> str:
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldLayout xmlns:a="{NS_A}" xmlns:r="{NS_R}" xmlns:p="{NS_P}" type="blank" preserve="1">
  <p:cSld name="Blank"><p:spTree>
    <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
    <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
  </p:spTree></p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sldLayout>
"""


def slide_layout_rels() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="../slideMasters/slideMaster1.xml"/>
</Relationships>
"""


def theme_xml() -> str:
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<a:theme xmlns:a="{NS_A}" name="Defesa Mestrado">
  <a:themeElements>
    <a:clrScheme name="Custom">
      <a:dk1><a:srgbClr val="{INK}"/></a:dk1>
      <a:lt1><a:srgbClr val="{BG}"/></a:lt1>
      <a:dk2><a:srgbClr val="{TEAL}"/></a:dk2>
      <a:lt2><a:srgbClr val="{WHITE}"/></a:lt2>
      <a:accent1><a:srgbClr val="{TEAL}"/></a:accent1>
      <a:accent2><a:srgbClr val="{BLUE}"/></a:accent2>
      <a:accent3><a:srgbClr val="{AMBER}"/></a:accent3>
      <a:accent4><a:srgbClr val="{GREEN}"/></a:accent4>
      <a:accent5><a:srgbClr val="{VIOLET}"/></a:accent5>
      <a:accent6><a:srgbClr val="{RED}"/></a:accent6>
      <a:hlink><a:srgbClr val="{BLUE}"/></a:hlink>
      <a:folHlink><a:srgbClr val="{VIOLET}"/></a:folHlink>
    </a:clrScheme>
    <a:fontScheme name="Aptos">
      <a:majorFont><a:latin typeface="Aptos Display"/></a:majorFont>
      <a:minorFont><a:latin typeface="Aptos"/></a:minorFont>
    </a:fontScheme>
    <a:fmtScheme name="Clean">
      <a:fillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:fillStyleLst>
      <a:lnStyleLst><a:ln w="9525"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln></a:lnStyleLst>
      <a:effectStyleLst><a:effectStyle><a:effectLst/></a:effectStyle></a:effectStyleLst>
      <a:bgFillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:bgFillStyleLst>
    </a:fmtScheme>
  </a:themeElements>
</a:theme>
"""


def core_xml() -> str:
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>Geração de Prompts Semânticos para Testes E2E</dc:title>
  <dc:subject>Apresentação de defesa de mestrado</dc:subject>
  <dc:creator>Codex</dc:creator>
  <cp:lastModifiedBy>Codex</cp:lastModifiedBy>
  <dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified>
</cp:coreProperties>
"""


def app_xml(slide_count: int) -> str:
    titles = "".join(f"<vt:lpstr>{clean(title)}</vt:lpstr>" for title, _ in SLIDES)
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>Codex</Application>
  <PresentationFormat>Widescreen</PresentationFormat>
  <Slides>{slide_count}</Slides>
  <HeadingPairs><vt:vector size="2" baseType="variant"><vt:variant><vt:lpstr>Slides</vt:lpstr></vt:variant><vt:variant><vt:i4>{slide_count}</vt:i4></vt:variant></vt:vector></HeadingPairs>
  <TitlesOfParts><vt:vector size="{slide_count}" baseType="lpstr">{titles}</vt:vector></TitlesOfParts>
</Properties>
"""


def build() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    slide_count = len(SLIDES)
    with ZipFile(OUT, "w", ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types(slide_count))
        zf.writestr("_rels/.rels", root_rels())
        zf.writestr("docProps/core.xml", core_xml())
        zf.writestr("docProps/app.xml", app_xml(slide_count))
        zf.writestr("ppt/presentation.xml", presentation_xml(slide_count))
        zf.writestr("ppt/_rels/presentation.xml.rels", presentation_rels(slide_count))
        zf.writestr("ppt/slideMasters/slideMaster1.xml", slide_master_xml())
        zf.writestr("ppt/slideMasters/_rels/slideMaster1.xml.rels", slide_master_rels())
        zf.writestr("ppt/slideLayouts/slideLayout1.xml", slide_layout_xml())
        zf.writestr("ppt/slideLayouts/_rels/slideLayout1.xml.rels", slide_layout_rels())
        zf.writestr("ppt/theme/theme1.xml", theme_xml())
        for i, (_, shapes) in enumerate(SLIDES, start=1):
            full_shapes = shapes + ([footer(i)] if i not in {1, slide_count} else [])
            zf.writestr(f"ppt/slides/slide{i}.xml", slide_xml(full_shapes))
            zf.writestr(f"ppt/slides/_rels/slide{i}.xml.rels", slide_rels())
    print(OUT)


if __name__ == "__main__":
    build()
