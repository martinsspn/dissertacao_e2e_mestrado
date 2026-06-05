# Projeto Do Modulo Web

## Objetivo

Criar uma interface grafica local para orquestrar o pipeline da pesquisa:

1. configurar e executar a exploracao com Crawljax;
2. confirmar que o grafo foi persistido no Neo4j;
3. visualizar o grafo navegacional;
4. cadastrar/editar especificacoes em linguagem natural;
5. gerar prompts estruturados;
6. visualizar ou abrir a pasta dos prompts gerados;
7. registrar testes `.spec.ts` criados a partir da LLM;
8. executar a avaliacao automatica dos testes gerados;
9. consultar relatorios de avaliacao.

O modulo web deve ser uma bancada local de experimentacao, voltada ao pesquisador/desenvolvedor, nao uma aplicacao multiusuario de producao.

## Principios

- O usuario deve informar o minimo necessario.
- O fluxo principal deve seguir a ordem natural do experimento.
- Parametros avancados devem existir, mas ficar recolhidos.
- Cada etapa deve deixar claro seu status: pendente, executando, concluida, falhou.
- A interface deve expor artefatos gerados: grafo, prompts, testes e relatorios.
- A interface nao deve esconder erros: logs devem ser acessiveis.
- O modulo web deve orquestrar o pipeline existente, nao duplicar regra de negocio.

## Escopo Funcional

### 1. Dashboard Do Pipeline

Tela inicial com os blocos:

- Infraestrutura;
- Crawler;
- Grafo;
- Especificacoes;
- Prompts;
- Testes gerados;
- Avaliacao.

Cada bloco mostra:

- status atual;
- ultima execucao;
- quantidade de artefatos;
- acao principal.

Exemplo:

```text
Crawler
Status: concluido
Ultima execucao: 26 paginas, 59 transicoes
Acao: executar novamente
```

### 2. Configuracao E Execucao Do Crawler

Tela: `Crawler`

Campos principais:

- URL alvo (`TARGET_URL`);

Campos avancados, recolhidos por padrao:

- profundidade maxima;
- numero maximo de estados;
- tempo maximo de execucao;
- espera apos reload;
- espera apos evento;
- clicar uma vez;
- ordem aleatoria;
- limpar grafo antes de persistir.

Mesmo que o uso normal seja "URL + executar", esses campos permitem experimentos controlados quando necessario.

Acoes:

- iniciar Neo4j e Selenium;
- executar Crawljax;
- acompanhar logs em tempo real;
- cancelar execucao, se possivel;
- limpar artefatos locais do crawler;
- abrir Neo4j Browser.

Resultado esperado:

- mensagem de sucesso;
- contagem de paginas;
- contagem de transicoes;
- tempo total;
- link para visualizacao do grafo.

### 3. Visualizacao Do Grafo

Tela: `Grafo`

Objetivo: permitir inspecionar o que o Crawljax descobriu.

Elementos:

- resumo: paginas, transicoes, URL alvo, data da exploracao;
- grafo interativo;
- lista lateral de paginas;
- lista lateral de transicoes;
- painel de detalhes do no/aresta selecionado.

Visualizacao:

- usar Cytoscape.js no frontend;
- nos representam `PageState`;
- arestas representam `NAVIGATES_TO`;
- cor/tamanho do no pode indicar `state_count` ou `interactive_count`;
- arestas podem exibir `action` e texto do elemento;
- filtro por termo;
- filtro por tipo de acao;
- filtro por seletor forte/medio/fraco.

Detalhes de pagina:

- URL;
- titulo;
- H1;
- trecho de texto visivel;
- quantidade de elementos interativos;
- screenshot, se existir.

Detalhes de transicao:

- origem;
- destino;
- acao;
- texto do elemento;
- seletores disponiveis;
- scores de seletor.

### 4. Especificacoes Em Linguagem Natural

Tela: `Especificacoes`

Funcionalidades:

