# Relatório auxiliar de avaliação dos testes E2E

> Este relatório é uma ferramenta não oficial de apoio à análise. As métricas automáticas são evidências; não constituem, isoladamente, uma avaliação de correção semântica.

## Visão geral

| Indicador | Resultado |
| --- | --- |
| Testes analisados | 14 |
| Com estrutura mínima reconhecida | 14 de 14 (100,0%) |
| Com pelo menos uma asserção | 14 de 14 (100,0%) |
| Com espera fixa `waitForTimeout` | 0 de 14 (0,0%) |
| Risco dos seletores | baixo: 0; médio: 13; alto: 0; não aplicável: 1 |
| Resultado da execução | não executado: 14 |
| Tamanho médio da entrada da LLM | 3664 caracteres; 51,5 linhas |
| Cobertura média de URLs no grafo | 100,0% |
| Cobertura média de textos no grafo | 85,1% |

## Como interpretar

- **Estrutura mínima** verifica apenas a presença de importação do Playwright, bloco de teste e asserção.
- **Risco dos seletores** é uma heurística: seletores semânticos reduzem o risco; XPath e esperas fixas elevam o risco.
- **Cobertura pelo grafo** indica se URLs e textos de locators foram encontrados nas evidências coletadas. Uma ausência é um ponto para revisão, não prova de erro.
- **Rubrica humana** deve receber notas de 0 (não atende), 1 (atende parcialmente) ou 2 (atende completamente).

## 1. fluxo_computadores_desktops

| Identificação | Valor |
| --- | --- |
| Abordagem | structured_context |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/structured_context/fluxo_computadores_desktops.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_prompts/fluxo_computadores_desktops.structured_context.prompt.md` |

### Leitura rápida

- ✅ Estrutura mínima do Playwright reconhecida.
- ✅ O teste contém asserção.
- ✅ Não usa espera fixa.
- **Risco estimado dos seletores:** médio.
- **URLs fundamentadas no grafo:** 100,0%.
- **Textos de locators fundamentados no grafo:** 66,7%.

### Estrutura e seletores

| Métrica | Resultado | Leitura |
| --- | --- | --- |
| Importa `@playwright/test` | sim | necessário para execução |
| Possui bloco `test(...)` | sim | estrutura do caso de teste |
| Possui `expect(...)` | sim | indício de verificação do resultado |
| Ações de usuário | 1 | cliques, preenchimentos e ações similares |
| Locators | 2 | total identificado estaticamente |
| Locators semânticos | 0 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demowebshop.tricentis.com/`

**Textos extraídos dos locators:**

- `, { hasText:`
- `h1`
- `Digital downloads`

### Pontos para revisão contra o grafo

**URLs não encontradas:**

- _nenhuma_

**Textos de locators não encontrados:**

- `, { hasText:`

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 2765 caracteres; 32 linhas |
| Estado da execução | não executado |
| Duração | não disponível |
| Tipo de erro | não informado |
| Mensagem | não informada |

### Rubrica para avaliação humana

| Critério | Pergunta orientadora | Nota (0–2) |
| --- | --- | --- |
| Fluxo correto | Executa os passos principais pedidos? | — |
| Alvo correto | Interage com os elementos esperados? | — |
| Asserção correta | Valida o resultado especificado? | — |
| Aderência ao grafo | Usa evidências disponíveis no contexto? | — |
| Robustez prática | Seletores e esperas são aceitáveis? | — |
| Utilidade geral | Exige pouca ou nenhuma correção manual? | — |

**Classificação da falha:** não preenchida

**Observações:** _preencher durante a análise_

---

## 2. suite_adicionar_carrinho

