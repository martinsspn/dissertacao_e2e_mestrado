# Projeto Do Modulo De Avaliacao

## Objetivo

O modulo de avaliacao mede evidencias automaticas sobre testes Playwright gerados por LLM e prepara um relatorio para a avaliacao humana.

Ele nao substitui a rubrica humana. Sua funcao e reduzir subjetividade e registrar dados reprodutiveis.

## Posicao Na Arquitetura

O modulo fica dentro do pacote do gerador de prompts:

```text
teste_prompt_e2e_semantico/
  evaluation/
    domain/
      models.py
    application/
      static_analysis.py
      graph_conformance.py
      evaluate_test.py
    infrastructure/
      filesystem_reports.py
    presentation/
      cli.py
```

Essa estrutura segue a mesma ideia de Clean Architecture do gerador:

- `domain`: modelos puros da avaliacao;
- `application`: regras de analise e caso de uso;
- `infrastructure`: escrita de relatorios e, futuramente, execucao externa do Playwright;
- `presentation`: CLI `evaluate-e2e`.

## Fluxo Projetado

1. Receber um teste gerado (`.spec.ts`), a abordagem usada (`baseline` ou `semantic_prompt`) e a especificacao associada.
2. Rodar analise estatica do arquivo.
3. Comparar URLs e textos usados no teste com o grafo navegacional.
4. Opcionalmente executar o teste com Playwright.
5. Gerar JSON com metricas automaticas.
6. Preencher posteriormente a rubrica humana e a classificacao da falha.

## Parte Ja Projetada Em Codigo

### Modelos

Arquivo:

```text
python_app/teste_prompt_e2e_semantico/teste_prompt_e2e_semantico/evaluation/domain/models.py
```

Principais modelos:

- `EvaluationCase`: identifica especificacao, abordagem, arquivo de teste e `base_url`;
- `StaticAnalysisResult`: resultado da analise estatica;
- `GraphConformanceResult`: aderencia automatica ao grafo;
- `ExecutionResult`: resultado futuro de execucao Playwright;
- `HumanReview`: campos da rubrica humana;
- `EvaluationReport`: relatorio consolidado por teste.

### Analise Estatica

Arquivo:

```text
evaluation/application/static_analysis.py
```

Coleta:

- import de `@playwright/test`;
- bloco `test(...)`;
- chamadas `expect(...)`;
- uso de `waitForTimeout`;
- URLs em `page.goto(...)`;
- quantidade de locators;
- quantidade de locators semanticos (`getByRole`, `getByText`, `getByLabel`, etc.);
- indícios de XPath;
- quantidade de acoes de usuario (`click`, `fill`, `check`, etc.);
- risco geral dos seletores (`none`, `low`, `medium`, `high`).

Essa analise usa expressoes regulares simples. Isso e suficiente para a primeira versao e explicavel metodologicamente. Se necessario, pode evoluir para parser TypeScript.

### Conformidade Com O Grafo

Arquivo:

```text
evaluation/application/graph_conformance.py
```

Compara:

- URLs usadas no teste versus URLs conhecidas no grafo;
- textos usados em locators versus textos, titulos, elementos e seletores presentes no grafo;
- cobertura de URLs conhecidas;
- cobertura de textos fundamentados no grafo;
- lista de URLs/textos possivelmente inventados.

### Caso De Uso

Arquivo:

```text
evaluation/application/evaluate_test.py
```

Funcao principal:

```python
evaluate_test_file(case, graph=None)
```

Ela le um `.spec.ts`, executa a analise estatica e, quando recebe o grafo, calcula a conformidade com ele.

### Escrita De Relatorio

Arquivo:

```text
evaluation/infrastructure/filesystem_reports.py
```

Grava uma lista de `EvaluationReport` em JSON.

### CLI

A CLI inicial foi implementada em `evaluation/presentation/cli.py`.

Uso com grafo do Neo4j:

```bash
python3 -m teste_prompt_e2e_semantico.evaluation \
  --tests-dir ./generated_tests/semantic_prompt \
  --approach semantic_prompt \
  --base-url https://demowebshop.tricentis.com/ \
  --output ./evaluation_reports/semantic_prompt.json
```

Uso sem Neo4j, apenas com analise estatica:

```bash
python3 -m teste_prompt_e2e_semantico.evaluation \
  --tests-dir ./generated_tests/semantic_prompt \
  --approach semantic_prompt \
  --base-url https://demowebshop.tricentis.com/ \
  --skip-graph \
  --output ./evaluation_reports/semantic_prompt.json
```

Quando o pacote estiver instalado, o comando equivalente e:

```bash
evaluate-e2e --tests-dir ./generated_tests/semantic_prompt --skip-graph
```

A CLI:

1. listar arquivos `.spec.ts`;
2. inferir `spec_id` pelo nome do arquivo;
3. carregar o grafo do Neo4j, exceto quando `--skip-graph` e usado;
4. gerar relatorio JSON.

## Proxima Etapa De Implementacao

### Runner Playwright

Adicionar `playwright_runner.py` para execucao controlada:

- executar `npx playwright test arquivo.spec.ts --reporter=json`;
- coletar status, erro e duracao;
- opcionalmente salvar traces/screenshots;
- classificar erro tecnico inicial.

Como o repositorio principal nao depende mais de Node/Playwright, essa etapa pode ser opcional e documentada como parte do ambiente experimental.

### Relatorio Comparativo

Depois de gerar relatorios para `baseline` e `semantic_prompt`, criar um agregador:

```text
evaluation/application/summarize_reports.py
```

Metricas:

- porcentagem de testes com import correto;
- porcentagem com `expect`;
- media de acoes por teste;
- media de cobertura de URLs no grafo;
- media de cobertura de textos no grafo;
- distribuicao de risco de seletores;
- quantidade de URLs desconhecidas;
- quantidade de textos possivelmente inventados;
- resultado de execucao quando disponivel;
- medias da rubrica humana quando preenchida.

## Exemplo De Uso Em Codigo

```python
from pathlib import Path

from teste_prompt_e2e_semantico.evaluation.application.evaluate_test import evaluate_test_file
from teste_prompt_e2e_semantico.evaluation.domain.models import EvaluationCase
from teste_prompt_e2e_semantico.evaluation.infrastructure.filesystem_reports import FileSystemEvaluationReportWriter

case = EvaluationCase(
    spec_id="fluxo_downloads_digitais",
    approach="semantic_prompt",
    test_file=Path("generated_tests/fluxo_downloads_digitais.spec.ts"),
    base_url="https://demowebshop.tricentis.com/",
)

report = evaluate_test_file(case)
FileSystemEvaluationReportWriter().write_json(Path("evaluation_reports/report.json"), [report])
```

## Decisao Metodologica

A avaliacao automatica deve ser tratada como coleta de evidencias, nao como oraculo final de corretude semantica.

O julgamento sobre "este teste representa corretamente a especificacao em linguagem natural?" permanece na rubrica humana descrita em `docs/protocolo_avaliacao_hibrida.md`.
