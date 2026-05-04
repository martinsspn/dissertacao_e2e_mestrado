# Semantic E2E Generator

Este diretório concentra o gerador de testes E2E em um unico modulo Python.

## Estrutura

```text
python_app/
├── semantic_e2e/
│   ├── domain/            # entidades e objetos de dados puros
│   ├── application/       # caso de uso e portas
│   ├── infrastructure/    # adapters de Neo4j, LLM e filesystem
│   ├── presentation/      # CLI
│   ├── config.py          # configuracao por ambiente/argumentos
│   └── __main__.py        # entrada para python3 -m semantic_e2e
├── specs/                 # entrada: um .txt por especificacao
├── generated_tests/       # saida: um .spec.ts por especificacao
└── README.md
```

## Arquitetura

O pacote segue uma separacao inspirada em Clean Architecture:

- `domain/`: nao depende de frameworks, banco, HTTP ou filesystem.
- `application/`: contem o caso de uso `GenerateTestsUseCase` e depende apenas das portas em `ports.py`.
- `infrastructure/`: implementa as portas com Neo4j, API OpenAI-compatible e arquivos locais.
- `presentation/`: monta as dependencias concretas e expoe a CLI.

## Uso

```bash
cd python_app
export OPENAI_API_KEY=...
python3 -m semantic_e2e \
  --specs-dir ./specs \
  --output-dir ./generated_tests \
  --base-url https://demowebshop.tricentis.com/ \
  --llm-model gpt-4.1-mini
```

## Variaveis de ambiente

- `NEO4J_URI` (padrao: `bolt://neo4j:7687`)
- `NEO4J_USER` (padrao: `neo4j`)
- `NEO4J_PASSWORD` (padrao: `neo4j_password`)
- `SEMANTIC_E2E_BASE_URL` (padrao: `https://demowebshop.tricentis.com/`)
- `OPENAI_API_KEY` (obrigatoria)
- `OPENAI_BASE_URL` (padrao: `https://api.openai.com/v1`)
- `LLM_MODEL` (padrao: `gpt-4.1-mini`)
- `SEMANTIC_E2E_GRAPH_MAX_EDGES` (padrao: `500`)
