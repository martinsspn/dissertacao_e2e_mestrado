# Avaliação de adequação semântica

A unidade é o arquivo gerado comparado à respectiva especificação em linguagem natural.
Aprovação em execução e adequação semântica são registradas separadamente.

## Rubrica

- fluxo: presença e coerência das etapas e pré-condições pedidas;
- alvo: aplicação, dados, produtos e controles corretos;
- asserção: capacidade de comprovar todos os resultados solicitados.

Cada eixo recebe 0 (não atende), 1 (parcial) ou 2 (completo). Um arquivo é
**adequado** somente com 6/6; **parcialmente adequado** com 3–5; e
**inadequado** com 0–2. Uma expectativa assíncrona sem `await`, um teste
fragmentado que depende de outro contexto ou um DOM simulado não recebe
crédito integral.

## Resultado por condição

| Modelo | Rodada | Condição | Arquivos | Adequados | Parciais | Inadequados | Média / 6 | Passaram | Erro de sintaxe |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| gemini-3.6-flash | gemini_new_20 | baseline | 20 | 12 | 8 | 0 | 5.500 | 8 | 1 |
| gemini-3.6-flash | gemini_new_20 | structured_context | 20 | 18 | 2 | 0 | 5.900 | 12 | 0 |
| gpt-5.6-sol | gpt_original_12 | baseline | 12 | 7 | 5 | 0 | 5.583 | 7 | 0 |
| gpt-5.6-sol | gpt_original_12 | structured_context | 12 | 7 | 5 | 0 | 5.583 | 7 | 0 |
| qwen2.5-coder:7b | qwen_new_20 | baseline | 20 | 0 | 19 | 1 | 3.700 | 0 | 0 |
| qwen2.5-coder:7b | qwen_new_20 | structured_context | 20 | 0 | 16 | 4 | 3.900 | 2 | 0 |
| qwen2.5-coder:7b | qwen_old_14 | baseline | 14 | 0 | 13 | 1 | 3.143 | 0 | 0 |
| qwen2.5-coder:7b | qwen_old_14 | structured_context | 14 | 0 | 12 | 2 | 3.571 | 2 | 0 |

## Comparação pareada da nota semântica

| Modelo | Rodada | Pares | Estruturado melhor | Mesma nota | Estruturado pior | Delta médio / 6 |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| gemini-3.6-flash | gemini_new_20 | 20 | 8 | 11 | 1 | +0.400 |
| gpt-5.6-sol | gpt_original_12 | 12 | 1 | 10 | 1 | +0.000 |
| qwen2.5-coder:7b | qwen_new_20 | 20 | 9 | 6 | 5 | +0.200 |
| qwen2.5-coder:7b | qwen_old_14 | 14 | 8 | 3 | 3 | +0.429 |

## Leitura comparativa

- No Gemini, o contexto estruturado elevou os testes adequados de 12/20
  para 18/20 e as aprovações de execução de 8/20 para 12/20. A única
  piora semântica foi a omissão de quantidade e preço no cenário com dois
  produtos no carrinho.
- No GPT-5.6 Sol, as duas condições ficaram com 7/12 testes adequados e
  média 5,583/6. O contexto corrigiu a ambiguidade de Add to cart, mas
  introduziu o papel incorreto para Continue no registro.
- No Qwen, o contexto aumentou a média nas duas rodadas, mas nenhum arquivo
  alcançou os três eixos completos. Na rodada nova, a média passou de
  3,700 para 3,900 e houve 9 melhorias, 6 empates e 5 pioras.
- Aprovação em execução não implica conformidade integral: o Qwen
  estruturado de Digital downloads passou sem verificar os itens, e o
  Gemini estruturado de dois produtos passou sem verificar quantidade e
  preço. O inverso também ocorre quando o fluxo é semanticamente próximo,
  mas um locator ou papel incorreto impede a execução.
- Os principais defeitos semânticos observados foram aplicação ou DOM
  inventados, pré-condições omitidas, fragmentação de um fluxo em testes
  sem estado compartilhado, asserções assíncronas sem await e oráculos que
  verificam apenas parte do resultado solicitado.

## Observações de escopo

- A rodada Qwen antiga é a rodada corrigida de 14 pares; a rodada anterior
  superseded não foi contada novamente.
- O baseline Gemini possui um arquivo com erro de sintaxe. Para não impedir
  a coleta dos demais, os outros 19 foram executados em uma cópia isolada.
- Os arquivos originais não foram modificados e cada condição foi executada
  em processo separado, com um worker e novo contexto por teste.

A justificativa individual de cada nota está em `semantic_review.csv`.
