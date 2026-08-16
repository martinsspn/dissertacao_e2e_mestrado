# Resultado da avaliação de resiliência

## Escopo

- Plano de mutações: `eb8b218eb4610c65ff6e57943d2b3af64e71d11aed779640c90fc6b050fba0c8`.
- Cenários elegíveis nas duas condições: 1.
- Repetições: 1.
- Mutações selecionadas: 3.
- Modo de seleção: `full_plan`.
- Mutantes inválidos pelo controle diferencial: 1.
- Mutantes não aplicáveis porque ambos os testes não interagiram com o alvo original: 0.
- Os resultados são apresentados por estrato; não há conclusão universal baseada em média única.

## Comparação pareada por estrato

| Estrato | Pares válidos | Ambos passam | Só baseline | Só estruturado | Ambos falham | McNemar exato |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| implementation_attribute_change | 2 | 1 | 0 | 1 | 0 | 1.0000 |

## Resultado por mutação

Condição A: **baseline**. Condição B: **structured_context**.

| Cenário | Mutação | Estrato | Operador | Controle | Aplicável ao par | A | B |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `suite_busca_blue_jeans` | `mutation-7b4b97f072a744db` | implementation_attribute_change | `rename_id` | inválido | não | - | - |
| `suite_busca_blue_jeans` | `mutation-c46dd5a0d76ba968` | implementation_attribute_change | `rename_class` | válido | sim | passed | passed |
| `suite_busca_blue_jeans` | `mutation-62c12f9ceba25067` | implementation_attribute_change | `rename_class` | válido | sim | failed | passed |

## Cenários elegíveis

- `suite_busca_blue_jeans`

## Limite

Os valores descrevem somente os operadores e elementos do plano utilizado nesta execução. Mudanças do contrato visível ou acessível não devem ser interpretadas como o mesmo fenômeno de mudanças internas neutras. Cenários diferentes podem reutilizar o mesmo componente da interface; nesses casos, os pares não são evidências independentes da quantidade de componentes alterados.
