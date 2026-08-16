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
| Resultado da execução | falhou: 10; erro de sintaxe: 4 |
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
| Estado da execução | falhou |
| Duração | 3.602 s |
| Tipo de erro | selector_ambiguity |
| Mensagem | Error: expect(locator).toBeVisible() failed Locator: locator('a').filter({ hasText: 'Digital downloads' }) Expected: visible Error: strict mode violation: locator('a').filter({ hasText: 'Digital downloads' }) resolved to 3 elements: 1) <a href="/digital-downloads">Digital downloads↵ </a> aka getByRole('link', { name: 'Digital downloads' }).first() 2) <a href="/digital-downloads">Digital downloads↵ </a> aka getByText('Digital downloads').nth(1) 3) <a href="/digital-downloads">Digital downloads↵… |

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
| Estado da execução | erro de sintaxe |
| Duração | 3.333 s |
| Tipo de erro | syntax_error |
| Mensagem | Error: page.click: SyntaxError: Failed to execute 'querySelectorAll' on 'Document': 'role_name:Search' is not a valid selector. at query (<anonymous>:5448:41) at <anonymous>:5458:7 at SelectorEvaluatorImpl._cached (<anonymous>:5235:20) at SelectorEvaluatorImpl._queryCSS (<anonymous>:5445:17) at SelectorEvaluatorImpl._querySimple (<anonymous>:5325:19) at <anonymous>:5273:29 at SelectorEvaluatorImpl._cached (<anonymous>:5235:20) at SelectorEvaluatorImpl.query (<anonymous>:5266:19) at Object.query… |

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
| Estado da execução | erro de sintaxe |
| Duração | 3.758 s |
| Tipo de erro | syntax_error |
| Mensagem | Error: page.click: SyntaxError: Failed to execute 'querySelectorAll' on 'Document': 'role_name:Search' is not a valid selector. at query (<anonymous>:5448:41) at <anonymous>:5458:7 at SelectorEvaluatorImpl._cached (<anonymous>:5235:20) at SelectorEvaluatorImpl._queryCSS (<anonymous>:5445:17) at SelectorEvaluatorImpl._querySimple (<anonymous>:5325:19) at <anonymous>:5273:29 at SelectorEvaluatorImpl._cached (<anonymous>:5235:20) at SelectorEvaluatorImpl.query (<anonymous>:5266:19) at Object.query… |

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
| Estado da execução | falhou |
| Duração | 13.273 s |
| Tipo de erro | locator_timeout |
| Mensagem | TimeoutError: locator.click: Timeout 10000ms exceeded. Call log: - waiting for locator('role=Search') 9 \| await searchInput.fill('Blue Jeans'); 10 \| const searchButton = page.locator('role=Search'); > 11 \| await searchButton.click(); \| ^ 12 \| 13 \| // Verifica se a URL contém o termo de pesquisa 14 \| await expect(page).toHaveURL(/blue-jeans/); at /home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/structured_context/suite_busca_blue_jeans.spec.ts:11:24 |

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
| Estado da execução | erro de sintaxe |
| Duração | 3.503 s |
| Tipo de erro | syntax_error |
| Mensagem | Error: page.click: SyntaxError: Failed to execute 'querySelectorAll' on 'Document': 'role_name:Search' is not a valid selector. at query (<anonymous>:5448:41) at <anonymous>:5458:7 at SelectorEvaluatorImpl._cached (<anonymous>:5235:20) at SelectorEvaluatorImpl._queryCSS (<anonymous>:5445:17) at SelectorEvaluatorImpl._querySimple (<anonymous>:5325:19) at <anonymous>:5273:29 at SelectorEvaluatorImpl._cached (<anonymous>:5235:20) at SelectorEvaluatorImpl.query (<anonymous>:5266:19) at Object.query… |

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
| Estado da execução | falhou |
| Duração | 15.880 s |
| Tipo de erro | locator_timeout |
| Mensagem | TimeoutError: page.selectOption: Timeout 10000ms exceeded. Call log: - waiting for locator('#product_attribute_1') 17 \| 18 \| // Etapa 3 > 19 \| await page.selectOption('#product_attribute_1', 'Fast'); \| ^ 20 \| await page.fill('#product_attribute_2', '4'); 21 \| await page.selectOption('#product_attribute_3', '400 GB'); 22 \| await page.click('text=Office Suite'); at /home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/structured_context/suite_configurar_… |

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
| Estado da execução | falhou |
| Duração | 13.753 s |
| Tipo de erro | locator_timeout |
| Mensagem | TimeoutError: locator.click: Timeout 10000ms exceeded. Call log: - waiting for locator('role=Search') 9 \| await searchInput.fill('Fiction'); 10 \| const searchButton = page.locator('role=Search'); > 11 \| await searchButton.click(); \| ^ 12 \| 13 \| // Verifica se a URL contém '/fiction' 14 \| await expect(page).toHaveURL(/\/fiction/); at /home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/structured_context/suite_detalhes_fiction.spec.ts:11:24 |

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
| Estado da execução | falhou |
| Duração | 14.746 s |
| Tipo de erro | locator_timeout |
| Mensagem | TimeoutError: page.click: Timeout 10000ms exceeded. Call log: - waiting for locator('input[name="removefromcart_36"]') 13 \| 14 \| // Etapa 3: Marcar Blue Jeans para remoção > 15 \| await page.click('input[name="removefromcart_36"]'); \| ^ 16 \| 17 \| // Etapa 4: Selecionar Atualizar carrinho 18 \| await page.click('button[name="updatecart"]'); at /home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/structured_context/suite_limpar_carrinho.spec.ts:15:16 |

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
| Estado da execução | falhou |
| Duração | 13.699 s |
| Tipo de erro | locator_timeout |
| Mensagem | TimeoutError: locator.click: Timeout 10000ms exceeded. Call log: - waiting for locator('.product-item-name').filter({ hasText: 'Camera' }) 14 \| // Etapa 4: Marca o produto Camera para remoção 15 \| const cameraProduct = page.locator('.product-item-name', { hasText: 'Camera' }); > 16 \| await cameraProduct.click(); \| ^ 17 \| await expect(cameraProduct).toBeVisible(); 18 \| 19 \| // Etapa 5: Seleciona Atualizar Wishlist at /home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantic… |

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
| Estado da execução | falhou |
| Duração | 11.312 s |
| Tipo de erro | assertion_failure |
| Mensagem | Error: expect(locator).toContainText(expected) failed Locator: locator('#message-error') Expected substring: "Login was unsuccessful. Please correct the errors and try again." Timeout: 7000ms Error: element(s) not found Call log: - Expect "toContainText" with timeout 7000ms - waiting for locator('#message-error') 24 \| expect(page).toHaveURL('https://demowebshop.tricentis.com/login'); 25 \| const errorMessage = page.locator('#message-error'); > 26 \| await expect(errorMessage).toContainText('Login… |

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
| Estado da execução | falhou |
| Duração | 11.800 s |
| Tipo de erro | assertion_failure |
| Mensagem | Error: expect(page).toHaveURL(expected) failed Expected: "https://demowebshop.tricentis.com/Account/Manage" Received: "https://demowebshop.tricentis.com/" Timeout: 7000ms Call log: - Expect "toHaveURL" with timeout 7000ms 17 × unexpected value "https://demowebshop.tricentis.com/" 22 \| 23 \| // Verificar que a página foi redirecionada para a conta do usuário > 24 \| expect(page).toHaveURL('https://demowebshop.tricentis.com/Account/Manage'); \| ^ 25 \| 26 \| // Verificar que os links de conta e logout… |

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
| Estado da execução | falhou |
| Duração | 13.455 s |
| Tipo de erro | locator_timeout |
| Mensagem | TimeoutError: locator.fill: Timeout 10000ms exceeded. Call log: - waiting for locator('#Email') 12 \| const loginButton = page.locator('#login-button'); 13 \| > 14 \| await emailInput.fill('valid-email@example.com'); \| ^ 15 \| await passwordInput.fill('valid-password'); 16 \| await loginButton.click(); 17 \| at /home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/structured_context/suite_logout.spec.ts:14:22 |

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
| Estado da execução | erro de sintaxe |
| Duração | 3.487 s |
| Tipo de erro | syntax_error |
| Mensagem | Error: page.click: SyntaxError: Failed to execute 'querySelectorAll' on 'Document': 'text:Register' is not a valid selector. at query (<anonymous>:5448:41) at <anonymous>:5458:7 at SelectorEvaluatorImpl._cached (<anonymous>:5235:20) at SelectorEvaluatorImpl._queryCSS (<anonymous>:5445:17) at SelectorEvaluatorImpl._querySimple (<anonymous>:5325:19) at <anonymous>:5273:29 at SelectorEvaluatorImpl._cached (<anonymous>:5235:20) at SelectorEvaluatorImpl.query (<anonymous>:5266:19) at Object.query (<… |

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
| Estado da execução | falhou |
| Duração | 3.167 s |
| Tipo de erro | assertion_failure |
| Mensagem | Error: page.click: Unknown engine "tag" while parsing selector tag=a, text=Register, href=/register Call log: - waiting for locator('tag=a, text=Register, href=/register') 6 \| 7 \| // Step 2: Click on the Register link > 8 \| await page.click('tag=a, text=Register, href=/register'); \| ^ 9 \| expect(page).toHaveURL('https://demowebshop.tricentis.com/register'); 10 \| 11 \| // Step 4: Fill in the email field at /home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_… |

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
