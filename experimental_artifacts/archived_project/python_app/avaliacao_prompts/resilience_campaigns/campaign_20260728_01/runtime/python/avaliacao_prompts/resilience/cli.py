from __future__ import annotations

import argparse
import json
from pathlib import Path

from avaliacao_prompts.resilience.execution import prepare_execution
from avaliacao_prompts.resilience.plan import build_plan, verify_plan, write_plan
from avaliacao_prompts.resilience.run import execute_eligibility, execute_experiment


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="avaliar-resiliencia")
    subparsers = parser.add_subparsers(dest="command", required=True)
    plan = subparsers.add_parser("plan", help="Gera o plano sem ler testes ou resultados")
    plan.add_argument("--specs-dir", type=Path, required=True)
    plan.add_argument("--prompt-dir", type=Path, required=True)
    plan.add_argument("--output", type=Path, required=True)
    verify = subparsers.add_parser("verify-plan", help="Verifica o hash interno de um plano congelado")
    verify.add_argument("plan", type=Path)
    prepare = subparsers.add_parser(
        "prepare-execution",
        help="Cria cópias instrumentadas e pareadas sem executar o site",
    )
    prepare.add_argument("--baseline-dir", type=Path, required=True)
    prepare.add_argument("--structured-dir", type=Path, required=True)
    prepare.add_argument("--fixture", type=Path, required=True)
    prepare.add_argument("--plan", type=Path, required=True)
    prepare.add_argument("--output-dir", type=Path, required=True)
    prepare.add_argument("--allowlist", type=Path, required=True)
    prepare.add_argument("--semantic-review", type=Path, required=True)
    prepare.add_argument("--track-id", choices=("P", "R"), required=True)
    prepare.add_argument("--model-id", required=True)
    eligibility = subparsers.add_parser(
        "eligibility",
        help="Executa e congela somente as repetições na interface original",
    )
    eligibility.add_argument("--execution-manifest", type=Path, required=True)
    eligibility.add_argument("--playwright-config", type=Path, required=True)
    eligibility.add_argument("--node-project-dir", type=Path, required=True)
    eligibility.add_argument("--output-dir", type=Path, required=True)
    eligibility.add_argument("--repetitions", type=int, default=3)
    eligibility.add_argument("--execute-live-site", action="store_true")
    run = subparsers.add_parser("run", help="Executa o protocolo pareado sobre o site público")
    run.add_argument("--execution-manifest", type=Path, required=True)
    run.add_argument("--eligibility-results", type=Path, required=True)
    run.add_argument("--playwright-config", type=Path, required=True)
    run.add_argument("--node-project-dir", type=Path, required=True)
    run.add_argument("--control-test", type=Path, required=True)
    run.add_argument("--output-dir", type=Path, required=True)
    run.add_argument("--repetitions", type=int, default=3)
    run.add_argument("--mutation", action="append", default=[])
    run.add_argument(
        "--scenario",
        action="append",
        default=[],
        help="Limita a execução aos IDs de cenário informados (opção repetível).",
    )
    run.add_argument(
        "--mutations-per-scenario",
        type=int,
        choices=(1, 2),
        help=(
            "Executa uma amostra deterministica de 1 ou 2 mutacoes neutras (E1/E2) "
            "por cenario elegivel. Nao pode ser combinada com --mutation."
        ),
    )
    run.add_argument(
        "--execute-live-site",
        action="store_true",
        help="Confirma explicitamente requisições e efeitos de estado no site público.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "plan":
        payload = build_plan(args.specs_dir, args.prompt_dir)
        output = write_plan(args.output, payload)
        print(f"[avaliar-resiliencia] Plano: {output}")
        print(f"[avaliar-resiliencia] Catálogo: {payload['catalog_size']} alvos")
        print(f"[avaliar-resiliencia] Mutações: {payload['mutation_count']}")
        print(f"[avaliar-resiliencia] SHA-256: {payload['plan_sha256']}")
        return 0
    if args.command == "verify-plan":
        payload = json.loads(args.plan.read_text(encoding="utf-8"))
        if verify_plan(payload):
            print(f"[avaliar-resiliencia] Plano íntegro: {payload['plan_sha256']}")
            return 0
        print("[avaliar-resiliencia] ERRO: hash interno do plano não confere.")
        return 2
    if args.command == "prepare-execution":
        output = prepare_execution(
            baseline_dir=args.baseline_dir,
            structured_dir=args.structured_dir,
            fixture=args.fixture,
            frozen_plan=args.plan,
            output_dir=args.output_dir,
            allowlist=args.allowlist,
            semantic_review=args.semantic_review,
            track_id=args.track_id,
            model_id=args.model_id,
        )
        print(f"[avaliar-resiliencia] Execução preparada: {output}")
        return 0
    if not args.execute_live_site:
        print("[avaliar-resiliencia] Nenhuma requisição executada. Confirme com --execute-live-site.")
        return 2
    if args.command == "eligibility":
        output = execute_eligibility(
            execution_manifest_path=args.execution_manifest,
            playwright_config=args.playwright_config,
            node_project_dir=args.node_project_dir,
            output_dir=args.output_dir,
            repetitions=args.repetitions,
        )
        print(f"[avaliar-resiliencia] Elegibilidade: {output}")
        return 0
    json_output, markdown_output = execute_experiment(
        execution_manifest_path=args.execution_manifest,
        eligibility_results_path=args.eligibility_results,
        playwright_config=args.playwright_config,
        node_project_dir=args.node_project_dir,
        control_test=args.control_test,
        output_dir=args.output_dir,
        repetitions=args.repetitions,
        mutation_ids=tuple(args.mutation),
        mutations_per_scenario=args.mutations_per_scenario,
        scenario_ids=tuple(args.scenario),
    )
    print(f"[avaliar-resiliencia] JSON: {json_output}")
    print(f"[avaliar-resiliencia] Markdown: {markdown_output}")
    return 0