| Identificação | Valor |
| --- | --- |
| Abordagem | structured_context |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/structured_context/suite_adicionar_carrinho.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_prompts/suite_adicionar_carrinho.structured_context.prompt.md` |

### Leitura rápida

- ✅ Estrutura mínima do Playwright reconhecida.
- ✅ O teste contém asserção.
- ✅ Não usa espera fixa.
- **Risco estimado dos seletores:** médio.
- **URLs fundamentadas no grafo:** 100,0%.
- **Textos de locators fundamentados no grafo:** 100,0%.

### Estrutura e seletores

| Métrica | Resultado | Leitura |
| --- | --- | --- |
| Importa `@playwright/test` | sim | necessário para execução |
| Possui bloco `test(...)` | sim | estrutura do caso de teste |
| Possui `expect(...)` | sim | indício de verificação do resultado |
| Ações de usuário | 4 | cliques, preenchimentos e ações similares |
| Locators | 4 | total identificado estaticamente |
| Locators semânticos | 1 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demowebshop.tricentis.com/`

**Textos extraídos dos locators:**

- `h1`
- `Blue Jeans`
- `Shopping cart`
- `td.item`

### Pontos para revisão contra o grafo

**URLs não encontradas:**

- _nenhuma_

**Textos de locators não encontrados:**

- _nenhum_

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 3751 caracteres; 54 linhas |
| Estado da execução | não executado |
| Duração | não disponível |
| Tipo de erro | não informado |
| Mensagem | não informada |

### Rubrica para avaliação humana

| Critério | Pergunta orientadora | Nota (0–2) |
| --- | --- | --- |
| Fluxo correto | Executa os passos principais pedidos? | — |
| Alvo correto | Interage com os elementos esperados? | — |
| Asserção correta | Valida o resultado especificado? | — |
| Aderência ao grafo | Usa evidências disponíveis no contexto? | — |
| Robustez prática | Seletores e esperas são aceitáveis? | — |
| Utilidade geral | Exige pouca ou nenhuma correção manual? | — |

**Classificação da falha:** não preenchida

**Observações:** _preencher durante a análise_

---

## 3. suite_adicionar_wishlist

| Identificação | Valor |
| --- | --- |
| Abordagem | structured_context |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/structured_context/suite_adicionar_wishlist.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_prompts/suite_adicionar_wishlist.structured_context.prompt.md` |

### Leitura rápida

- ✅ Estrutura mínima do Playwright reconhecida.
- ✅ O teste contém asserção.
- ✅ Não usa espera fixa.
- **Risco estimado dos seletores:** médio.
- **URLs fundamentadas no grafo:** 100,0%.
- **Textos de locators fundamentados no grafo:** 100,0%.

### Estrutura e seletores

| Métrica | Resultado | Leitura |
| --- | --- | --- |
| Importa `@playwright/test` | sim | necessário para execução |
| Possui bloco `test(...)` | sim | estrutura do caso de teste |
| Possui `expect(...)` | sim | indício de verificação do resultado |
| Ações de usuário | 4 | cliques, preenchimentos e ações similares |
| Locators | 4 | total identificado estaticamente |
| Locators semânticos | 1 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demowebshop.tricentis.com/`

**Textos extraídos dos locators:**

- `h1`
- `Digital SLR Camera 12.2 Mpixel`
- `Wishlist`
- `li.product-item`

### Pontos para revisão contra o grafo

**URLs não encontradas:**

- _nenhuma_

**Textos de locators não encontrados:**

- _nenhum_

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 3884 caracteres; 55 linhas |
| Estado da execução | não executado |
| Duração | não disponível |
| Tipo de erro | não informado |
| Mensagem | não informada |

### Rubrica para avaliação humana

| Critério | Pergunta orientadora | Nota (0–2) |
| --- | --- | --- |
| Fluxo correto | Executa os passos principais pedidos? | — |
| Alvo correto | Interage com os elementos esperados? | — |
| Asserção correta | Valida o resultado especificado? | — |
| Aderência ao grafo | Usa evidências disponíveis no contexto? | — |
| Robustez prática | Seletores e esperas são aceitáveis? | — |
| Utilidade geral | Exige pouca ou nenhuma correção manual? | — |

