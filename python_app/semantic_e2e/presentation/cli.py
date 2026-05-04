from __future__ import annotations

import argparse
from pathlib import Path

from semantic_e2e.application.generate_tests import GenerateTestsUseCase
from semantic_e2e.config import GeneratorConfig
from semantic_e2e.infrastructure.filesystem_specs import FileSystemSpecRepository
from semantic_e2e.infrastructure.filesystem_tests import FileSystemGeneratedTestWriter
from semantic_e2e.infrastructure.neo4j_graph_repository import Neo4jNavigationGraphRepository
from semantic_e2e.infrastructure.openai_test_generator import OpenAITestGenerator


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="semantic-e2e",
        description="Gera testes Playwright a partir de especificacoes em linguagem natural e Neo4j.",
    )
    parser.add_argument("--specs-dir", type=Path, default=None, help="Diretorio com arquivos .txt de especificacao")
    parser.add_argument("--output-dir", type=Path, default=None, help="Diretorio de saida para os testes gerados")
    parser.add_argument("--base-url", type=str, default=None, help="URL base da aplicacao alvo")
    parser.add_argument("--neo4j-uri", type=str, default=None, help="URI Bolt do Neo4j")
    parser.add_argument("--neo4j-user", type=str, default=None, help="Usuario do Neo4j")
    parser.add_argument("--neo4j-password", type=str, default=None, help="Senha do Neo4j")
    parser.add_argument("--openai-base-url", type=str, default=None, help="URL base da API OpenAI-compatible")
    parser.add_argument("--llm-model", type=str, default=None, help="Modelo usado para gerar os testes")
    parser.add_argument("--graph-max-edges", type=int, default=None, help="Maximo de transicoes enviadas como contexto")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    config = _build_config(args)
    graph_repository = Neo4jNavigationGraphRepository(config)
    use_case = GenerateTestsUseCase(
        spec_repository=FileSystemSpecRepository(),
        graph_repository=graph_repository,
        test_generator=OpenAITestGenerator(config),
        test_writer=FileSystemGeneratedTestWriter(),
        graph_max_edges=config.graph_max_edges,
    )

    try:
        results = use_case.execute(config.specs_dir, config.output_dir)
    finally:
        graph_repository.close()

    for result in results:
        print(f"[semantic-e2e] {result['spec']} -> {result['output']} ({result['model']})")
    return 0


def _build_config(args: argparse.Namespace) -> GeneratorConfig:
    base_config = GeneratorConfig()
    return GeneratorConfig(
        neo4j_uri=args.neo4j_uri or base_config.neo4j_uri,
        neo4j_user=args.neo4j_user or base_config.neo4j_user,
        neo4j_password=args.neo4j_password or base_config.neo4j_password,
        base_url=args.base_url or base_config.base_url,
        specs_dir=args.specs_dir or base_config.specs_dir,
        output_dir=args.output_dir or base_config.output_dir,
        openai_api_key=base_config.openai_api_key,
        openai_base_url=args.openai_base_url or base_config.openai_base_url,
        llm_model=args.llm_model or base_config.llm_model,
        llm_timeout_seconds=base_config.llm_timeout_seconds,
        graph_max_edges=args.graph_max_edges or base_config.graph_max_edges,
    )


if __name__ == "__main__":
    raise SystemExit(main())
