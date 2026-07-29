from __future__ import annotations

import argparse
import os
import re
from pathlib import Path

from avaliacao_prompts.application.evaluate_test import evaluate_test_file
from avaliacao_prompts.domain.models import EvaluationCase
from avaliacao_prompts.infrastructure.markdown_reports import MarkdownEvaluationReportWriter
from avaliacao_prompts.infrastructure.neo4j_graph import Neo4jGraphEvidenceReader
from avaliacao_prompts.infrastructure.playwright_results import read_playwright_json


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="avaliar-prompts",
        description="Gera um relatório Markdown legível para apoiar a análise de testes E2E gerados.",
    )
    parser.add_argument("--tests-dir", type=Path, required=True, help="Diretório com arquivos .spec.ts")
    parser.add_argument(
        "--approach",
        choices=["baseline", "structured_context"],
        default="structured_context",
        help="Abordagem usada para gerar os testes",
    )
    parser.add_argument(
        "--base-url",
        default=os.getenv("PROMPT_E2E_BASE_URL", "https://demowebshop.tricentis.com/"),
        help="URL base da aplicação alvo",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("relatorios/relatorio_avaliacao.md"),
        help="Arquivo Markdown de saída",
    )
    parser.add_argument("--prompt-dir", type=Path, default=None, help="Diretório opcional com prompts .prompt.md")
    parser.add_argument(
        "--specs-dir",
        type=Path,
        default=None,
        help="Diretório opcional com especificações .txt usadas como entrada do baseline",
    )
    parser.add_argument(
        "--playwright-results",
        type=Path,
        action="append",
        default=[],
        help="JSON técnico do Playwright; pode ser repetido e o último resultado prevalece",
    )
    parser.add_argument("--skip-graph", action="store_true", help="Executa apenas análise estática, sem consultar Neo4j")
    parser.add_argument("--neo4j-uri", default=os.getenv("NEO4J_URI", "bolt://neo4j:7687"))
    parser.add_argument("--neo4j-user", default=os.getenv("NEO4J_USER", "neo4j"))
    parser.add_argument("--neo4j-password", default=os.getenv("NEO4J_PASSWORD", "neo4j_password"))
    parser.add_argument(
        "--neo4j-ready-timeout-seconds",
        type=int,
        default=int(os.getenv("NEO4J_READY_TIMEOUT_SECONDS", "60")),
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    test_files = sorted(args.tests_dir.resolve().glob("*.spec.ts"))
    if not test_files:
        print(f"[avaliar-prompts] Nenhum arquivo .spec.ts encontrado em {args.tests_dir}.")
        return 0

    graph = None
    if not args.skip_graph:
        reader = Neo4jGraphEvidenceReader(
            uri=args.neo4j_uri,
            user=args.neo4j_user,
            password=args.neo4j_password,
            ready_timeout_seconds=args.neo4j_ready_timeout_seconds,
        )
        try:
            graph = reader.read()
        finally:
            reader.close()

    execution_results = {}
    for results_path in args.playwright_results:
        execution_results.update(read_playwright_json(results_path))
    reports = [
        evaluate_test_file(
            EvaluationCase(
                spec_id=_spec_id_for(test_file),
                approach=args.approach,
                test_file=test_file,
                base_url=args.base_url,
                prompt_file=(
                    _spec_file_for(args.specs_dir, test_file)
                    if args.approach == "baseline"
                    else _prompt_file_for(args.prompt_dir, test_file, args.approach)
                ),
            ),
            graph=graph,
        )
        for test_file in test_files
    ]
    if execution_results:
        from dataclasses import replace

        reports = [
            replace(report, execution=execution_results.get(report.case.test_file.resolve(), report.execution))
            for report in reports
        ]
    output = MarkdownEvaluationReportWriter().write(args.output, reports)
    print(f"[avaliar-prompts] {len(reports)} teste(s) analisado(s) -> {output}")
    if args.skip_graph:
        print("[avaliar-prompts] Conformidade com o grafo não analisada (--skip-graph).")
    return 0


def _spec_id_for(test_file: Path) -> str:
    return test_file.name.removesuffix(".spec.ts")


def _prompt_file_for(prompt_dir: Path | None, test_file: Path, approach: str) -> Path | None:
    if prompt_dir is None or approach == "baseline":
        return None
    prompt_file = prompt_dir / f"{_spec_id_for(test_file)}.{approach}.prompt.md"
    if prompt_file.exists():
        return prompt_file.resolve()

    alias = _suite_alias(_spec_id_for(test_file))
    if alias:
        alias_path = prompt_dir / f"{alias}.{approach}.prompt.md"
        if alias_path.exists():
            return alias_path.resolve()

    candidates = sorted(prompt_dir.glob(f"*.{approach}.prompt.md"))
    if not candidates:
        return None
    test_terms = _identifier_terms(_spec_id_for(test_file))
    ranked = sorted(
        ((_term_similarity(test_terms, _identifier_terms(candidate.name)), candidate) for candidate in candidates),
        key=lambda item: (item[0], item[1].name),
        reverse=True,
    )
    best_score, best = ranked[0]
    if best_score <= 0 or (len(ranked) > 1 and best_score == ranked[1][0]):
        return None
    return best.resolve()


def _spec_file_for(specs_dir: Path | None, test_file: Path) -> Path | None:
    if specs_dir is None:
        return None
    exact_path = specs_dir / f"{_spec_id_for(test_file)}.txt"
    if exact_path.exists():
        return exact_path.resolve()
    alias = _suite_alias(_spec_id_for(test_file))
    candidates = sorted(specs_dir.glob("suite_*.txt"))
    if alias:
        alias_path = specs_dir / f"{alias}.txt"
        if alias_path.exists():
            return alias_path.resolve()
    test_terms = _identifier_terms(_spec_id_for(test_file))
    ranked = sorted(
        ((_term_similarity(test_terms, _identifier_terms(candidate.name)), candidate) for candidate in candidates),
        key=lambda item: (item[0], item[1].name),
        reverse=True,
    )
    if not ranked or ranked[0][0] <= 0 or (len(ranked) > 1 and ranked[0][0] == ranked[1][0]):
        return None
    return ranked[0][1].resolve()


def _suite_alias(spec_id: str) -> str | None:
    aliases = {
        "teste_wishlist_estruturado": "suite_adicionar_wishlist",
        "teste_wishlist_baseline": "suite_adicionar_wishlist",
        "teste_buscar_blue_jeans_estruturado": "suite_busca_blue_jeans",
        "teste_buscar_blue_jeans_baseline": "suite_busca_blue_jeans",
    }
    return aliases.get(spec_id)


def _identifier_terms(value: str) -> set[str]:
    ignored = {"teste", "suite", "estruturado", "structured", "context", "prompt", "spec", "ts", "md"}
    return {
        term
        for term in re.findall(r"[a-z0-9]+", value.lower())
        if term not in ignored
    }


def _term_similarity(left: set[str], right: set[str]) -> float:
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)
