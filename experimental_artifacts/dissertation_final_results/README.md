# Consolidação final usada na dissertação

Esta pasta reúne as métricas derivadas da base final de 64 pares únicos, ou
128 arquivos. Os resultados são apresentados por modelo porque as quantidades
de especificações e os ambientes de geração não foram iguais.

## Execução e adequação integral

| Modelo | Pares | Aprovação baseline | Aprovação estruturada | Adequação baseline | Adequação estruturada |
|---|---:|---:|---:|---:|---:|
| GPT-5.6 Sol | 12 | 7/12 | 7/12 | 7/12 | 7/12 |
| Gemini 3.6 Flash | 20 | 8/20 | 12/20 | 12/20 | 18/20 |
| Qwen 2.5 Coder | 32 | 0/32 | 3/32 | 0/32 | 0/32 |

## Comparação pareada

As tabelas `paired_execution.csv`, `paired_integral_adequacy.csv` e
`paired_semantic_scores.csv` mostram, respectivamente, as transições de
execução, as transições de adequação integral e as diferenças dos escores
semânticos dentro de cada par.

As taxas marginais iguais do GPT não significam identidade entre os pares: em
execução, seis pares foram aprovados nas duas condições, um somente na
baseline, um somente na condição estruturada e quatro em nenhuma delas.

## Esforço de geração do Qwen

| Métrica | Baseline | Estruturado | Variação |
|---|---:|---:|---:|
| Tokens de entrada | 6.362 | 40.067 | +529,8% |
| Tokens de saída | 7.370 | 10.450 | +41,8% |
| Tempo total do cliente | 502,102 s | 799,292 s | +59,2% |
| Tempo médio por chamada | 15,691 s | 24,978 s | +59,2% |

## Correção automática na base final

Uma tentativa sem estado com o Qwen 2.5 Coder foi aplicada a cada arquivo
reprovado da base final.

| Indicador | Resultado |
|---|---:|
| Arquivos submetidos | 91 |
| Arquivos coletáveis após a correção | 90 |
| Arquivos aprovados após a correção | 6 |
| Aprovações sem adequação integral | 1 |
| Reparos efetivos | 5/91 (5,49%) |
| Tempo total de inferência | 3.251,624 s |
| Tokens de entrada | 125.012 |
| Tokens de saída | 34.040 |
| Alterações de linha | 560 |
| Similaridade média | 0,9122 |

## Resiliência

A análise principal corresponde à trilha P da campanha, formada por pares
originalmente aprovados. Foram selecionadas 14 mutações, das quais 12 tiveram
controle válido e 10 permaneceram aplicáveis. A baseline sobreviveu a 6/10 e a
condição estruturada a 10/10. No estrato E1, ambas sobreviveram a 5/5; no E2,
a baseline sobreviveu a 1/5 e a condição estruturada a 5/5.

## Proveniência

Os dados primários e relatórios usados nesta consolidação estão em:

- `../archived_project/python_app/avaliacao_prompts/resultados_adequacao_semantica_20260728/`;
- `../archived_project/python_app/avaliacao_prompts/repair_results/qwen25coder_repair_20260728_01/`;
- `../archived_project/python_app/avaliacao_prompts/resilience_campaign_results/campaign_20260728_01/`;
- `../archived_project/python_app/teste_prompt_e2e_semantico/ollama_runs/`.

O script `derive_final_results.py` recompõe as métricas principais diretamente
dos CSVs e manifestos preservados.

