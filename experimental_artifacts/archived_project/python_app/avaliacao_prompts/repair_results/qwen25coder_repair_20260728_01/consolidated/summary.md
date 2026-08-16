# Resultado da rodada única de reparo

Todos os arquivos receberam no máximo uma chamada sem estado ao Qwen 2.5 Coder 7B.
Aprovação em execução só conta como reparo bem-sucedido quando a revisão também confirma 6/6.

## Visão geral

| Indicador | Resultado |
| --- | ---: |
| Arquivos reparados | 94 |
| Coletáveis após reparo | 93 |
| Aprovados em execução | 6 |
| Falsos sucessos semânticos | 1 |
| Reparos executáveis e semanticamente adequados | 5 |
| Taxa efetiva de reparo | 5.3% |
| Tempo total de inferência | 3379.9 s |
| Tokens de entrada | 130114 |
| Tokens de saída | 35313 |
| Churn total | 588 linhas |
| Tempo por reparo efetivo | 676.0 s |

## Resultado por origem

| Origem | Rodada | Condição | Tentados | Coletados | Passaram | Reparos efetivos | Tempo médio (s) | Tokens | Churn |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| gemini-3.6-flash | gemini_new_20 | baseline | 12 | 11 | 1 | 1 | 36.7 | 17240 | 62 |
| gemini-3.6-flash | gemini_new_20 | structured_context | 8 | 8 | 2 | 2 | 39.5 | 17162 | 17 |
| gpt-5.6-sol | gpt_original_12 | baseline | 5 | 5 | 1 | 1 | 56.6 | 8569 | 46 |
| gpt-5.6-sol | gpt_original_12 | structured_context | 5 | 5 | 0 | 0 | 76.9 | 15152 | 50 |
| qwen2.5-coder:7b | qwen_new_20 | baseline | 20 | 20 | 0 | 0 | 18.6 | 17768 | 145 |
| qwen2.5-coder:7b | qwen_new_20 | structured_context | 18 | 18 | 1 | 0 | 41.8 | 45859 | 93 |
| qwen2.5-coder:7b | qwen_old_14 | baseline | 14 | 14 | 0 | 0 | 20.6 | 13282 | 114 |
| qwen2.5-coder:7b | qwen_old_14 | structured_context | 12 | 12 | 1 | 1 | 45.2 | 30395 | 61 |

## Pares provisoriamente elegíveis para mutação após reparo

- gemini-3.6-flash / gemini_new_20 / fluxo_computadores_desktops
- gemini-3.6-flash / gemini_new_20 / suite_cadastro_campos_obrigatorios
- gemini-3.6-flash / gemini_new_20 / suite_cadastro_confirmacao_senha
- gemini-3.6-flash / gemini_new_20 / suite_navegar_categoria_livros
- gemini-3.6-flash / gemini_new_20 / suite_navegar_sobre_nos
- gemini-3.6-flash / gemini_new_20 / user_registration_book_purchase
- gpt-5.6-sol / gpt_original_12 / suite_adicionar_carrinho
- gpt-5.6-sol / gpt_original_12 / suite_busca_blue_jeans
- gpt-5.6-sol / gpt_original_12 / suite_detalhes_fiction
- gpt-5.6-sol / gpt_original_12 / suite_limpar_carrinho
- gpt-5.6-sol / gpt_original_12 / suite_login_invalido
- gpt-5.6-sol / gpt_original_12 / suite_login_valido
- gpt-5.6-sol / gpt_original_12 / suite_logout

Os pares acima combinam testes originais já aprovados com reparos efetivos.
Eles ainda precisam passar em três repetições normalizadas antes do congelamento.
O fluxo de registro e compra deve permanecer fora da campanha no site público
por criar contas permanentes.
