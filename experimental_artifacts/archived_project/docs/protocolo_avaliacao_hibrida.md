# Protocolo De Avaliacao Hibrida

> Este documento trata da qualidade dos testes gerados e de sua execução na
> interface original. A avaliação posterior de resiliência possui protocolo
> próprio em [`protocolo_avaliacao_resiliencia.md`](protocolo_avaliacao_resiliencia.md).

## Objetivo

Avaliar se os testes E2E gerados a partir dos prompts representam corretamente a especificacao em linguagem natural e se sao tecnicamente utilizaveis em Playwright.

A avaliacao nao deve usar apenas o resultado `passou/falhou`, porque um teste pode falhar por detectar corretamente um comportamento ausente na aplicacao. Por isso, a avaliacao separa:

- qualidade do teste gerado;
- comportamento observado na execucao;
- causa provavel de falha.

## Ideia Central

Um teste gerado e considerado eficaz quando:

1. expressa corretamente a intencao da especificacao em linguagem natural;
2. interage com os elementos corretos;
3. valida o resultado esperado com assercoes observaveis;
4. usa rotas, elementos e seletores fundamentados no grafo sempre que possivel;
5. pode ser executado pelo Playwright.

O teste nao precisa necessariamente passar para ser considerado conceitualmente correto. Se a aplicacao nao cumprir o comportamento especificado, a falha pode ser uma falha legitima da aplicacao.

## Avaliacao Automatica

A parte automatica mede propriedades objetivas e reprodutiveis.

### Entradas

- especificacao em linguagem natural;
- teste Playwright gerado;
- grafo navegacional usado no prompt;
- prompt utilizado para gerar o teste;
- logs de execucao do Playwright;
- resultado da execucao (`passed`, `failed`, `timed_out`, `syntax_error` etc.).

### Saidas

Um arquivo estruturado por teste, por exemplo:

```json
{
  "spec_id": "fluxo_downloads_digitais",
  "approach": "structured_context",
  "test_file": "generated_tests/fluxo_downloads_digitais.spec.ts",
  "static_analysis": {
    "has_playwright_import": true,
    "has_test_block": true,
    "has_expect_assertion": true,
    "uses_wait_for_timeout": false,
    "xpath_count": 0,
    "locator_count": 5,
    "semantic_locator_count": 4,
    "graph_url_coverage": 1.0,
    "unknown_urls": [],
    "selector_risk": "low"
  },
  "execution": {
    "status": "failed",
    "error_type": "expectation_failed",
    "error_message_excerpt": "Expected dialog to be visible"
  },
  "human_review": {
    "conceptual_correctness": null,
    "failure_classification": null
  }
}
```

### Metricas Automaticas

#### Executabilidade

- O arquivo possui import de `@playwright/test`?
- Existe bloco `test(...)`?
- O codigo TypeScript e parseavel?
- O Playwright consegue iniciar a execucao?

#### Estrutura De Teste

- Existe pelo menos uma chamada `expect(...)`?
- O teste navega para a `base_url` esperada?
- O teste contem acoes de usuario (`click`, `fill`, `selectOption`, `check`, etc.)?
- O teste evita `waitForTimeout`?

#### Fundamentacao No Grafo

- URLs usadas no teste aparecem no grafo ou derivam da `base_url`?
- Textos usados em locators aparecem em paginas/transicoes relevantes?
- Seletores por `id`, `name`, `href`, texto ou role aparecem entre os seletores recomendados?
- O teste usa rotas ou elementos que nao aparecem no contexto fornecido?

#### Robustez De Seletores

Classificar seletores usados no teste:

- `low risk`: `getByRole`, `getByLabel`, `getByPlaceholder`, `getByText` com texto especifico, `id`, `name`, `data-testid`;
- `medium risk`: CSS curto ou `href`;
- `high risk`: XPath, `nth-child`, classes genericas, indices ou texto pouco informativo.

#### Resultado De Execucao

Registrar:

- `passed`;
- `failed`;
- `timed_out`;
- `syntax_error`;
- `runtime_error`;
- `environment_error`.

Quando houver falha, extrair uma causa tecnica inicial:

- seletor nao encontrado;
- timeout de visibilidade;
- URL inesperada;
- assercao falhou;
- erro de sintaxe;
- erro de dependencia/ambiente;
- erro desconhecido.

## Avaliacao Humana

A parte humana avalia a aderencia semantica, que a ferramenta nao consegue decidir com seguranca.

### Rubrica

Cada criterio recebe nota:

- `0`: nao atende;
- `1`: atende parcialmente;
- `2`: atende completamente.

Critérios:

