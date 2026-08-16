# Avaliação auxiliar de prompts E2E

Este é um módulo **não oficial e independente** do gerador de prompts. Ele existe apenas para auxiliar a execução do experimento e a análise dos testes produzidos. Não faz parte do método proposto nem do artefato principal da dissertação.

O módulo lê testes Playwright (`.spec.ts`), coleta evidências estáticas e, opcionalmente, compara URLs e textos de locators com o grafo no Neo4j. A saída padrão é um relatório Markdown destinado à leitura humana, com:

- visão geral da execução;
- explicação curta de como interpretar cada indicador;
- leitura rápida por teste;
- tabelas de estrutura, seletores, prompt e execução;
- URLs e textos que merecem revisão;
- rubrica humana pronta para preenchimento.

As métricas não determinam sozinhas se um teste está correto. Elas indicam pontos para inspeção e devem ser combinadas com a especificação original e a avaliação humana.

## Avaliação posterior de resiliência

A comparação estática e a execução na interface original não medem resiliência.
O protocolo separado de mutações controladas está documentado em
[`../../docs/protocolo_avaliacao_resiliencia.md`](../../docs/protocolo_avaliacao_resiliencia.md).

O plano de mutações deverá ser gerado sem ler os testes produzidos ou seus
resultados. A comparação será pareada, estratificada por classe de mudança e
incluirá somente cenários aprovados nas duas abordagens antes da mutação. O
executor exige um plano com hash interno válido.

### 1. Gerar e verificar o plano

```bash
python3 -m avaliacao_prompts.resilience plan \
  --specs-dir ../teste_prompt_e2e_semantico/specs \
  --prompt-dir ../teste_prompt_e2e_semantico/generated_prompts \
  --output resilience_artifacts/frozen_mutation_plan.json

python3 -m avaliacao_prompts.resilience verify-plan \
  resilience_artifacts/frozen_mutation_plan.json
```

O gerador não recebe diretório de testes. Ele usa a associação entre etapas e
controles registrada nos prompts estruturados antes da geração dos `.spec.ts` e
produz todos os operadores aplicáveis, sem escolher mutações depois dos
resultados. O plano congelado atual contém 49 alvos e 182 mutações.

### 2. Preparar cópias instrumentadas

```bash
python3 -m avaliacao_prompts.resilience prepare-execution \
  --baseline-dir ../teste_prompt_e2e_semantico/generated_tests/baseline \
  --structured-dir ../teste_prompt_e2e_semantico/generated_tests/structured_context \
  --fixture playwright_resilience/fixture.ts \
  --plan resilience_artifacts/frozen_mutation_plan.json \
  --allowlist resilience_artifacts/eligibility_candidates/track_P_gpt-5.6-sol.json \
  --semantic-review resultados_adequacao_semantica_20260728/semantic_review.csv \
  --track-id P \
  --model-id gpt-5.6-sol \
  --output-dir resilience_artifacts/prepared_execution
```

Os testes originais não são modificados. Nas cópias, somente a origem da
importação de `test` e `expect` é trocada pela fixture de instrumentação; hashes
dos originais, das cópias, da fixture, do plano, da allowlist e da revisão
semântica ficam no manifesto. Um diretório existente nunca é removido ou
sobrescrito.

### 3. Congelar a elegibilidade

```bash
python3 -m avaliacao_prompts.resilience eligibility \
  --execution-manifest resilience_artifacts/prepared_execution/execution_manifest.json \
  --playwright-config playwright.config.ts \
  --node-project-dir ../.. \
  --output-dir resilience_artifacts/eligibility \
  --repetitions 3 \
  --execute-live-site
```

A elegibilidade é executada e assinada separadamente. Somente cenários com 3/3
aprovações nas duas condições podem ser consumidos pela campanha de mutação.

### 4. Executar as mutações

```bash
python3 -m avaliacao_prompts.resilience run \
  --execution-manifest resilience_artifacts/prepared_execution/execution_manifest.json \
  --eligibility-results resilience_artifacts/eligibility/eligibility_results.json \
  --playwright-config playwright.config.ts \
  --node-project-dir ../.. \
  --control-test playwright_resilience/control.spec.ts \
  --output-dir resilience_artifacts/results \
  --repetitions 3 \
  --mutations-per-scenario 2 \
  --execute-live-site
```

Sem `--execute-live-site`, nenhuma requisição é enviada. A opção `--mutation`
serve somente para depuração. `--mutations-per-scenario 1` ou `2` seleciona
deterministicamente mutações E1 e E2, sem ler os resultados das condições,
dando preferência a uma mutação de cada estrato. E3 é excluído porque altera o
contrato visível/acessível.
O executor primeiro identifica cenários aprovados nas duas condições. Para cada
mutante, ele também confirma que ambos os testes interagiam com o mesmo alvo
antes da mudança. Mutantes não aplicáveis ou funcionalmente inválidos permanecem
registrados e não entram no denominador. Uma execução mutada só sobrevive quando
passa e registra interação com o alvo correto. JSON, stderr, trace e screenshot
são mantidos em diretórios exclusivos por execução.

## Execução

A partir deste diretório:

```bash
python3 -m avaliacao_prompts \
  --tests-dir ../teste_prompt_e2e_semantico/generated_tests/structured_context \
  --approach structured_context \
  --prompt-dir ../teste_prompt_e2e_semantico/generated_prompts \
  --specs-dir ../teste_prompt_e2e_semantico/specs \
  --base-url https://demowebshop.tricentis.com/ \
  --skip-graph \
  --output ./relatorios/structured_context.md
```

Remova `--skip-graph` e informe `--neo4j-uri`, `--neo4j-user` e `--neo4j-password` para incluir a análise de conformidade com o grafo.

O pacote também pode ser instalado para disponibilizar o comando `avaliar-prompts`.

## Testes

```bash
python3 -m unittest discover -s tests -v
```
