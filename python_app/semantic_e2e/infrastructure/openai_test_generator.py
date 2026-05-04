from __future__ import annotations

import json
import re

import requests

from semantic_e2e.config import GeneratorConfig
from semantic_e2e.domain.models import NavigationGraph, SpecPlan


def _strip_markdown_code_block(value: str) -> str:
    text = value.strip()
    match = re.fullmatch(r"```(?:typescript|ts|javascript|js)?\s*(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip() + "\n"
    return text + "\n"


class OpenAITestGenerator:
    def __init__(self, config: GeneratorConfig) -> None:
        self._config = config

    @property
    def model(self) -> str:
        return self._config.llm_model

    def generate(self, spec: SpecPlan, graph: NavigationGraph) -> str:
        if not self._config.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY nao definida. A geracao depende da LLM com contexto do grafo.")

        response = requests.post(
            self._chat_completions_url(),
            headers={
                "Authorization": f"Bearer {self._config.openai_api_key}",
                "Content-Type": "application/json",
            },
            json=self._build_payload(spec, graph),
            timeout=self._config.llm_timeout_seconds,
        )
        response.raise_for_status()
        data = response.json()
        content = data["choices"][0]["message"]["content"]
        return _strip_markdown_code_block(content)

    def _build_payload(self, spec: SpecPlan, graph: NavigationGraph) -> dict[str, object]:
        return {
            "model": self._config.llm_model,
            "temperature": 0.1,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "Voce gera exclusivamente codigo TypeScript de testes Playwright. "
                        "Use a especificacao do usuario e o grafo navegacional fornecido como fonte de verdade para paginas, "
                        "transicoes e seletores. Nao invente rotas ou seletores quando houver alternativa no grafo. "
                        "Retorne apenas o conteudo do arquivo .spec.ts, sem Markdown."
                    ),
                },
                {
                    "role": "user",
                    "content": json.dumps(
                        {
                            "task": "Gerar um teste E2E Playwright baseado na especificacao e no grafo navegacional.",
                            "base_url": self._config.base_url.rstrip("/"),
                            "test_title": spec.title,
                            "specification": spec.raw_text,
                            "navigation_graph": graph.to_prompt_context(),
                            "requirements": [
                                "Importar test e expect de @playwright/test.",
                                "Comecar navegando pela base_url.",
                                "Usar os seletores existentes no grafo sempre que eles forem aplicaveis.",
                                "Preferir seletores com maior selector_scores.",
                                "Adicionar assercoes observaveis do fluxo descrito.",
                                "Nao incluir explicacoes, comentarios metodologicos ou blocos Markdown.",
                            ],
                        },
                        ensure_ascii=False,
                    ),
                },
            ],
        }

    def _chat_completions_url(self) -> str:
        return self._config.openai_base_url.rstrip("/") + "/chat/completions"
