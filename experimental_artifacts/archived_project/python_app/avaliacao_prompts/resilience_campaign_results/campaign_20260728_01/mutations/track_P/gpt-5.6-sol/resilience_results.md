# Resultado da avaliação de resiliência

## Escopo

- Plano de mutações: `054db1613694d3f96ce00a85fc77e01126e32b3e58225e63652864c038e81979`.
- Cenários elegíveis nas duas condições: 4.
- Repetições: 3.
- Mutações selecionadas: 8.
- Seleção reduzida: até 2 mutações neutras por cenário (uma E1 e uma E2 quando disponível; desempate por hash do plano).
- Mutantes inválidos pelo controle diferencial: 0.
- Mutantes não aplicáveis porque ambos os testes não interagiram com o alvo original: 0.
- Os resultados são apresentados por estrato; não há conclusão universal baseada em média única.

## Comparação pareada por estrato

| Estrato | Pares válidos | Ambos passam | Só baseline | Só estruturado | Ambos falham | McNemar exato |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| E1 | 4 | 4 | 0 | 0 | 0 | 1.0000 |
| E2 | 4 | 0 | 0 | 4 | 0 | 0.1250 |

## Resultado por mutação

Condição A: **baseline**. Condição B: **structured_context**.

| Cenário | Mutação | Estrato | Operador | Controle | Aplicável ao par | A | B |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `suite_busca_blue_jeans` | `mutation-f026cc4f906a76d1` | E1 | `insert_noninteractive_sibling_before` | válido | sim | passed_interacted, passed_interacted, passed_interacted | passed_interacted, passed_interacted, passed_interacted |
| `suite_busca_blue_jeans` | `mutation-8b066797110a117f` | E2 | `input_submit_to_button` | válido | sim | locator_not_found, locator_not_found, locator_not_found | passed_interacted, passed_interacted, passed_interacted |
| `suite_detalhes_fiction` | `mutation-b745f8523a2ad8e7` | E1 | `insert_noninteractive_sibling_before` | válido | sim | passed_interacted, passed_interacted, passed_interacted | passed_interacted, passed_interacted, passed_interacted |
| `suite_detalhes_fiction` | `mutation-361a9103a5072567` | E2 | `input_submit_to_button` | válido | sim | locator_not_found, locator_not_found, locator_not_found | passed_interacted, passed_interacted, passed_interacted |
| `suite_login_invalido` | `mutation-5fdf1828cabd53de` | E1 | `insert_wrapper` | válido | sim | passed_interacted, passed_interacted, passed_interacted | passed_interacted, passed_interacted, passed_interacted |
| `suite_login_invalido` | `mutation-439ad347e64028d4` | E2 | `rename_id` | válido | sim | locator_not_found, locator_not_found, locator_not_found | passed_interacted, passed_interacted, passed_interacted |
| `suite_login_valido` | `mutation-ac2305bb5ac9e7a3` | E1 | `insert_noninteractive_sibling_before` | válido | sim | passed_interacted, passed_interacted, passed_interacted | passed_interacted, passed_interacted, passed_interacted |
| `suite_login_valido` | `mutation-01c92a29170fe542` | E2 | `input_submit_to_button` | válido | sim | locator_not_found, locator_not_found, locator_not_found | passed_interacted, passed_interacted, passed_interacted |

## Cenários elegíveis

- `suite_busca_blue_jeans`
- `suite_detalhes_fiction`
- `suite_login_invalido`
- `suite_login_valido`

## Limite

Os valores descrevem somente os operadores e elementos do plano utilizado nesta execução. Mudanças do contrato visível ou acessível não devem ser interpretadas como o mesmo fenômeno de mudanças internas neutras. Cenários diferentes podem reutilizar o mesmo componente da interface; nesses casos, os pares não são evidências independentes da quantidade de componentes alterados.
