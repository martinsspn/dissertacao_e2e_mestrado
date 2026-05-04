# Pipeline E2E Semantico

Este repositorio integra o crawler (Crawljax + plugin semantico) com o gerador de testes E2E em Python.

## Como o crawler funciona

1. O Crawljax explora a aplicacao via Selenium.
2. O plugin `SemanticExportPlugin` coleta metadados de elementos (id, name, aria-label, text, href, class, role).
3. O plugin persiste no Neo4j:
	- Nos `PageState` com URL, titulo e contagem.
	- Arestas `NAVIGATES_TO` com acao, seletores e scores de robustez.

O gerador Python envia esse grafo como contexto para a LLM, que gera o teste Playwright a partir da especificacao em linguagem natural e das transicoes reais descobertas pelo crawler.

## Executar o crawler (gera o grafo)

```bash
docker compose up -d neo4j selenium_chrome
docker compose run --rm crawljax_java
```

## Executar o gerador Python

### Entrada e saida

- `python_app/specs/`: coloque aqui um ou mais arquivos `.txt` em linguagem natural.
- `python_app/generated_tests/`: aqui serao gravados os testes Playwright gerados, um `.spec.ts` por especificacao.

### Execucao

```bash
cd python_app
python3 -m semantic_e2e --specs-dir ./specs --output-dir ./generated_tests
```

Antes da execucao, defina `OPENAI_API_KEY`. Opcionalmente ajuste `OPENAI_BASE_URL`, `LLM_MODEL` e `SEMANTIC_E2E_GRAPH_MAX_EDGES`.

## O que o gerador faz

- Conecta no Neo4j e le o grafo `PageState` / `NAVIGATES_TO`.
- Le cada especificacao `.txt` sem extrair fluxo por heuristica.
- Monta um contexto JSON com paginas, transicoes, elementos, seletores e scores.
- Envia especificacao + grafo para a LLM.
- Grava o codigo Playwright retornado pela LLM.

## Componentes principais

- `crawljax_explorer/src/main/java/br/ufrn/mestrado/plugin/SemanticExportPlugin.java`: captura atributos ricos de seletores e persiste no Neo4j.
- `python_app/semantic_e2e/domain/`: entidades e objetos de dados puros.
- `python_app/semantic_e2e/application/`: caso de uso e portas.
- `python_app/semantic_e2e/infrastructure/`: adapters de Neo4j, LLM e filesystem.
- `python_app/semantic_e2e/presentation/`: CLI.
- `python_app/specs/`: entrada das especificacoes.
- `python_app/generated_tests/`: saida dos testes.

## Scripts legados

Os scripts antigos em `python_app/` continuam como compatibilidade, mas a entrada recomendada agora e a CLI do pacote `semantic_e2e`.
