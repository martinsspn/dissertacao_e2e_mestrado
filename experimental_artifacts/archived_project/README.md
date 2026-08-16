# Gerador De Prompts E2E Com Contexto Estruturado

Este repositorio contem um pipeline para gerar prompts estruturados que auxiliam LLMs na criacao de testes E2E Playwright.

O foco do projeto e usar contexto extraido da aplicacao real para reduzir alucinacoes de rotas, seletores e fluxos em testes gerados por IA.

## Visao Geral

1. O Crawljax explora links navegacionais de uma aplicacao web via Selenium usando uma politica fixa.
2. O componente de extracao inventaria todos os controles dos DOMs visitados, inclusive botoes e campos que o crawler nao executa.
3. O grafo navegacional e o inventario estruturado da interface sao persistidos no Neo4j.
4. O gerador Python le uma especificacao em linguagem natural.
5. A especificacao e segmentada em etapas textuais sem uso de LLM; titulos isolados ou inline antes da primeira acao sao descartados.
6. O gerador associa a cada etapa as interacoes da interface, evidencias de pagina e resultados observados aplicaveis e produz apenas o prompt estruturado.

## Estrutura

```text
crawljax_explorer/                     # Crawler Java + componente de extracao
python_app/teste_prompt_e2e_semantico/ # Gerador de prompts
python_app/avaliacao_prompts/           # Ferramenta auxiliar nao oficial
web_app/                               # Interface auxiliar nao oficial
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

Os limites de profundidade, quantidade de estados, tempo de execucao e esperas do Crawljax sao definidos por uma politica padrao no codigo. A ordem aleatoria fica desativada e a prioridade e `SHALLOW_FIRST`. Somente links (`a`) sao executados durante a exploracao; botoes, inputs, selects e formularios continuam no inventario extraido do HTML, mas nao alteram o estado da aplicacao durante o mapeamento. Os parametros de cada execucao sao gravados em `output_crawljax/crawl_run_manifest.json`.

Na pagina inicial do Demo Web Shop, o Nivo Slider e excluido dos eventos e da
comparacao entre estados. O carrossel troca automaticamente seu DOM; considera-lo
como comportamento navegacional impede o Crawljax de reconhecer a pagina inicial
depois de um reset. A exclusao e estrutural (`slider-wrapper`) e nao depende das
especificacoes avaliadas. O bloco `block-recently-viewed-products` tambem e
ignorado na comparacao entre estados, pois seu conteudo muda como efeito colateral
da visita a produtos e invalidaria caminhos de backtracking.

Campos `input[type=password]` permanecem no inventario para fornecer rotulo,
identificador e seletor ao gerador. O atributo `value` desses campos e sempre
persistido como string vazia.

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

### Selecao De Contexto Orientada A Interface

O gerador trata a interface ativa como ponto de partida de cada etapa. Primeiro
procura campos, botoes, links e outros controles na pagina corrente; uma rota e
apenas uma evidencia auxiliar de navegacao, e nao o criterio principal de
selecao. Uma etapa pode receber ate quatro interacoes distintas quando elas sao
explicitamente mencionadas ou estruturalmente relacionadas, como o campo e o
botao de envio do mesmo formulario.

Acoes locais, como preencher, marcar ou clicar em um botao sem navegacao
observada, mantem a pagina ativa. O cursor de pagina so avanca por um `href`, por
uma transicao efetivamente observada ou por uma pagina identificada de forma
literal e univoca pelo seu `h1` ou `title`. O atributo `form_action` descreve a
estrutura do formulario, mas nao comprova que houve redirecionamento.

No prompt, interacoes da mesma interface compartilham um unico `pagina=`;
`pagina_evidencia=` identifica separadamente a pagina cujo `h1` ou `title` foi
usado como evidencia. Referencias genericas a um grupo `radio` permanecem sem
opcao associada ate que a etapa mencione um rotulo ou valor concreto.

O contexto e auxiliar e deliberadamente incompleto. O prompt instrui a LLM a
combina-lo com a especificacao e com seu conhecimento de navegacao web para
acessar paginas, localizar elementos visiveis e completar todas as acoes. Uma
etapa sem contexto nao deve ser omitida, e rotas ou seletores nao observados nao
devem ser apresentados como fatos extraidos.

As regras sao deterministicas e nao usam scores, pesos ou uma metrica de
cobertura da especificacao. O exportador atual consolida em um mesmo `PageState`
os DOMs observados com a mesma URL. Assim, controles encontrados em estados
AJAX distintos podem ser unidos e sua ordem temporal nao fica disponivel ao
gerador; essa e uma limitacao registrada do contexto extraido.

## Ferramentas Auxiliares Nao Oficiais

A interface em `web_app/` e o avaliador em `python_app/avaliacao_prompts/` existem apenas para auxiliar a execucao local e a analise dos resultados. Eles nao integram o artefato principal proposto para a dissertacao.

A interface web orquestra o pipeline em telas:

- crawler e infraestrutura;
- visualizacao do grafo;
- especificacoes em linguagem natural;
- prompts gerados;
- testes `.spec.ts` colados a partir da LLM;
- avaliacao auxiliar com relatorio Markdown legivel.

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

- `crawljax_explorer/src/main/java/br/ufrn/mestrado/plugin/SemanticExportPlugin.java`: extrai dados estruturados da interface e persiste o grafo no Neo4j.
- `python_app/teste_prompt_e2e_semantico/teste_prompt_e2e_semantico/application/`: segmentacao, selecao de contexto, seletores e montagem dos prompts.
- `python_app/teste_prompt_e2e_semantico/teste_prompt_e2e_semantico/infrastructure/`: adaptadores de Neo4j e filesystem.
- `docs/proposta_gerador_prompt_e2e_semantico.md`: recorte da pesquisa, perguntas, avaliacao e relevancia.
- `docs/projeto_contexto_estruturado_por_etapa.md`: desenho implementado para extrair controles HTML e associar contexto diretamente a cada etapa.
- `docs/resultado_experimento_contexto_estruturado_2026-07-14.md`: registro historico da comparacao entre os prompts anteriores e os artefatos gerados com o crawler estabilizado antes da selecao orientada a interface.
- `docs/resultado_seletor_orientado_a_interface.md`: comparacao do seletor anterior com a versao orientada a controles e evidencias da interface, usando o mesmo grafo.
- `python_app/avaliacao_prompts/`: ferramenta auxiliar nao oficial para organizar evidencias em relatorios Markdown.
- `docs/projeto_modulo_web.md`: desenho da interface web auxiliar local.
- `web_app/`: interface auxiliar nao oficial para operar o pipeline durante o experimento.

## Escopo

Este projeto nao gera testes automaticamente nem chama uma LLM diretamente. Ele gera apenas o prompt com contexto estruturado. Na condicao baseline, a especificacao original e enviada diretamente a LLM, sem passar pelo gerador.

A geracao totalmente autonoma de testes fica como trabalho futuro.
