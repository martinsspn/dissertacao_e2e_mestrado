# Resultado da avaliação de resiliência

## Escopo

- Plano de mutações: `7e1ed1318e46271b4a055e9a475e38b85f31b6f22c4614d4033656450fcbbbfc`.
- Cenários elegíveis nas duas condições: 2.
- Repetições: 3.
- Mutações selecionadas: 4.
- Seleção reduzida: até 2 mutações neutras por cenário (uma E1 e uma E2 quando disponível; desempate por hash do plano).
- Mutantes inválidos pelo controle diferencial: 2.
- Mutantes não aplicáveis porque ambos os testes não interagiram com o alvo original: 0.
- Os resultados são apresentados por estrato; não há conclusão universal baseada em média única.

## Comparação pareada por estrato

| Estrato | Pares válidos | Ambos passam | Só baseline | Só estruturado | Ambos falham | McNemar exato |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| E1 | 2 | 2 | 0 | 0 | 0 | 1.0000 |

## Resultado por mutação

Condição A: **baseline**. Condição B: **structured_context**.

| Cenário | Mutação | Estrato | Operador | Controle | Aplicável ao par | A | B |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `fluxo_computadores_desktops` | `mutation-3eaa4cad6dfee398` | E1 | `insert_noninteractive_sibling_before` | inválido | não | - | - |
| `fluxo_computadores_desktops` | `mutation-970dfe4afdc63621` | E1 | `insert_wrapper` | inválido | não | - | - |
| `suite_navegar_sobre_nos` | `mutation-5b72726c4f561716` | E1 | `insert_noninteractive_sibling_before` | válido | sim | passed_interacted, passed_interacted, passed_interacted | passed_interacted, passed_interacted, passed_interacted |
| `suite_navegar_sobre_nos` | `mutation-d20cb5bb3f6fd31b` | E1 | `insert_wrapper` | válido | sim | passed_interacted, passed_interacted, passed_interacted | passed_interacted, passed_interacted, passed_interacted |

## Cenários elegíveis

- `fluxo_computadores_desktops`
- `suite_navegar_sobre_nos`

## Limite

Os valores descrevem somente os operadores e elementos do plano utilizado nesta execução. Mudanças do contrato visível ou acessível não devem ser interpretadas como o mesmo fenômeno de mudanças internas neutras. Cenários diferentes podem reutilizar o mesmo componente da interface; nesses casos, os pares não são evidências independentes da quantidade de componentes alterados.