**Classificação da falha:** não preenchida

**Observações:** _preencher durante a análise_

---

## 4. suite_busca_blue_jeans

| Identificação | Valor |
| --- | --- |
| Abordagem | structured_context |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/structured_context/suite_busca_blue_jeans.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_prompts/suite_busca_blue_jeans.structured_context.prompt.md` |

### Leitura rápida

- ✅ Estrutura mínima do Playwright reconhecida.
- ✅ O teste contém asserção.
- ✅ Não usa espera fixa.
- **Risco estimado dos seletores:** médio.
- **URLs fundamentadas no grafo:** 100,0%.
- **Textos de locators fundamentados no grafo:** 50,0%.

### Estrutura e seletores

| Métrica | Resultado | Leitura |
| --- | --- | --- |
| Importa `@playwright/test` | sim | necessário para execução |
| Possui bloco `test(...)` | sim | estrutura do caso de teste |
| Possui `expect(...)` | sim | indício de verificação do resultado |
| Ações de usuário | 3 | cliques, preenchimentos e ações similares |
| Locators | 4 | total identificado estaticamente |
| Locators semânticos | 0 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demowebshop.tricentis.com/`

**Textos extraídos dos locators:**

- `role=Search`
- `, { hasText:`
- `h1`
- `Blue Jeans`

### Pontos para revisão contra o grafo

**URLs não encontradas:**

- _nenhuma_

**Textos de locators não encontrados:**

- `role=Search`
- `, { hasText:`

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 3159 caracteres; 42 linhas |
| Estado da execução | não executado |
| Duração | não disponível |
| Tipo de erro | não informado |
| Mensagem | não informada |

### Rubrica para avaliação humana

| Critério | Pergunta orientadora | Nota (0–2) |
| --- | --- | --- |
| Fluxo correto | Executa os passos principais pedidos? | — |
| Alvo correto | Interage com os elementos esperados? | — |
| Asserção correta | Valida o resultado especificado? | — |
| Aderência ao grafo | Usa evidências disponíveis no contexto? | — |
| Robustez prática | Seletores e esperas são aceitáveis? | — |
| Utilidade geral | Exige pouca ou nenhuma correção manual? | — |

**Classificação da falha:** não preenchida

**Observações:** _preencher durante a análise_

---

## 5. suite_checkout_blue_jeans

| Identificação | Valor |
| --- | --- |
| Abordagem | structured_context |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/structured_context/suite_checkout_blue_jeans.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_prompts/suite_checkout_blue_jeans.structured_context.prompt.md` |

### Leitura rápida

- ✅ Estrutura mínima do Playwright reconhecida.
- ✅ O teste contém asserção.
- ✅ Não usa espera fixa.
- **Risco estimado dos seletores:** médio.
- **URLs fundamentadas no grafo:** 100,0%.
- **Textos de locators fundamentados no grafo:** 75,0%.

### Estrutura e seletores

| Métrica | Resultado | Leitura |
| --- | --- | --- |
| Importa `@playwright/test` | sim | necessário para execução |
| Possui bloco `test(...)` | sim | estrutura do caso de teste |
| Possui `expect(...)` | sim | indício de verificação do resultado |
| Ações de usuário | 36 | cliques, preenchimentos e ações similares |
| Locators | 4 | total identificado estaticamente |
| Locators semânticos | 1 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demowebshop.tricentis.com/`

**Textos extraídos dos locators:**

- `h1`
- `Blue Jeans`
- `Shopping cart`
- `Your order has been successfully processed!`

### Pontos para revisão contra o grafo

**URLs não encontradas:**

- _nenhuma_

**Textos de locators não encontrados:**

- `Your order has been successfully processed!`

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 4192 caracteres; 59 linhas |
| Estado da execução | não executado |
| Duração | não disponível |
| Tipo de erro | não informado |
| Mensagem | não informada |

### Rubrica para avaliação humana

