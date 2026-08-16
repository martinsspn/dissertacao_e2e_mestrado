# Resultado da avaliação de resiliência

## Escopo

- Plano de mutações: `44fe459525f513719dc46a9bb394fa77d00c8fe1679bc77d4fbedb16b5da4e7b`.
- Cenários elegíveis nas duas condições: 4.
- Repetições: 1.
- Mutações selecionadas: 8.
- Seleção reduzida: até 2 mutações neutras por cenário (uma E1 e uma E2 quando disponível; desempate por hash do plano).
- Mutantes inválidos pelo controle diferencial: 0.
- Mutantes não aplicáveis porque ambos os testes não interagiram com o alvo original: 3.
- Os resultados são apresentados por estrato; não há conclusão universal baseada em média única.

## Comparação pareada por estrato

| Estrato | Pares válidos | Ambos passam | Só baseline | Só estruturado | Ambos falham | McNemar exato |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| E1 | 2 | 2 | 0 | 0 | 0 | 1.0000 |
| E2 | 3 | 0 | 0 | 3 | 0 | 0.2500 |

## Resultado por mutação

Condição A: **baseline**. Condição B: **structured_context**.

| Cenário | Mutação | Estrato | Operador | Controle | Aplicável ao par | A | B |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `suite_adicionar_carrinho` | `mutation-7c48b3e946d99eaa` | E1 | `insert_noninteractive_sibling_before` | válido | não | - | - |
| `suite_adicionar_carrinho` | `mutation-766d2310c5144a4d` | E2 | `input_submit_to_button` | válido | sim | failed | passed |
| `suite_busca_blue_jeans` | `mutation-dd9a3b88732c15c6` | E1 | `insert_noninteractive_sibling_before` | válido | sim | passed | passed |
| `suite_busca_blue_jeans` | `mutation-8b066797110a117f` | E2 | `input_submit_to_button` | válido | sim | failed | passed |
| `suite_detalhes_fiction` | `mutation-9eb1e5a299eb758d` | E1 | `insert_wrapper` | válido | sim | passed | passed |
| `suite_detalhes_fiction` | `mutation-361a9103a5072567` | E2 | `input_submit_to_button` | válido | sim | failed | passed |
| `suite_limpar_carrinho` | `mutation-0631d1b7c50168dd` | E1 | `insert_noninteractive_sibling_before` | válido | não | - | - |
| `suite_limpar_carrinho` | `mutation-dfcce8f46a857a7c` | E2 | `rename_id` | válido | não | - | - |

## Cenários elegíveis

- `suite_adicionar_carrinho`
- `suite_busca_blue_jeans`
- `suite_detalhes_fiction`
- `suite_limpar_carrinho`

## Limite

Os valores descrevem somente os operadores e elementos do plano congelado. Mutações do contrato visível ou acessível (E3) não são interpretadas como o mesmo fenômeno de E1/E2. Cenários diferentes podem reutilizar o mesmo componente da interface; nesses casos, os pares não são evidências independentes da quantidade de componentes alterados.
