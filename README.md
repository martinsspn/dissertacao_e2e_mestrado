# Pipeline E2E Semântico (estado atual)

1. **Exploração com Crawljax (Java)**
2. **Coleta multimodal por aresta (Playwright/Python)**
3. **Enriquecimento semântico por LLM (Python)**

---

## Arquitetura atual

### Serviço `selenium_chrome`
Navegador remoto usado pelo Crawljax.

### Serviço `crawljax_java`
Executa a exploração e persiste o grafo navegacional no Neo4j:
- Nós com label `PageState`
- Relações `NAVIGATES_TO` com metadados básicos de interação (ação, seletor e tipo de gatilho)

### Serviço `neo4j`
Banco de grafo para armazenar os estados e transições de navegação.

### Serviço `python_enricher`
Container de execução para o pipeline Python:
- `python_app/multimodal_collector.py`
- `python_app/llm_multimodal_enricher.py`
- `python_app/run_multimodal_pipeline.py`

---

## Formato da saída LLM

O arquivo `output_crawljax/grafo_semantico_enriquecido_llm.json` salva progresso incremental:

- `total_edges`: total de arestas esperadas
- `processed_edges`: quantas já foram processadas
- `completed`: `true/false` indicando finalização
- `enriched_edges`: arestas enriquecidas já processadas

Isso permite retomada automática com `--resume` sem perder o que já foi processado.

---

## Comandos de execução (passo a passo)

### 0) Preparação
```bash
cp .env.example .env
# edite .env e preencha OPENAI_API_KEY

docker compose build python_enricher
docker compose up -d neo4j selenium_chrome
```

### 1) Exploração (Crawljax)
```bash
docker compose run --rm crawljax_java
```

Após executar, abra o Neo4j Browser em `http://localhost:7474` (usuário `neo4j`, senha `neo4j_password`) e rode:

```cypher
MATCH (n:PageState) RETURN n LIMIT 25;
```

```cypher
MATCH (a:PageState)-[r:NAVIGATES_TO]->(b:PageState) RETURN a, r, b LIMIT 50;
```

### 2) Coleta multimodal (somente)
```bash
docker compose run --rm -T python_enricher \
  python3 multimodal_collector.py \
  --input-dir /app/data_input \
  --output-dir /app/data_input/multimodal_dataset
```

### 3) Enriquecimento LLM (mock)
```bash
docker compose run --rm -T python_enricher \
  python3 llm_multimodal_enricher.py \
  --mock \
  --input /app/data_input/multimodal_dataset/multimodal_packages.json \
  --output /app/data_input/grafo_semantico_enriquecido_llm.json
```

### 4) Enriquecimento LLM real (com lote e pausa)
```bash
docker compose run --rm -T python_enricher \
  python3 llm_multimodal_enricher.py \
  --batch-size 1 \
  --batch-sleep 8 \
  --input /app/data_input/multimodal_dataset/multimodal_packages.json \
  --output /app/data_input/grafo_semantico_enriquecido_llm.json
```

### 5) Retomar execução após falha/429
```bash
docker compose run --rm -T python_enricher \
  python3 llm_multimodal_enricher.py \
  --resume \
  --batch-size 1 \
  --batch-sleep 8 \
  --input /app/data_input/multimodal_dataset/multimodal_packages.json \
  --output /app/data_input/grafo_semantico_enriquecido_llm.json
```

### 6) Pipeline completo em um comando

**Mock**
```bash
docker compose run --rm python_enricher \
  python3 run_multimodal_pipeline.py --mock
```

**LLM real**
```bash
docker compose run --rm python_enricher \
  python3 run_multimodal_pipeline.py
```

---

## Saídas

- Neo4j (`PageState` e `NAVIGATES_TO`): grafo navegacional persistido
- `output_crawljax/multimodal_dataset/multimodal_packages.json`: pacotes multimodais por aresta
- `output_crawljax/multimodal_dataset/multimodal_packages_summary.json`: resumo da coleta
- `output_crawljax/grafo_semantico_enriquecido_llm.json`: resultado do enriquecimento (parcial ou final)

> Observação: o pipeline Python atual ainda lê `nos.json` e `arestas.json`. Nesta mudança, o crawler passa a gravar o grafo no Neo4j. A adaptação do pipeline Python para ler direto do Neo4j pode ser feita no próximo passo.

---

## Estrutura relevante

```text
/dissertacao_e2e_semantico
├── docker-compose.yml
├── crawljax_explorer/
│   ├── Dockerfile
│   ├── pom.xml
│   └── src/main/java/br/ufrn/mestrado/MainExplorer.java
├── python_app/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── multimodal_collector.py
│   ├── llm_multimodal_enricher.py
│   └── run_multimodal_pipeline.py
└── output_crawljax/
```