| Critério | Pergunta orientadora | Nota (0–2) |
| --- | --- | --- |
| Fluxo correto | Executa os passos principais pedidos? | — |
| Alvo correto | Interage com os elementos esperados? | — |
| Asserção correta | Valida o resultado especificado? | — |
| Aderência ao grafo | Usa evidências disponíveis no contexto? | — |
| Robustez prática | Seletores e esperas são aceitáveis? | — |
| Utilidade geral | Exige pouca ou nenhuma correção manual? | — |

**Classificação da falha:** não preenchida

**Observações:** _preencher durante a análise_

---

## 6. suite_configurar_desktop

| Identificação | Valor |
| --- | --- |
| Abordagem | structured_context |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/structured_context/suite_configurar_desktop.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_prompts/suite_configurar_desktop.structured_context.prompt.md` |

### Leitura rápida

- ✅ Estrutura mínima do Playwright reconhecida.
- ✅ O teste contém asserção.
- ✅ Não usa espera fixa.
- **Risco estimado dos seletores:** médio.
- **URLs fundamentadas no grafo:** 100,0%.
- **Textos de locators fundamentados no grafo:** 50,0%.

### Estrutura e seletores

| Métrica | Resultado | Leitura |
| --- | --- | --- |
| Importa `@playwright/test` | sim | necessário para execução |
| Possui bloco `test(...)` | sim | estrutura do caso de teste |
| Possui `expect(...)` | sim | indício de verificação do resultado |
| Ações de usuário | 9 | cliques, preenchimentos e ações similares |
| Locators | 5 | total identificado estaticamente |
| Locators semânticos | 1 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demowebshop.tricentis.com/`

**Textos extraídos dos locators:**

- `, { hasText:`
- `Shopping cart`

### Pontos para revisão contra o grafo

**URLs não encontradas:**

- _nenhuma_

**Textos de locators não encontrados:**

- `, { hasText:`

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 3601 caracteres; 52 linhas |
| Estado da execução | não executado |
| Duração | não disponível |
| Tipo de erro | não informado |
| Mensagem | não informada |

### Rubrica para avaliação humana

| Critério | Pergunta orientadora | Nota (0–2) |
| --- | --- | --- |
| Fluxo correto | Executa os passos principais pedidos? | — |
| Alvo correto | Interage com os elementos esperados? | — |
| Asserção correta | Valida o resultado especificado? | — |
| Aderência ao grafo | Usa evidências disponíveis no contexto? | — |
| Robustez prática | Seletores e esperas são aceitáveis? | — |
| Utilidade geral | Exige pouca ou nenhuma correção manual? | — |

**Classificação da falha:** não preenchida

**Observações:** _preencher durante a análise_

---

## 7. suite_detalhes_fiction

| Identificação | Valor |
| --- | --- |
| Abordagem | structured_context |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/structured_context/suite_detalhes_fiction.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_prompts/suite_detalhes_fiction.structured_context.prompt.md` |

### Leitura rápida

- ✅ Estrutura mínima do Playwright reconhecida.
- ✅ O teste contém asserção.
- ✅ Não usa espera fixa.
- **Risco estimado dos seletores:** médio.
- **URLs fundamentadas no grafo:** 100,0%.
- **Textos de locators fundamentados no grafo:** 50,0%.

### Estrutura e seletores

| Métrica | Resultado | Leitura |
| --- | --- | --- |
| Importa `@playwright/test` | sim | necessário para execução |
| Possui bloco `test(...)` | sim | estrutura do caso de teste |
| Possui `expect(...)` | sim | indício de verificação do resultado |
| Ações de usuário | 2 | cliques, preenchimentos e ações similares |
| Locators | 4 | total identificado estaticamente |
| Locators semânticos | 0 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demowebshop.tricentis.com/`

**Textos extraídos dos locators:**

- `role=Search`
- `h1`

### Pontos para revisão contra o grafo

**URLs não encontradas:**

