from __future__ import annotations

import argparse
from pathlib import Path

from teste_prompt_e2e_semantico.config import PromptGeneratorConfig
from teste_prompt_e2e_semantico.evaluation.application.evaluate_test import evaluate_test_file
from teste_prompt_e2e_semantico.evaluation.domain.models import EvaluationCase
from teste_prompt_e2e_semantico.evaluation.infrastructure.filesystem_reports import FileSystemEvaluationReportWriter
from teste_prompt_e2e_semantico.infrastructure.neo4j_graph_repository import Neo4jNavigationGraphRepository


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="evaluate-e2e",
        description="Gera relatorio automatico de avaliacao para testes Playwright gerados.",
    )
    parser.add_argument("--tests-dir", type=Path, required=True, help="Diretorio com arquivos .spec.ts")
    parser.add_argument(
        "--approach",
        choices=["baseline", "semantic_prompt"],
        default="semantic_prompt",
        help="Abordagem usada para gerar os testes",
    )
    parser.add_argument("--base-url", type=str, default=None, help="URL base da aplicacao alvo")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("evaluation_reports/evaluation_report.json"),
        help="Arquivo JSON de saida",
    )
    parser.add_argument("--prompt-dir", type=Path, default=None, help="Diretorio opcional com prompts .prompt.md")
    parser.add_argument("--skip-graph", action="store_true", help="Executa apenas analise estatica, sem consultar Neo4j")
    parser.add_argument("--graph-max-edges", type=int, default=None, help="Maximo de transicoes lidas do Neo4j")
    parser.add_argument("--neo4j-uri", type=str, default=None, help="URI Bolt do Neo4j")
    parser.add_argument("--neo4j-user", type=str, default=None, help="Usuario do Neo4j")
    parser.add_argument("--neo4j-password", type=str, default=None, help="Senha do Neo4j")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    config = _build_config(args)
    test_files = _list_test_files(args.tests_dir)
    if not test_files:
        print(f"[evaluate-e2e] Nenhum arquivo .spec.ts encontrado em {args.tests_dir}.")
        return 0

    graph = None
    graph_repository = None
    if not args.skip_graph:
        graph_repository = Neo4jNavigationGraphRepository(config)
        try:
            graph = graph_repository.get_navigation_graph(config.graph_max_edges)
        finally:
            graph_repository.close()

    reports = [
        evaluate_test_file(
            EvaluationCase(
                spec_id=_spec_id_for(test_file),
                approach=args.approach,
                test_file=test_file,
                base_url=config.base_url,
                prompt_file=_prompt_file_for(args.prompt_dir, test_file),
            ),
            graph=graph,
        )
        for test_file in test_files
    ]

    output_path = FileSystemEvaluationReportWriter().write_json(args.output, reports)
    print(f"[evaluate-e2e] {len(reports)} testes avaliados -> {output_path}")
    if args.skip_graph:
        print("[evaluate-e2e] Conformidade com grafo ignorada (--skip-graph).")
    return 0


def _build_config(args: argparse.Namespace) -> PromptGeneratorConfig:
    base_config = PromptGeneratorConfig()
    return PromptGeneratorConfig(
        neo4j_uri=args.neo4j_uri or base_config.neo4j_uri,
        neo4j_user=args.neo4j_user or base_config.neo4j_user,
        neo4j_password=args.neo4j_password or base_config.neo4j_password,
        neo4j_ready_timeout_seconds=base_config.neo4j_ready_timeout_seconds,
        base_url=args.base_url or base_config.base_url,
        specs_dir=base_config.specs_dir,
        output_dir=base_config.output_dir,
        graph_max_edges=args.graph_max_edges or base_config.graph_max_edges,
        relevant_pages_limit=base_config.relevant_pages_limit,
        relevant_transitions_limit=base_config.relevant_transitions_limit,
        candidate_paths_limit=base_config.candidate_paths_limit,
        max_path_depth=base_config.max_path_depth,
    )


def _list_test_files(tests_dir: Path) -> list[Path]:
    return sorted(tests_dir.resolve().glob("*.spec.ts"))


def _spec_id_for(test_file: Path) -> str:
    name = test_file.name
    return name.removesuffix(".spec.ts")


def _prompt_file_for(prompt_dir: Path | None, test_file: Path) -> Path | None:
    if prompt_dir is None:
        return None
    prompt_file = prompt_dir / f"{_spec_id_for(test_file)}.prompt.md"
    return prompt_file.resolve() if prompt_file.exists() else None


if __name__ == "__main__":
    raise SystemExit(main())