- listar arquivos `.txt`;
- criar nova especificacao;
- editar especificacao existente;
- excluir especificacao;
- duplicar especificacao;
- marcar especificacoes selecionadas para gerar prompts.

Campos:

- identificador;
- titulo;
- texto em linguagem natural;
- tags opcionais;
- observacoes.

Armazenamento:

- salvar como `.txt` em `python_app/teste_prompt_e2e_semantico/specs/`;
- opcionalmente manter metadados em JSON no futuro.

### 5. Geracao De Prompts

Tela: `Prompts`

Acoes:

- gerar prompts para todas as especificacoes;
- gerar prompt para uma especificacao selecionada;
- visualizar prompt gerado;
- copiar prompt para area de transferencia;
- abrir pasta `generated_prompts`;
- baixar prompt individual.

Parametros avancados:

- maximo de arestas lidas do grafo;
- limite de paginas relevantes;
- limite de transicoes relevantes;
- limite de caminhos candidatos;
- profundidade maxima dos caminhos.

Esses parametros devem ficar em "Configuracoes avancadas", pois o fluxo padrao deve usar os defaults do gerador.

Resultado:

- lista de prompts gerados;
- tamanho do prompt;
- quantidade de paginas/transicoes/caminhos usados;
- avisos de qualidade do contexto (`context_quality`).

### 6. Testes Gerados Pela LLM

Tela: `Testes`

Como a LLM ainda e externa ao sistema, a interface deve apoiar o processo manual:

- selecionar uma especificacao;
- abrir o prompt correspondente;
- colar o teste TypeScript gerado pela LLM;
- salvar como `.spec.ts`;
- listar testes salvos;
- editar teste salvo;
- visualizar diff simples entre versoes, se houver;
- associar teste a abordagem: `baseline` ou `semantic_prompt`.

Diretorios sugeridos:

```text
generated_tests/
  baseline/
  semantic_prompt/
```

Arquivo sugerido:

```text
generated_tests/semantic_prompt/user_registration_book_purchase.spec.ts
```

### 7. Avaliacao Automatica

Tela: `Avaliacao`

Acoes:

- escolher abordagem (`baseline` ou `semantic_prompt`);
- escolher pasta de testes;
- rodar avaliacao estatica;
- rodar avaliacao com grafo;
- futuramente, executar Playwright;
- visualizar relatorio JSON;
- exportar CSV;
- preencher rubrica humana na interface.

Metricas automaticas exibidas:

- possui import Playwright;
- possui bloco `test`;
- possui `expect`;
- quantidade de acoes;
- quantidade de locators;
- risco de seletor;
- URLs desconhecidas;
- cobertura de URLs no grafo;
- textos possivelmente inventados;
- cobertura de textos no grafo;
- status de execucao, quando existir.

Rubrica humana:

- fluxo correto;
- alvo correto;
- assercao correta;
- aderencia ao grafo;
- robustez pratica;
- utilidade geral;
- classificacao da falha;
- observacoes.

## Implementacao Inicial

A primeira versao foi implementada em `web_app/` com FastAPI, templates Jinja e CSS/JavaScript simples.

Ela ja permite:

- iniciar Neo4j e Selenium via Docker Compose;
- executar o Crawljax informando URL alvo e parametros avancados opcionais;
- consultar resumo e visualizacao simplificada do grafo;
- criar/editar especificacoes `.txt`;
- executar o gerador de prompts;
- visualizar e copiar prompts gerados;
- colar/salvar testes Playwright em `generated_tests/baseline` ou `generated_tests/semantic_prompt`;
- executar a avaliacao automatica e abrir relatorios JSON;
- acompanhar logs das execucoes em `web_app_data/jobs/`.

Pendencias planejadas:

- streaming automatico de logs;
- cancelamento de jobs;
- visualizacao de grafo com Cytoscape.js;
- rubrica humana editavel na interface;
- exportacao CSV dos relatorios.

## Arquitetura Recomendada

### Escolha Tecnica