- _nenhuma_

**Textos de locators não encontrados:**

- `role=Search`

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 3157 caracteres; 42 linhas |
| Estado da execução | não executado |
| Duração | não disponível |
| Tipo de erro | não informado |
| Mensagem | não informada |

### Rubrica para avaliação humana

| Critério | Pergunta orientadora | Nota (0–2) |
| --- | --- | --- |
| Fluxo correto | Executa os passos principais pedidos? | — |
| Alvo correto | Interage com os elementos esperados? | — |
| Asserção correta | Valida o resultado especificado? | — |
| Aderência ao grafo | Usa evidências disponíveis no contexto? | — |
| Robustez prática | Seletores e esperas são aceitáveis? | — |
| Utilidade geral | Exige pouca ou nenhuma correção manual? | — |

**Classificação da falha:** não preenchida

**Observações:** _preencher durante a análise_

---

## 8. suite_limpar_carrinho

| Identificação | Valor |
| --- | --- |
| Abordagem | structured_context |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/structured_context/suite_limpar_carrinho.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_prompts/suite_limpar_carrinho.structured_context.prompt.md` |

### Leitura rápida

- ✅ Estrutura mínima do Playwright reconhecida.
- ✅ O teste contém asserção.
- ✅ Não usa espera fixa.
- **Risco estimado dos seletores:** médio.
- **URLs fundamentadas no grafo:** 100,0%.
- **Textos de locators fundamentados no grafo:** 100,0%.

### Estrutura e seletores

| Métrica | Resultado | Leitura |
| --- | --- | --- |
| Importa `@playwright/test` | sim | necessário para execução |
| Possui bloco `test(...)` | sim | estrutura do caso de teste |
| Possui `expect(...)` | sim | indício de verificação do resultado |
| Ações de usuário | 4 | cliques, preenchimentos e ações similares |
| Locators | 4 | total identificado estaticamente |
| Locators semânticos | 1 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demowebshop.tricentis.com/blue-jeans`

**Textos extraídos dos locators:**

- `Shopping cart`
- `h1`

### Pontos para revisão contra o grafo

**URLs não encontradas:**

- _nenhuma_

**Textos de locators não encontrados:**

- _nenhum_

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 3139 caracteres; 42 linhas |
| Estado da execução | não executado |
| Duração | não disponível |
| Tipo de erro | não informado |
| Mensagem | não informada |

### Rubrica para avaliação humana

| Critério | Pergunta orientadora | Nota (0–2) |
| --- | --- | --- |
| Fluxo correto | Executa os passos principais pedidos? | — |
| Alvo correto | Interage com os elementos esperados? | — |
| Asserção correta | Valida o resultado especificado? | — |
| Aderência ao grafo | Usa evidências disponíveis no contexto? | — |
| Robustez prática | Seletores e esperas são aceitáveis? | — |
| Utilidade geral | Exige pouca ou nenhuma correção manual? | — |

**Classificação da falha:** não preenchida

**Observações:** _preencher durante a análise_

---

## 9. suite_limpar_wishlist

| Identificação | Valor |
| --- | --- |
| Abordagem | structured_context |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/structured_context/suite_limpar_wishlist.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_prompts/suite_limpar_wishlist.structured_context.prompt.md` |

### Leitura rápida

- ✅ Estrutura mínima do Playwright reconhecida.
- ✅ O teste contém asserção.
- ✅ Não usa espera fixa.
- **Risco estimado dos seletores:** médio.
- **URLs fundamentadas no grafo:** 100,0%.
- **Textos de locators fundamentados no grafo:** 100,0%.

### Estrutura e seletores

| Métrica | Resultado | Leitura |
| --- | --- | --- |
| Importa `@playwright/test` | sim | necessário para execução |
| Possui bloco `test(...)` | sim | estrutura do caso de teste |
| Possui `expect(...)` | sim | indício de verificação do resultado |
| Ações de usuário | 3 | cliques, preenchimentos e ações similares |
| Locators | 4 | total identificado estaticamente |
| Locators semânticos | 2 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demowebshop.tricentis.com/`

