# Resultado da avaliação de resiliência

## Escopo

- Plano de mutações: `7e1ed1318e46271b4a055e9a475e38b85f31b6f22c4614d4033656450fcbbbfc`.
- Cenários elegíveis nas duas condições: 3.
- Repetições: 3.
- Mutações selecionadas: 6.
- Seleção reduzida: até 2 mutações neutras por cenário (uma E1 e uma E2 quando disponível; desempate por hash do plano).
- Mutantes inválidos pelo controle diferencial: 2.
- Mutantes não aplicáveis porque ambos os testes não interagiram com o alvo original: 2.
- Os resultados são apresentados por estrato; não há conclusão universal baseada em média única.

## Comparação pareada por estrato

| Estrato | Pares válidos | Ambos passam | Só baseline | Só estruturado | Ambos falham | McNemar exato |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| E1 | 1 | 1 | 0 | 0 | 0 | 1.0000 |
| E2 | 1 | 1 | 0 | 0 | 0 | 1.0000 |

## Resultado por mutação

Condição A: **baseline**. Condição B: **structured_context**.

| Cenário | Mutação | Estrato | Operador | Controle | Aplicável ao par | A | B |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `suite_cadastro_campos_obrigatorios` | `mutation-eba9a88e12218532` | E1 | `insert_wrapper` | válido | não | - | - |
| `suite_cadastro_campos_obrigatorios` | `mutation-f449b64a22b3eb79` | E2 | `rename_id` | válido | não | - | - |
| `suite_cadastro_confirmacao_senha` | `mutation-d8744bdb7fd5af84` | E1 | `insert_noninteractive_sibling_before` | válido | sim | passed_interacted, passed_interacted, passed_interacted | passed_interacted, passed_interacted, passed_interacted |
| `suite_cadastro_confirmacao_senha` | `mutation-d5cd8e90b29b1b31` | E2 | `rename_id` | válido | sim | passed_interacted, passed_interacted, passed_interacted | passed_interacted, passed_interacted, passed_interacted |
| `suite_navegar_categoria_livros` | `mutation-8abd56080bd4efa1` | E1 | `insert_noninteractive_sibling_before` | inválido | não | - | - |
| `suite_navegar_categoria_livros` | `mutation-e0bcb5d5196386aa` | E1 | `insert_wrapper` | inválido | não | - | - |

## Cenários elegíveis

- `suite_cadastro_campos_obrigatorios`
- `suite_cadastro_confirmacao_senha`
- `suite_navegar_categoria_livros`

## Limite

Os valores descrevem somente os operadores e elementos do plano utilizado nesta execução. Mudanças do contrato visível ou acessível não devem ser interpretadas como o mesmo fenômeno de mudanças internas neutras. Cenários diferentes podem reutilizar o mesmo componente da interface; nesses casos, os pares não são evidências independentes da quantidade de componentes alterados.
