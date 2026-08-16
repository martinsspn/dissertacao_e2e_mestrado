#!/usr/bin/env python3
"""Generate isolated baseline and structured-context Playwright tests with Ollama."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SYSTEM_PROMPT = (
    "Você é especialista em testes E2E com Playwright Test. Crie um único arquivo "
    "TypeScript .spec.ts completo e executável a partir do conteúdo fornecido. "
    "Importe test e expect de @playwright/test e registre testes exclusivamente com "
    "test(), test.describe() e seus fixtures. Não use Jest, Mocha, React, JSX, "
    "playwright.chromium, comandos Bash, instruções de instalação ou pseudocódigo. "
    "Responda somente com um bloco de código typescript, sem explicações fora dele."
)
CODE_BLOCK = re.compile(r"```(?:typescript|ts)?\s*(.*?)```", re.DOTALL | re.IGNORECASE)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Executa condições baseline e structured_context sem histórico compartilhado."
    )
    parser.add_argument("--specs-dir", type=Path, required=True)
    parser.add_argument("--prompts-dir", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--model", default="granite3.2-vision:latest")
    parser.add_argument("--ollama-url", default="http://127.0.0.1:11434")
    parser.add_argument(
        "--transport",
        choices=["http", "windows-powershell"],
        default="http",
        help="Use windows-powershell para acessar com segurança o localhost do Windows.",
    )
    parser.add_argument("--seed", type=int, default=20260724)
    parser.add_argument("--num-ctx", type=int, default=16384)
    parser.add_argument("--num-predict", type=int, default=4096)
    parser.add_argument("--timeout", type=int, default=1800)
    return parser.parse_args()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def post_json_http(url: str, payload: dict[str, Any], timeout: int) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Ollama retornou HTTP {error.code}: {detail}") from error


def post_json_windows(payload: dict[str, Any], timeout: int) -> dict[str, Any]:
    script = (
        "[Console]::InputEncoding = [System.Text.UTF8Encoding]::new($false); "
        "[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false); "
        "$body = [Console]::In.ReadToEnd(); "
        "$result = Invoke-RestMethod "
        "-Uri 'http://127.0.0.1:11434/api/generate' "
        "-Method Post -ContentType 'application/json; charset=utf-8' -Body $body; "
        "$result.PSObject.Properties.Remove('context'); "
        "$result | ConvertTo-Json -Depth 20 -Compress"
    )
    completed = subprocess.run(
        ["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", script],
        input=json.dumps(payload, ensure_ascii=False),
        text=True,
        encoding="utf-8",
        capture_output=True,
        timeout=timeout,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            "Falha na ponte PowerShell para o Ollama: "
            + completed.stderr.strip()
        )
    return json.loads(completed.stdout)


def extract_typescript(response: str) -> str:
    match = CODE_BLOCK.search(response)
    source = match.group(1) if match else response
    return source.strip() + "\n"


def discover_cases(specs_dir: Path, prompts_dir: Path) -> list[tuple[str, Path, Path]]:
    cases: list[tuple[str, Path, Path]] = []
    for spec_path in sorted(specs_dir.glob("*.txt")):
        scenario = spec_path.stem
        prompt_path = prompts_dir / f"{scenario}.structured_context.prompt.md"
        if not prompt_path.is_file():
            raise FileNotFoundError(
                f"Prompt estruturado ausente para {scenario}: {prompt_path}"
            )
        cases.append((scenario, spec_path, prompt_path))
    if not cases:
        raise ValueError(f"Nenhuma especificação .txt encontrada em {specs_dir}")
    return cases


def generate_one(
    *,
    api_url: str,
    model: str,
    prompt: str,
    seed: int,
    num_ctx: int,
    num_predict: int,
    timeout: int,
    transport: str,
) -> dict[str, Any]:
    # /api/generate is stateless unless a context returned by a prior call is sent
    # back. This runner deliberately never sends that field.
    payload = {
        "model": model,
        "system": SYSTEM_PROMPT,
        "prompt": prompt,
        "stream": False,
        "keep_alive": "10m",
        "options": {
            "temperature": 0,
            "seed": seed,
            "num_ctx": num_ctx,
            "num_predict": num_predict,
        },
    }
    if transport == "windows-powershell":
        return post_json_windows(payload, timeout)
    return post_json_http(api_url, payload, timeout)


def main() -> int:
    args = parse_args()
    output_root = args.output_root.resolve()
    if output_root.exists():
        print(
            f"[ollama-experiment] Recusando reutilizar saída existente: {output_root}",
            file=sys.stderr,
        )
        return 2

    cases = discover_cases(args.specs_dir.resolve(), args.prompts_dir.resolve())
    output_root.mkdir(parents=True)
    started_at = datetime.now(timezone.utc)
    records: list[dict[str, Any]] = []

    # Conditions are materialized independently before inference. No output from
    # either condition is ever read to construct an input for the other.
    conditions = {
        "baseline": [(name, spec.read_text(encoding="utf-8")) for name, spec, _ in cases],
        "structured_context": [
            (name, prompt.read_text(encoding="utf-8")) for name, _, prompt in cases
        ],
    }

    for condition, inputs in conditions.items():
        for index, (scenario, prompt) in enumerate(inputs, start=1):
            case_dir = output_root / condition / scenario
            write_text(case_dir / "input.prompt.txt", prompt)
            print(
                f"[ollama-experiment] {condition} {index}/{len(inputs)}: {scenario}",
                flush=True,
            )
            started = time.monotonic()
            response = generate_one(
                api_url=f"{args.ollama_url.rstrip('/')}/api/generate",
                model=args.model,
                prompt=prompt,
                seed=args.seed,
                num_ctx=args.num_ctx,
                num_predict=args.num_predict,
                timeout=args.timeout,
                transport=args.transport,
            )
            elapsed = time.monotonic() - started
            raw_response = str(response.get("response", ""))
            write_text(case_dir / "response.raw.md", raw_response)
            write_text(case_dir / f"{scenario}.spec.ts", extract_typescript(raw_response))

            metadata = {
                key: value
                for key, value in response.items()
                if key not in {"response", "context"}
            }
            metadata.update(
                {
                    "condition": condition,
                    "scenario": scenario,
                    "model_requested": args.model,
                    "seed": args.seed,
                    "temperature": 0,
                    "num_ctx": args.num_ctx,
                    "num_predict": args.num_predict,
                    "elapsed_seconds_client": round(elapsed, 3),
                    "input_sha256": sha256_text(prompt),
                    "response_sha256": sha256_text(raw_response),
                    "stateless": True,
                }
            )
            write_text(
                case_dir / "metadata.json",
                json.dumps(metadata, ensure_ascii=False, indent=2) + "\n",
            )
            records.append(metadata)

    manifest = {
        "run_id": output_root.name,
        "started_at_utc": started_at.isoformat(),
        "finished_at_utc": datetime.now(timezone.utc).isoformat(),
        "ollama_url": args.ollama_url,
        "transport": args.transport,
        "model": args.model,
        "system_prompt": SYSTEM_PROMPT,
        "settings": {
            "temperature": 0,
            "seed": args.seed,
            "num_ctx": args.num_ctx,
            "num_predict": args.num_predict,
        },
        "isolation": {
            "api": "/api/generate",
            "context_reused": False,
            "independent_condition_directories": True,
            "existing_output_reuse_allowed": False,
        },
        "case_count_per_condition": len(cases),
        "records": records,
    }
    write_text(
        output_root / "manifest.json",
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    )
    print(f"[ollama-experiment] Concluído: {output_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
