# Resultado da avaliação de resiliência

## Escopo

- Plano de mutações: `054db1613694d3f96ce00a85fc77e01126e32b3e58225e63652864c038e81979`.
- Cenários elegíveis nas duas condições: 1.
- Repetições: 3.
- Mutações selecionadas: 2.
- Seleção reduzida: até 2 mutações neutras por cenário (uma E1 e uma E2 quando disponível; desempate por hash do plano).
- Mutantes inválidos pelo controle diferencial: 0.
- Mutantes não aplicáveis porque ambos os testes não interagiram com o alvo original: 0.
- Os resultados são apresentados por estrato; não há conclusão universal baseada em média única.

## Comparação pareada por estrato

| Estrato | Pares válidos | Ambos passam | Só baseline | Só estruturado | Ambos falham | McNemar exato |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| E1 | 1 | 1 | 0 | 0 | 0 | 1.0000 |
| E2 | 1 | 0 | 0 | 1 | 0 | 1.0000 |

## Resultado por mutação

Condição A: **baseline**. Condição B: **structured_context**.

| Cenário | Mutação | Estrato | Operador | Controle | Aplicável ao par | A | B |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `suite_adicionar_carrinho` | `mutation-defa59a332c6148b` | E1 | `insert_noninteractive_sibling_before` | válido | sim | passed_interacted, passed_interacted, passed_interacted | passed_interacted, passed_interacted, passed_interacted |
| `suite_adicionar_carrinho` | `mutation-766d2310c5144a4d` | E2 | `input_submit_to_button` | válido | sim | locator_not_found, locator_not_found, locator_not_found | passed_interacted, passed_interacted, passed_interacted |

## Cenários elegíveis

- `suite_adicionar_carrinho`

## Limite

Os valores descrevem somente os operadores e elementos do plano utilizado nesta execução. Mudanças do contrato visível ou acessível não devem ser interpretadas como o mesmo fenômeno de mudanças internas neutras. Cenários diferentes podem reutilizar o mesmo componente da interface; nesses casos, os pares não são evidências independentes da quantidade de componentes alterados.
