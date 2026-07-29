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
            f"{result['spec']} [{result['approach']}] -> {result['output']} "
            f"({result['requirements']} etapas, {result['context_items']} itens de contexto, "
            f"{result['characters']} caracteres)"
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
    )


if __name__ == "__main__":
    raise SystemExit(main())
