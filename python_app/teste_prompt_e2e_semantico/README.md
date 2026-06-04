# Gerador De Prompts E2E Semanticos

Modulo Python responsavel por gerar prompts estruturados para LLMs criarem testes E2E Playwright.

Entrada:

- especificacoes em linguagem natural (`specs/*.txt`);
- grafo navegacional `PageState` / `NAVIGATES_TO` persistido no Neo4j.

Saida:

- arquivos `.prompt.md` em `generated_prompts/`;
- resumo de execucao em `generated_prompts/prompt_generation_summary.json`.

## Arquitetura

O modulo segue uma separacao simples inspirada em Clean Architecture:

```text
teste_prompt_e2e_semantico/
  domain/          # modelos puros do dominio
  application/     # casos de uso, ranking, seletores e montagem do prompt
  infrastructure/  # Neo4j e filesystem
  presentation/    # CLI
  config.py        # configuracao por ambiente
```

## Fluxo

1. Le especificacoes `.txt`.
2. Carrega paginas e transicoes do Neo4j.
3. Normaliza os termos da especificacao.
4. Ranqueia paginas, transicoes e caminhos candidatos.
5. Classifica seletores por robustez.
6. Monta um prompt Markdown com dados estruturados em JSON.

## Execucao Local

```bash
python3 -m teste_prompt_e2e_semantico --specs-dir ./specs --output-dir ./generated_prompts
```

## Execucao Via Docker Compose

Na raiz do repositorio:

```bash
docker compose run --rm prompt_e2e
```

## Avaliacao Automatica De Testes Gerados

Para gerar um relatorio automatico de avaliacao sobre arquivos `.spec.ts`:

```bash
python3 -m teste_prompt_e2e_semantico.evaluation \
  --tests-dir ./generated_tests/semantic_prompt \
  --approach semantic_prompt \
  --base-url https://demowebshop.tricentis.com/ \
  --skip-graph \
  --output ./evaluation_reports/semantic_prompt.json
```

Remova `--skip-graph` para comparar URLs e textos do teste com o grafo armazenado no Neo4j.

## Configuracao

No uso via Docker Compose, o modulo ja recebe as configuracoes necessarias. Para trocar a aplicacao alvo em todo o pipeline, ajuste `TARGET_URL`; o Compose repassa esse valor como `PROMPT_E2E_BASE_URL`.

Variaveis opcionais para execucao local ou experimentos:

- `PROMPT_E2E_BASE_URL` (padrao: `https://demowebshop.tricentis.com/`)
- `PROMPT_E2E_SPECS_DIR` (padrao: `specs`)
- `PROMPT_E2E_OUTPUT_DIR` (padrao: `generated_prompts`)
- `PROMPT_E2E_GRAPH_MAX_EDGES` (padrao: `500`)
- `PROMPT_E2E_RELEVANT_PAGES_LIMIT` (padrao: `12`)
- `PROMPT_E2E_RELEVANT_TRANSITIONS_LIMIT` (padrao: `20`)
- `PROMPT_E2E_CANDIDATE_PATHS_LIMIT` (padrao: `5`)
- `PROMPT_E2E_MAX_PATH_DEPTH` (padrao: `6`)
- `NEO4J_URI`, `NEO4J_USER`, `NEO4J_PASSWORD`