Recomendacao: backend Python com FastAPI e frontend simples com HTML server-side + HTMX + Cytoscape.js.

Justificativa:

- evita reinstalar uma stack grande de frontend;
- combina bem com o projeto Python existente;
- e suficiente para uma ferramenta local de pesquisa;
- permite streaming de logs via Server-Sent Events;
- Cytoscape.js resolve bem a visualizacao do grafo.

Alternativa: React/Vite. Mais flexivel, mas adiciona `node_modules`, build e complexidade que o projeto acabou de remover.

### Estrutura Proposta

```text
web_app/
  pyproject.toml
  requirements.txt
  web_app/
    __init__.py
    main.py
    config.py
    domain/
      models.py
    application/
      pipeline_service.py
      job_manager.py
      graph_service.py
      specs_service.py
      prompts_service.py
      tests_service.py
      evaluation_service.py
    infrastructure/
      docker_compose_runner.py
      filesystem_repository.py
      neo4j_repository.py
      process_runner.py
    presentation/
      routes.py
      api.py
      templates/
        layout.html
        dashboard.html
        crawler.html
        graph.html
        specs.html
        prompts.html
        tests.html
        evaluation.html
      static/
        app.css
        app.js
```

### Integracao Com O Pipeline Existente

O modulo web deve chamar comandos existentes em vez de reimplementar o pipeline:

Crawler:

```bash
docker compose up -d neo4j selenium_chrome
docker compose run --rm crawljax_java
```

Gerador de prompts:

```bash
docker compose run --rm prompt_e2e
```

Avaliacao:

```bash
python3 -m teste_prompt_e2e_semantico.evaluation ...
```

Para execucao local dentro do `web_app`, o backend pode invocar esses comandos via `subprocess`, capturando logs e status.

## Modelo De Jobs

Operacoes longas devem virar jobs:

- `crawl`;
- `generate_prompts`;
- `evaluate_tests`;
- futuramente `run_playwright`.

Modelo:

```json
{
  "id": "job_20260604_001",
  "type": "crawl",
  "status": "running",
  "started_at": "2026-06-04T16:00:00",
  "finished_at": null,
  "command": "docker compose run --rm crawljax_java",
  "exit_code": null,
  "log_path": "web_app_data/jobs/job_20260604_001.log"
}
```

Status:

- `queued`;
- `running`;
- `succeeded`;
- `failed`;
- `cancelled`.

Persistencia simples:

```text
web_app_data/
  jobs/
    job_id.log
    jobs.json
  settings.json
```

## API Interna

### Pipeline

```text
GET  /api/status
POST /api/infra/start
```

### Crawler

```text
GET  /api/crawler/config
POST /api/crawler/run
GET  /api/crawler/jobs/{job_id}
GET  /api/crawler/jobs/{job_id}/logs
```

Payload de execucao:

```json
{
  "target_url": "https://demowebshop.tricentis.com/",
  "advanced": {
    "max_depth": 8,
    "max_states": 400,
    "runtime_minutes": 45
  }
}
```

### Grafo

```text
GET /api/graph/summary
GET /api/graph
GET /api/graph/pages
GET /api/graph/transitions
```

Formato para visualizacao:

```json
{
  "nodes": [
    {
      "id": "page-id",
      "label": "Books",
      "url": "https://...",
      "state_count": 3
    }
  ],
  "edges": [
    {
      "id": "edge-id",
      "source": "home",
      "target": "books",
      "label": "click Books"
    }
  ]
}
```

### Especificacoes

```text
GET    /api/specs
POST   /api/specs
GET    /api/specs/{spec_id}
PUT    /api/specs/{spec_id}
DELETE /api/specs/{spec_id}
```

### Prompts

```text
POST /api/prompts/generate
GET  /api/prompts
GET  /api/prompts/{spec_id}
POST /api/prompts/{spec_id}/copy
POST /api/prompts/open-folder
```

Observacao: abrir pasta local pode depender do sistema operacional. No Linux/WSL, talvez seja melhor exibir o caminho e oferecer download.