| Criterio | Pergunta |
|---|---|
| Fluxo correto | O teste executa os passos principais pedidos na especificacao? |
| Alvo correto | O teste interage com os elementos esperados? |
| Assercao correta | O teste valida o resultado esperado pela especificacao? |
| Aderencia ao grafo | O teste se apoia em rotas, paginas e elementos disponiveis no contexto? |
| Robustez pratica | Os seletores e esperas seriam aceitaveis em um projeto real? |
| Utilidade geral | O teste exigiria pouca ou nenhuma correcao manual? |

### Classificacao Da Falha

Se a execucao falhar, o avaliador classifica a causa:

| Classe | Definicao |
|---|---|
| `application_failure` | O teste representa corretamente a especificacao, mas a aplicacao nao exibiu o comportamento esperado. |
| `generated_test_failure` | O teste falhou por erro de geracao: fluxo errado, seletor inventado, assercao inadequada, rota inexistente etc. |
| `environment_failure` | A falha decorre de ambiente, rede, container, indisponibilidade, dependencia ou instabilidade externa. |
| `inconclusive` | Nao ha informacao suficiente para separar as causas com seguranca. |

## Comparacao Entre Abordagens

Para cada especificacao, gerar dois testes:

- `baseline`: especificacao em linguagem natural enviada diretamente a LLM, sem template produzido pelo gerador;
- `structured_context`: prompt produzido pelo gerador com a especificacao segmentada e o contexto estruturado da interface.

O gerador nao cria arquivo de prompt para o baseline. A especificacao `.txt` e a propria entrada experimental dessa condicao.

Comparar:

- taxa de codigo executavel;
- taxa de testes com assercoes;
- quantidade de rotas/seletores inventados;
- distribuicao de risco dos seletores;
- nota media da rubrica humana;
- quantidade de falhas classificadas como `generated_test_failure`;
- quantidade de casos `application_failure` corretamente detectados.
- quantidade de caracteres ou tokens do prompt;
- tempo e custo de geracao, quando disponibilizados pela LLM.

## Como Automatizar

A parte automatizada é mantida em uma ferramenta auxiliar separada do gerador:

```text
python_app/avaliacao_prompts/avaliacao_prompts/
  static_analysis.py      # analisa o arquivo .spec.ts
  graph_conformance.py    # compara URLs/seletores com o contexto do grafo
  playwright_runner.py    # executa testes e coleta logs
  markdown_reports.py     # organiza as evidencias em relatorio legivel
```

O desenho tecnico inicial desse modulo esta documentado em `docs/projeto_modulo_avaliacao.md`.

### Passo 1: Analise Estatica

Ler o `.spec.ts` gerado e extrair:

- imports;
- chamadas `test`;
- chamadas `expect`;
- URLs em `page.goto`;
- locators (`getByRole`, `getByText`, `locator`, XPath etc.);
- chamadas de acao (`click`, `fill`, `check`, `selectOption`);
- uso de esperas frageis (`waitForTimeout`).

Essa etapa pode comecar com expressoes regulares simples e depois evoluir para parser TypeScript, se necessario.

### Passo 2: Conformidade Com O Grafo

Comparar os dados extraidos do teste com o contexto usado no prompt:

- `page.goto(...)` deve apontar para `base_url` ou URLs presentes no grafo;
- textos de locators devem aparecer no texto visivel, elementos ou seletores do grafo;
- `id`, `name`, `href` e outros atributos devem aparecer nos seletores recomendados;
- XPath e seletores estruturais devem ser marcados como risco alto.

### Passo 3: Execucao Controlada

Executar os testes com Playwright e salvar:

- status final;
- stack trace;
- mensagem de erro;
- screenshot ou trace, quando disponivel;
- tempo de execucao.

O resultado automatico nao decide sozinho se o teste e bom. Ele apenas fornece evidencias para a rubrica humana.

### Passo 4: Relatorio

Gerar um arquivo `.json` ou `.csv` com uma linha por teste:

```text
spec_id,approach,compile_ok,has_expect,unknown_url_count,selector_risk,execution_status,error_type,human_score_total,failure_classification
```

Esse relatorio permite comparar `baseline` e `structured_context` com estatistica descritiva.

## Cenario Ideal E Cenario Viavel

Cenario ideal:

- dois avaliadores humanos independentes;
- rubrica predefinida;
- calculo de concordancia entre avaliadores;
- revisao de divergencias.

Cenario viavel para o mestrado:

- um avaliador humano;
- rubrica fixa definida antes da avaliacao;
- justificativas curtas por teste;
- metricas automaticas para reduzir subjetividade;
- ameaca a validade explicitada no texto da dissertacao.

## Ameacas A Validade

- A avaliacao humana pode introduzir subjetividade.
- Um unico site alvo pode limitar a generalizacao.
- Diferentes LLMs podem produzir resultados distintos.
- O grafo gerado pelo crawler pode nao conter todos os fluxos relevantes.
- Um teste correto pode falhar por instabilidade do ambiente ou por defeito real da aplicacao.
- Analise estatica baseada em padroes textuais pode deixar passar casos complexos.
