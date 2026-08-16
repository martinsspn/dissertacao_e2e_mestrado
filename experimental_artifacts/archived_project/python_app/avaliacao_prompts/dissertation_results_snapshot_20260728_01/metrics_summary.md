# Snapshot consolidado dos resultados

Este diretório reúne as métricas derivadas e aponta, por hash SHA-256, para os artefatos primários. Nenhum arquivo LaTeX foi alterado.

## Execução e adequação semântica

| Modelo/rodada | Baseline: execução | Estruturado: execução | Baseline: adequado | Estruturado: adequado |
|---|---:|---:|---:|---:|
| gpt-5.6-sol / gpt_original_12 | 7/12 | 7/12 | 7/12 | 7/12 |
| gemini-3.6-flash / gemini_new_20 | 8/20 | 12/20 | 12/20 | 18/20 |
| qwen2.5-coder:7b / qwen_new_20 | 0/20 | 2/20 | 0/20 | 0/20 |
| qwen2.5-coder:7b / qwen_old_14 | 0/14 | 2/14 | 0/14 | 0/14 |

## Reparo

- Tentativas: 94; coletadas: 93.
- Reparos efetivos: 5 (5.32%).
- Tempo total de inferência: 3379.884 s; tokens de entrada/saída: 130114/35313.

## Resiliência

- 20 mutações selecionadas, 16 controles válidos e 14 unidades pareadas aplicáveis.
- Sobrevivência robusta: baseline 9/14; contexto estruturado 14/14.
- McNemar exato bilateral agregado: p=0.0625.
- Execuções Playwright de resiliência: 366.

Os resultados de resiliência devem ser apresentados prioritariamente por modelo, porque o agregado combina amostras pequenas e heterogêneas.

## Arquivos

- `metrics_summary.json`: todas as métricas consolidadas.
- `generation_execution_semantic.csv`: uma linha por condição e rodada.
- `paired_semantic_comparison.csv`: comparação pareada dos escores.
- `artifact_index.csv`: localização, estado e hash dos artefatos primários.
