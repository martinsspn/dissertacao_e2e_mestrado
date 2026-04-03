import argparse
import base64
import json
import os
import time
from pathlib import Path
from typing import Any, Dict, List

import requests


SYSTEM_PROMPT = (
    "Você é um analista de testes E2E. "
    "Receberá contexto multimodal de uma transição entre estados. "
    "Retorne JSON puro (sem markdown) no formato: "
    "{\"intent\":string,\"confidence\":number,\"reason\":string,"
    "\"entities\":[string],\"alternatives\":[{\"intent\":string,\"confidence\":number}]}"
)


def infer_mock_semantics(package: Dict[str, Any]) -> Dict[str, Any]:
    edge = package.get("edge", {})
    action = (edge.get("acao", "") or "").lower()
    trigger_text = (edge.get("trigger_text", "") or "").lower()
    destination = package.get("destination_node", {})
    destination_errors = (destination.get("mensagens_erro_visiveis", "") or "").strip()
    destination_title = destination.get("titulo", "") or ""

    if action == "click" and "register" in trigger_text:
        return {
            "intent": "INTENT_NAVIGATE_TO_REGISTER",
            "confidence": 0.8,
            "reason": "Clique em elemento com texto de cadastro",
            "entities": ["navigation", "register"],
            "alternatives": [{"intent": "INTENT_OPEN_AUTH_ENTRY", "confidence": 0.35}],
            "comment_ptbr": f"A ação parece navegar para cadastro. Página destino: {destination_title}."
        }

    if action == "click" and (edge.get("input_type", "") or "").lower() == "submit":
        intent = "INTENT_SUBMIT_FORM"
        reason = "Clique em input do tipo submit"
        entities = ["form", "submit"]
        if destination_errors:
            intent = "INTENT_SUBMIT_WITH_VALIDATION_ERROR"
            reason = "Submissão seguida de mensagens de erro no destino"
            entities.append("validation_error")
        return {
            "intent": intent,
            "confidence": 0.82,
            "reason": reason,
            "entities": entities,
            "alternatives": [{"intent": "INTENT_TRIGGER_FORM_VALIDATION", "confidence": 0.42}],
            "comment_ptbr": "A interação corresponde ao envio de formulário, com indícios de validação no fluxo."
        }

    if action == "reload":
        return {
            "intent": "INTENT_RELOAD_OR_REDIRECT",
            "confidence": 0.65,
            "reason": "Aresta técnica do tipo reload",
            "entities": ["navigation", "reload"],
            "alternatives": [{"intent": "INTENT_AUTO_REFRESH", "confidence": 0.4}],
            "comment_ptbr": "A transição aparenta ser recarga/redirecionamento automático da página."
        }

    return {
        "intent": "INTENT_UNKNOWN",
        "confidence": 0.3,
        "reason": "Sinais insuficientes para classificação segura no modo mock",
        "entities": ["unknown"],
        "alternatives": [],
        "comment_ptbr": "Não há evidências suficientes para classificar a intenção com segurança."
    }


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=False, indent=2)


def encode_image_to_data_url(path: str) -> str:
    file_path = Path(path)
    if not file_path.exists():
        return ""
    payload = base64.b64encode(file_path.read_bytes()).decode("utf-8")
    return f"data:image/png;base64,{payload}"


def call_llm(package: Dict[str, Any], api_key: str, model: str, base_url: str) -> Dict[str, Any]:
    origin_img = encode_image_to_data_url(package.get("origin_screenshot", ""))
    dest_img = encode_image_to_data_url(package.get("destination_screenshot", ""))

    user_payload = {
        "edge": package.get("edge", {}),
        "origin_node": package.get("origin_node", {}),
        "destination_node": package.get("destination_node", {}),
        "origin_context": package.get("origin_context", {}),
        "destination_context": package.get("destination_context", {}),
        "element_metadata": package.get("element_metadata", {}),
        "collector_status": package.get("collector_status", ""),
        "collector_errors": package.get("collector_errors", []),
    }

    content: List[Dict[str, Any]] = [
        {
            "type": "text",
            "text": "Analise a transição e classifique a intenção principal com confiança.\\n"
            + json.dumps(user_payload, ensure_ascii=False)
        }
    ]
    if origin_img:
        content.append({"type": "image_url", "image_url": {"url": origin_img}})
    if dest_img:
        content.append({"type": "image_url", "image_url": {"url": dest_img}})

    payload = {
        "model": model,
        "temperature": 0.1,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": content},
        ],
        "response_format": {"type": "json_object"},
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    max_attempts = 6
    for attempt in range(1, max_attempts + 1):
        response = requests.post(
            f"{base_url.rstrip('/')}/chat/completions",
            headers=headers,
            json=payload,
            timeout=120,
        )

        if response.status_code < 400:
            text = response.json()["choices"][0]["message"]["content"]
            return json.loads(text)

        retryable = response.status_code == 429 or 500 <= response.status_code < 600
        if not retryable or attempt == max_attempts:
            response.raise_for_status()

        retry_after_header = response.headers.get("Retry-After", "")
        retry_after_seconds = 0.0
        try:
            retry_after_seconds = float(retry_after_header)
        except ValueError:
            retry_after_seconds = 0.0

        backoff_seconds = max(retry_after_seconds, 2 ** attempt)
        time.sleep(min(backoff_seconds, 60.0))

    raise RuntimeError("Falha inesperada ao chamar LLM")