### Testes

```text
GET  /api/tests?approach=semantic_prompt
POST /api/tests
GET  /api/tests/{approach}/{spec_id}
PUT  /api/tests/{approach}/{spec_id}
```

Payload:

```json
{
  "spec_id": "user_registration_book_purchase",
  "approach": "semantic_prompt",
  "code": "import { test, expect } from '@playwright/test'; ..."
}
```

### Avaliacao

```text
POST /api/evaluation/run
GET  /api/evaluation/reports
GET  /api/evaluation/reports/{report_id}
PUT  /api/evaluation/reports/{report_id}/human-review
```

Payload:

```json
{
  "approach": "semantic_prompt",
  "tests_dir": "generated_tests/semantic_prompt",
  "use_graph": true
}
```

## Telas

### Dashboard

Primeira tela do sistema.

Componentes:

- status do Neo4j;
- status do Selenium;
- resumo do grafo;
- quantidade de especificacoes;
- quantidade de prompts;
- quantidade de testes;
- ultimo relatorio de avaliacao.

### Crawler

Formulario:

- URL alvo;
- botao `Executar crawler`;
- botao `Iniciar infraestrutura`;
- acordeao `Parametros avancados`;
- painel de logs;
- card de resultado.

### Grafo

Layout:

- barra superior com filtros;
- grafo central;
- painel lateral de detalhes;
- botao `Atualizar do Neo4j`.

### Especificacoes

Layout:

- lista de specs;
- editor de texto;
- salvar;
- gerar prompt para spec atual.

### Prompts

Layout:

- lista de prompts gerados;
- viewer Markdown/texto;
- copiar;
- abrir/mostrar pasta;
- metadados do prompt.

### Testes

Layout:

- seletor de abordagem;
- lista de `.spec.ts`;
- editor de codigo;
- salvar;
- marcar para avaliacao.

### Avaliacao

Layout:

- seletor de abordagem;
- botao `Rodar avaliacao`;
- tabela de resultados;
- painel de detalhes;
- formulario da rubrica humana;
- exportar JSON/CSV.

## Segurança E Limites

Como o modulo executa comandos locais (`docker compose`, scripts Python e futuramente Playwright), ele deve ser tratado como ferramenta local confiavel.

Cuidados:

- nao expor publicamente na rede;
- rodar apenas em `localhost`;
- validar caminhos para impedir escrita fora do workspace;
- nao permitir comandos arbitrarios vindos da interface;
- registrar logs de cada job;
- deixar claro quando um comando pode demorar ou modificar o grafo.

## Plano De Implementacao Incremental

### Etapa 1: Web App Minimo

- FastAPI;
- dashboard simples;
- botao para iniciar Neo4j/Selenium;
- botao para executar Crawljax;
- painel de logs;
- resumo de paginas/transicoes.

### Etapa 2: Especificacoes E Prompts

- CRUD simples de specs `.txt`;
- executar gerador de prompts;
- listar e visualizar prompts gerados.

### Etapa 3: Grafo

- endpoint JSON do grafo;
- visualizacao com Cytoscape.js;
- painel de detalhes.

### Etapa 4: Testes E Avaliacao

- salvar `.spec.ts`;
- rodar `evaluate-e2e`;
- visualizar JSON de avaliacao;
- preencher rubrica humana.

### Etapa 5: Execucao Playwright

- adicionar ambiente opcional Node/Playwright;
- executar testes;
- coletar resultado, trace e screenshots.

## Decisao Recomendada Para A Dissertacao

O modulo web deve ser apresentado como ferramenta de apoio experimental, nao como contribuicao cientifica principal.

A contribuicao principal continua sendo:

- extrair contexto semantico da aplicacao;
- gerar prompts fundamentados no grafo;
- avaliar testes gerados com protocolo hibrido.

O modulo web ajuda a demonstrar a aplicabilidade pratica e melhora a reproducibilidade dos experimentos.
