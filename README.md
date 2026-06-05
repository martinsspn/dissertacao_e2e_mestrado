cd /home/martinsspn/dissertacao_e2e_semantico
docker compose up --build -d web_app# Gerador De Prompts E2E Semanticos

Este repositorio contem um pipeline para gerar prompts estruturados que auxiliam LLMs na criacao de testes E2E Playwright.

O foco do projeto e usar contexto extraido da aplicacao real para reduzir alucinacoes de rotas, seletores e fluxos em testes gerados por IA.

## Visao Geral

1. O Crawljax explora uma aplicacao web via Selenium usando uma politica padrao de exploracao.
2. O plugin semantico coleta paginas, transicoes, textos, atributos de elementos e seletores.
3. O grafo navegacional e persistido no Neo4j.
4. O gerador Python le uma especificacao em linguagem natural.
5. O gerador seleciona paginas, transicoes e caminhos relevantes no grafo.
6. O resultado e um arquivo `.prompt.md` para ser usado em uma LLM.

## Estrutura

```text
crawljax_explorer/                     # Crawler Java + plugin semantico
python_app/teste_prompt_e2e_semantico/ # Gerador de prompts
docs/                                  # Proposta e material da dissertacao
docker-compose.yml                     # Neo4j, Selenium, Crawljax e gerador
```

## Executar O Crawler

```bash
docker compose up -d neo4j selenium_chrome
docker compose run --rm crawljax_java
```

Por padrao, o alvo e `https://demowebshop.tricentis.com/`. A unica entrada necessaria para trocar a aplicacao explorada e `TARGET_URL`:

```bash
TARGET_URL=https://exemplo.com docker compose run --rm crawljax_java
```

Os limites de profundidade, quantidade de estados, tempo de execucao e esperas do Crawljax sao definidos por uma politica padrao no codigo. Eles existem apenas para manter o grafo finito e reprodutivel.

Quando o gerador de prompts roda via Docker Compose, esse mesmo `TARGET_URL` tambem e usado como `base_url` do prompt.

## Gerar Prompts

As especificacoes devem ficar em:

```text
python_app/teste_prompt_e2e_semantico/specs/
```

Execute via Docker:

```bash
docker compose run --rm prompt_e2e
```

Ou localmente:

```bash
cd python_app/teste_prompt_e2e_semantico
python3 -m teste_prompt_e2e_semantico --specs-dir ./specs --output-dir ./generated_prompts
```

Os prompts gerados ficam em:

```text
python_app/teste_prompt_e2e_semantico/generated_prompts/
```

## Interface Web Local

A interface web fica em `web_app/` e orquestra o pipeline completo em telas:

- crawler e infraestrutura;
- visualizacao do grafo;
- especificacoes em linguagem natural;
- prompts gerados;
- testes `.spec.ts` colados a partir da LLM;
- avaliacao automatica.

Instale as dependencias e execute:

```bash
cd web_app
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/uvicorn web_app.main:app --host 127.0.0.1 --port 8000
```

Depois acesse:

```text
http://127.0.0.1:8000
```

A interface salva logs de execucao em `web_app_data/jobs/`.

### Interface Web via Docker

Execute o container do app web:

```bash
docker compose up --build web_app
```

Depois acesse:

```text
http://127.0.0.1:8000
```

Para usar outra aplicacao alvo:

```bash
TARGET_URL=https://exemplo.com docker compose up --build web_app
```

O container monta o socket do Docker para disparar os jobs do pipeline a partir da interface.

## Componentes Principais

- `crawljax_explorer/src/main/java/br/ufrn/mestrado/plugin/SemanticExportPlugin.java`: extrai metadados semanticos e persiste o grafo no Neo4j.
- `python_app/teste_prompt_e2e_semantico/teste_prompt_e2e_semantico/application/`: regras de ranking, seletores e montagem do prompt.
- `python_app/teste_prompt_e2e_semantico/teste_prompt_e2e_semantico/infrastructure/`: adaptadores de Neo4j e filesystem.
- `docs/proposta_gerador_prompt_e2e_semantico.md`: recorte da pesquisa, perguntas, avaliacao e relevancia.
- `docs/projeto_modulo_web.md`: desenho de uma interface web local para operar o pipeline.
- `web_app/`: interface web local para executar crawler, gerar prompts, registrar testes e avaliar resultados.

## Escopo

Este projeto nao gera testes automaticamente nem chama uma LLM diretamente. Ele gera um prompt estruturado, auditavel e fundamentado no grafo da aplicacao.

A geracao totalmente autonoma de testes fica como trabalho futuro.