**Textos extraídos dos locators:**

- `Wishlist`
- `Camera`
- `Update wishlist`

### Pontos para revisão contra o grafo

**URLs não encontradas:**

- _nenhuma_

**Textos de locators não encontrados:**

- _nenhum_

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 2973 caracteres; 38 linhas |
| Estado da execução | não executado |
| Duração | não disponível |
| Tipo de erro | não informado |
| Mensagem | não informada |

### Rubrica para avaliação humana

| Critério | Pergunta orientadora | Nota (0–2) |
| --- | --- | --- |
| Fluxo correto | Executa os passos principais pedidos? | — |
| Alvo correto | Interage com os elementos esperados? | — |
| Asserção correta | Valida o resultado especificado? | — |
| Aderência ao grafo | Usa evidências disponíveis no contexto? | — |
| Robustez prática | Seletores e esperas são aceitáveis? | — |
| Utilidade geral | Exige pouca ou nenhuma correção manual? | — |

**Classificação da falha:** não preenchida

**Observações:** _preencher durante a análise_

---

## 10. suite_login_invalido

| Identificação | Valor |
| --- | --- |
| Abordagem | structured_context |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/structured_context/suite_login_invalido.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_prompts/suite_login_invalido.structured_context.prompt.md` |

### Leitura rápida

- ✅ Estrutura mínima do Playwright reconhecida.
- ✅ O teste contém asserção.
- ✅ Não usa espera fixa.
- **Risco estimado dos seletores:** médio.
- **URLs fundamentadas no grafo:** 100,0%.
- **Textos de locators fundamentados no grafo:** 100,0%.

### Estrutura e seletores

| Métrica | Resultado | Leitura |
| --- | --- | --- |
| Importa `@playwright/test` | sim | necessário para execução |
| Possui bloco `test(...)` | sim | estrutura do caso de teste |
| Possui `expect(...)` | sim | indício de verificação do resultado |
| Ações de usuário | 4 | cliques, preenchimentos e ações similares |
| Locators | 5 | total identificado estaticamente |
| Locators semânticos | 0 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demowebshop.tricentis.com/`

**Textos extraídos dos locators:**

- `text=Log in`
- `Log in`

### Pontos para revisão contra o grafo

**URLs não encontradas:**

- _nenhuma_

**Textos de locators não encontrados:**

- _nenhum_

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 3453 caracteres; 48 linhas |
| Estado da execução | não executado |
| Duração | não disponível |
| Tipo de erro | não informado |
| Mensagem | não informada |

### Rubrica para avaliação humana

| Critério | Pergunta orientadora | Nota (0–2) |
| --- | --- | --- |
| Fluxo correto | Executa os passos principais pedidos? | — |
| Alvo correto | Interage com os elementos esperados? | — |
| Asserção correta | Valida o resultado especificado? | — |
| Aderência ao grafo | Usa evidências disponíveis no contexto? | — |
| Robustez prática | Seletores e esperas são aceitáveis? | — |
| Utilidade geral | Exige pouca ou nenhuma correção manual? | — |

**Classificação da falha:** não preenchida

**Observações:** _preencher durante a análise_

---

## 11. suite_login_valido

| Identificação | Valor |
| --- | --- |
| Abordagem | structured_context |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/structured_context/suite_login_valido.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_prompts/suite_login_valido.structured_context.prompt.md` |

### Leitura rápida

- ✅ Estrutura mínima do Playwright reconhecida.
- ✅ O teste contém asserção.
- ✅ Não usa espera fixa.
- **Risco estimado dos seletores:** médio.
- **URLs fundamentadas no grafo:** 100,0%.
- **Textos de locators fundamentados no grafo:** 100,0%.

### Estrutura e seletores

| Métrica | Resultado | Leitura |
| --- | --- | --- |
| Importa `@playwright/test` | sim | necessário para execução |
| Possui bloco `test(...)` | sim | estrutura do caso de teste |
| Possui `expect(...)` | sim | indício de verificação do resultado |
| Ações de usuário | 4 | cliques, preenchimentos e ações similares |
| Locators | 6 | total identificado estaticamente |
| Locators semânticos | 0 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demowebshop.tricentis.com/`