def load_existing_edges(output_path: Path) -> Dict[str, Dict[str, Any]]:
    if not output_path.exists():
        return {}
    try:
        payload = load_json(output_path)
    except Exception:
        return {}

    existing_edges = payload.get("enriched_edges", []) if isinstance(payload, dict) else []
    by_edge_id: Dict[str, Dict[str, Any]] = {}
    for item in existing_edges:
        edge_id = item.get("edge_id", "") if isinstance(item, dict) else ""
        if edge_id:
            by_edge_id[edge_id] = item
    return by_edge_id


def save_checkpoint(
    output_path: Path,
    packages: List[Dict[str, Any]],
    enriched_by_id: Dict[str, Dict[str, Any]],
    model: str,
    mode: str,
) -> None:
    ordered_enriched = []
    for package in packages:
        edge_id = package.get("edge_id", "")
        if edge_id and edge_id in enriched_by_id:
            ordered_enriched.append(enriched_by_id[edge_id])

    result = {
        "model": model,
        "mode": mode,
        "total_edges": len(packages),
        "processed_edges": len(ordered_enriched),
        "completed": len(ordered_enriched) == len(packages),
        "enriched_edges": ordered_enriched,
    }
    save_json(output_path, result)


def main() -> None:
    parser = argparse.ArgumentParser(description="Enriquecedor semântico multimodal via LLM")
    parser.add_argument("--input", default="/app/data_input/multimodal_dataset/multimodal_packages.json")
    parser.add_argument("--output", default="/app/data_input/grafo_semantico_enriquecido_llm.json")
    parser.add_argument("--model", default=os.getenv("LLM_MODEL", "gpt-4.1-mini"))
    parser.add_argument("--base-url", default=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"))
    parser.add_argument("--mock", action="store_true", help="Executa enriquecimento sem chamada externa de LLM")
    parser.add_argument("--batch-size", type=int, default=int(os.getenv("LLM_BATCH_SIZE", "1")))
    parser.add_argument("--batch-sleep", type=float, default=float(os.getenv("LLM_BATCH_SLEEP_SECONDS", "5")))
    parser.add_argument("--resume", action="store_true", help="Retoma de uma saída parcial já existente")
    args = parser.parse_args()

    api_key = os.getenv("OPENAI_API_KEY", "")
    use_mock = args.mock or os.getenv("LLM_MOCK_MODE", "false").lower() in {"1", "true", "yes"}
    if not use_mock and not api_key:
        raise EnvironmentError("OPENAI_API_KEY não definido (ou use --mock)")

    packages = load_json(Path(args.input))
    output_path = Path(args.output)
    mode = "mock" if use_mock else "llm_api"
    model_name = "mock-multimodal" if use_mock else args.model

    enriched_by_id = load_existing_edges(output_path) if args.resume else {}
    start_processed = len(enriched_by_id)
    api_calls_since_pause = 0

    for index, package in enumerate(packages, start=1):
        edge_id = package.get("edge_id", "")
        if edge_id and edge_id in enriched_by_id:
            continue

        try:
            llm_result = infer_mock_semantics(package) if use_mock else call_llm(
                package,
                api_key=api_key,
                model=args.model,
                base_url=args.base_url,
            )
        except Exception:
            save_checkpoint(output_path, packages, enriched_by_id, model_name, mode)
            raise

        enriched_item = {
            "edge_id": edge_id,
            "edge": package.get("edge", {}),
            "llm_semantics": llm_result,
            "collector_status": package.get("collector_status", ""),
        }
        if edge_id:
            enriched_by_id[edge_id] = enriched_item

        save_checkpoint(output_path, packages, enriched_by_id, model_name, mode)
        print(f"Progresso LLM: {len(enriched_by_id)}/{len(packages)} arestas processadas (índice {index}).")

        if not use_mock:
            api_calls_since_pause += 1
            if args.batch_size > 0 and api_calls_since_pause >= args.batch_size and len(enriched_by_id) < len(packages):
                api_calls_since_pause = 0
                if args.batch_sleep > 0:
                    print(f"Pausa de {args.batch_sleep:.1f}s para reduzir risco de rate limit.")
                    time.sleep(args.batch_sleep)

    if args.resume and start_processed > 0:
        print(f"Retomada ativa: {start_processed} arestas já estavam processadas.")

    save_checkpoint(output_path, packages, enriched_by_id, model_name, mode)
    print(f"Enriquecimento LLM concluído: {args.output}")


if __name__ == "__main__":
    main()