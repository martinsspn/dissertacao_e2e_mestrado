import argparse
import subprocess
import sys
from pathlib import Path


def run_step(command, cwd: Path):
    print(f"\n>>> Executando: {' '.join(command)}")
    process = subprocess.run(command, cwd=str(cwd), check=False)
    if process.returncode != 0:
        raise RuntimeError(f"Falha no comando: {' '.join(command)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Pipeline: Crawljax outputs -> coleta multimodal -> enriquecimento LLM")
    parser.add_argument("--input-dir", default="output_crawljax")
    parser.add_argument("--dataset-dir", default="output_crawljax/multimodal_dataset")
    parser.add_argument("--output-file", default="output_crawljax/grafo_semantico_enriquecido_llm.json")
    parser.add_argument("--mock", action="store_true", help="Executa o estágio LLM em modo mock")
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    running_in_container = (script_dir / "data_input").exists()
    repo_root = script_dir if running_in_container else script_dir.parent

    if args.input_dir == "output_crawljax":
        args.input_dir = str(script_dir / "data_input") if running_in_container else str((repo_root / "output_crawljax").resolve())

    if args.dataset_dir == "output_crawljax/multimodal_dataset":
        args.dataset_dir = (
            str(script_dir / "data_input" / "multimodal_dataset")
            if running_in_container
            else str((repo_root / "output_crawljax" / "multimodal_dataset").resolve())
        )

    if args.output_file == "output_crawljax/grafo_semantico_enriquecido_llm.json":
        args.output_file = (
            str(script_dir / "data_input" / "grafo_semantico_enriquecido_llm.json")
            if running_in_container
            else str((repo_root / "output_crawljax" / "grafo_semantico_enriquecido_llm.json").resolve())
        )

    collector_script = script_dir / "multimodal_collector.py"
    enricher_script = script_dir / "llm_multimodal_enricher.py"

    collector_cmd = [
        sys.executable,
        str(collector_script),
        "--input-dir",
        args.input_dir,
        "--output-dir",
        args.dataset_dir,
    ]

    enricher_cmd = [
        sys.executable,
        str(enricher_script),
        "--input",
        f"{args.dataset_dir}/multimodal_packages.json",
        "--output",
        args.output_file,
    ]

    if args.mock:
        enricher_cmd.append("--mock")

    run_step(collector_cmd, repo_root)
    run_step(enricher_cmd, repo_root)

    print("\nPipeline concluído com sucesso.")
    print(f"- Dataset multimodal: {args.dataset_dir}")
    print(f"- Grafo enriquecido: {args.output_file}")


if __name__ == "__main__":
    main()