**Textos extraídos dos locators:**

- `text=Log in`
- `Log in`
- `text=Welcome, Please Sign In!`
- `text=Log out`

### Pontos para revisão contra o grafo

**URLs não encontradas:**

- _nenhuma_

**Textos de locators não encontrados:**

- _nenhum_

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 3405 caracteres; 48 linhas |
| Estado da execução | não executado |
| Duração | não disponível |
| Tipo de erro | não informado |
| Mensagem | não informada |

### Rubrica para avaliação humana

| Critério | Pergunta orientadora | Nota (0–2) |
| --- | --- | --- |
| Fluxo correto | Executa os passos principais pedidos? | — |
| Alvo correto | Interage com os elementos esperados? | — |
| Asserção correta | Valida o resultado especificado? | — |
| Aderência ao grafo | Usa evidências disponíveis no contexto? | — |
| Robustez prática | Seletores e esperas são aceitáveis? | — |
| Utilidade geral | Exige pouca ou nenhuma correção manual? | — |

**Classificação da falha:** não preenchida

**Observações:** _preencher durante a análise_

---

## 12. suite_logout

| Identificação | Valor |
| --- | --- |
| Abordagem | structured_context |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/structured_context/suite_logout.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_prompts/suite_logout.structured_context.prompt.md` |

### Leitura rápida

- ✅ Estrutura mínima do Playwright reconhecida.
- ✅ O teste contém asserção.
- ✅ Não usa espera fixa.
- **Risco estimado dos seletores:** médio.
- **URLs fundamentadas no grafo:** 100,0%.
- **Textos de locators fundamentados no grafo:** 100,0%.

### Estrutura e seletores

| Métrica | Resultado | Leitura |
| --- | --- | --- |
| Importa `@playwright/test` | sim | necessário para execução |
| Possui bloco `test(...)` | sim | estrutura do caso de teste |
| Possui `expect(...)` | sim | indício de verificação do resultado |
| Ações de usuário | 4 | cliques, preenchimentos e ações similares |
| Locators | 5 | total identificado estaticamente |
| Locators semânticos | 0 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demowebshop.tricentis.com/`

**Textos extraídos dos locators:**

- _nenhum texto de locator identificado_

### Pontos para revisão contra o grafo

**URLs não encontradas:**

- _nenhuma_

**Textos de locators não encontrados:**

- _nenhum_

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 2595 caracteres; 28 linhas |
| Estado da execução | não executado |
| Duração | não disponível |
| Tipo de erro | não informado |
| Mensagem | não informada |

### Rubrica para avaliação humana

| Critério | Pergunta orientadora | Nota (0–2) |
| --- | --- | --- |
| Fluxo correto | Executa os passos principais pedidos? | — |
| Alvo correto | Interage com os elementos esperados? | — |
| Asserção correta | Valida o resultado especificado? | — |
| Aderência ao grafo | Usa evidências disponíveis no contexto? | — |
| Robustez prática | Seletores e esperas são aceitáveis? | — |
| Utilidade geral | Exige pouca ou nenhuma correção manual? | — |

**Classificação da falha:** não preenchida

**Observações:** _preencher durante a análise_

---

## 13. suite_registro_usuario

