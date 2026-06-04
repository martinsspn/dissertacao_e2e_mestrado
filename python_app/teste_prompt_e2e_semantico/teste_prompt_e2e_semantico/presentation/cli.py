from __future__ import annotations

import argparse
from pathlib import Path

from teste_prompt_e2e_semantico.application.generate_prompts import GeneratePromptsUseCase
from teste_prompt_e2e_semantico.config import PromptGeneratorConfig
from teste_prompt_e2e_semantico.infrastructure.filesystem_prompts import FileSystemPromptWriter
from teste_prompt_e2e_semantico.infrastructure.filesystem_specs import FileSystemSpecRepository
from teste_prompt_e2e_semantico.infrastructure.neo4j_graph_repository import Neo4jNavigationGraphRepository


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="prompt-e2e",
        description="Gera prompts estruturados para testes Playwright a partir de especificacoes em LN e Neo4j.",
    )
    parser.add_argument("--specs-dir", type=Path, default=None, help="Diretorio com arquivos .txt de especificacao")
    parser.add_argument("--output-dir", type=Path, default=None, help="Diretorio de saida para os prompts gerados")
    parser.add_argument("--base-url", type=str, default=None, help="URL base da aplicacao alvo")
    parser.add_argument("--neo4j-uri", type=str, default=None, help="URI Bolt do Neo4j")
    parser.add_argument("--neo4j-user", type=str, default=None, help="Usuario do Neo4j")
    parser.add_argument("--neo4j-password", type=str, default=None, help="Senha do Neo4j")
    parser.add_argument("--graph-max-edges", type=int, default=None, help="Maximo de transicoes lidas do grafo")
    parser.add_argument("--relevant-pages-limit", type=int, default=None, help="Maximo de paginas relevantes no prompt")
    parser.add_argument(
        "--relevant-transitions-limit",
        type=int,
        default=None,
        help="Maximo de transicoes relevantes no prompt",
    )
    parser.add_argument("--candidate-paths-limit", type=int, default=None, help="Maximo de caminhos candidatos")
    parser.add_argument("--max-path-depth", type=int, default=None, help="Profundidade maxima dos caminhos candidatos")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    config = _build_config(args)
    graph_repository = Neo4jNavigationGraphRepository(config)
    use_case = GeneratePromptsUseCase(
        spec_repository=FileSystemSpecRepository(),
        graph_repository=graph_repository,
        prompt_writer=FileSystemPromptWriter(),
        base_url=config.base_url,
        graph_max_edges=config.graph_max_edges,
        relevant_pages_limit=config.relevant_pages_limit,
        relevant_transitions_limit=config.relevant_transitions_limit,
        candidate_paths_limit=config.candidate_paths_limit,
        max_path_depth=config.max_path_depth,
    )

    try:
        results = use_case.execute(config.specs_dir, config.output_dir)
    finally:
        graph_repository.close()

    if not results:
        print("[prompt-e2e] Nenhuma especificacao .txt encontrada.")
        return 0

    for result in results:
        print(
            "[prompt-e2e] "
            f"{result['spec']} -> {result['output']} "
            f"({result['relevant_pages']} paginas, {result['relevant_transitions']} transicoes, "
            f"{result['candidate_paths']} caminhos)"
        )
    return 0


def _build_config(args: argparse.Namespace) -> PromptGeneratorConfig:
    base_config = PromptGeneratorConfig()
    return PromptGeneratorConfig(
        neo4j_uri=args.neo4j_uri or base_config.neo4j_uri,
        neo4j_user=args.neo4j_user or base_config.neo4j_user,
        neo4j_password=args.neo4j_password or base_config.neo4j_password,
        neo4j_ready_timeout_seconds=base_config.neo4j_ready_timeout_seconds,
        base_url=args.base_url or base_config.base_url,
        specs_dir=args.specs_dir or base_config.specs_dir,
        output_dir=args.output_dir or base_config.output_dir,
        graph_max_edges=args.graph_max_edges or base_config.graph_max_edges,
        relevant_pages_limit=args.relevant_pages_limit or base_config.relevant_pages_limit,
        relevant_transitions_limit=args.relevant_transitions_limit or base_config.relevant_transitions_limit,
        candidate_paths_limit=args.candidate_paths_limit or base_config.candidate_paths_limit,
        max_path_depth=args.max_path_depth or base_config.max_path_depth,
    )


if __name__ == "__main__":
    raise SystemExit(main())