| Identificação | Valor |
| --- | --- |
| Abordagem | structured_context |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/structured_context/suite_registro_usuario.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_prompts/suite_registro_usuario.structured_context.prompt.md` |

### Leitura rápida

- ✅ Estrutura mínima do Playwright reconhecida.
- ✅ O teste contém asserção.
- ✅ Não usa espera fixa.
- **Risco estimado dos seletores:** não aplicável.
- **URLs fundamentadas no grafo:** 100,0%.
- **Textos de locators fundamentados no grafo:** 100,0%.

### Estrutura e seletores

| Métrica | Resultado | Leitura |
| --- | --- | --- |
| Importa `@playwright/test` | sim | necessário para execução |
| Possui bloco `test(...)` | sim | estrutura do caso de teste |
| Possui `expect(...)` | sim | indício de verificação do resultado |
| Ações de usuário | 7 | cliques, preenchimentos e ações similares |
| Locators | 0 | total identificado estaticamente |
| Locators semânticos | 0 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demowebshop.tricentis.com/`

**Textos extraídos dos locators:**

- _nenhum texto de locator identificado_

### Pontos para revisão contra o grafo

**URLs não encontradas:**

- _nenhuma_

**Textos de locators não encontrados:**

- _nenhum_

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 4447 caracteres; 66 linhas |
| Estado da execução | não executado |
| Duração | não disponível |
| Tipo de erro | não informado |
| Mensagem | não informada |

### Rubrica para avaliação humana

| Critério | Pergunta orientadora | Nota (0–2) |
| --- | --- | --- |
| Fluxo correto | Executa os passos principais pedidos? | — |
| Alvo correto | Interage com os elementos esperados? | — |
| Asserção correta | Valida o resultado especificado? | — |
| Aderência ao grafo | Usa evidências disponíveis no contexto? | — |
| Robustez prática | Seletores e esperas são aceitáveis? | — |
| Utilidade geral | Exige pouca ou nenhuma correção manual? | — |

**Classificação da falha:** não preenchida

**Observações:** _preencher durante a análise_

---

## 14. user_registration_book_purchase

| Identificação | Valor |
| --- | --- |
| Abordagem | structured_context |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/structured_context/user_registration_book_purchase.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_prompts/user_registration_book_purchase.structured_context.prompt.md` |

### Leitura rápida

- ✅ Estrutura mínima do Playwright reconhecida.
- ✅ O teste contém asserção.
- ✅ Não usa espera fixa.
- **Risco estimado dos seletores:** médio.
- **URLs fundamentadas no grafo:** 100,0%.
- **Textos de locators fundamentados no grafo:** 100,0%.

### Estrutura e seletores

| Métrica | Resultado | Leitura |
| --- | --- | --- |
| Importa `@playwright/test` | sim | necessário para execução |
| Possui bloco `test(...)` | sim | estrutura do caso de teste |
| Possui `expect(...)` | sim | indício de verificação do resultado |
| Ações de usuário | 11 | cliques, preenchimentos e ações similares |
| Locators | 3 | total identificado estaticamente |
| Locators semânticos | 1 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demowebshop.tricentis.com/`

**Textos extraídos dos locators:**

- `The product has been added to your shopping cart`
- `Shopping cart`
- `Health Book`

### Pontos para revisão contra o grafo

**URLs não encontradas:**

- _nenhuma_

**Textos de locators não encontrados:**

- _nenhum_

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 6774 caracteres; 115 linhas |
| Estado da execução | não executado |
| Duração | não disponível |
| Tipo de erro | não informado |
| Mensagem | não informada |

### Rubrica para avaliação humana

| Critério | Pergunta orientadora | Nota (0–2) |
| --- | --- | --- |
| Fluxo correto | Executa os passos principais pedidos? | — |
| Alvo correto | Interage com os elementos esperados? | — |
| Asserção correta | Valida o resultado especificado? | — |
| Aderência ao grafo | Usa evidências disponíveis no contexto? | — |
| Robustez prática | Seletores e esperas são aceitáveis? | — |
| Utilidade geral | Exige pouca ou nenhuma correção manual? | — |

**Classificação da falha:** não preenchida

**Observações:** _preencher durante a análise_

---
