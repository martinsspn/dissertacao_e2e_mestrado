# Relatório auxiliar de avaliação dos testes E2E

> Este relatório é uma ferramenta não oficial de apoio à análise. As métricas automáticas são evidências; não constituem, isoladamente, uma avaliação de correção semântica.

## Visão geral

| Indicador | Resultado |
| --- | --- |
| Testes analisados | 14 |
| Com estrutura mínima reconhecida | 14 de 14 (100,0%) |
| Com pelo menos uma asserção | 14 de 14 (100,0%) |
| Com espera fixa `waitForTimeout` | 0 de 14 (0,0%) |
| Risco dos seletores | baixo: 7; médio: 7; alto: 0; não aplicável: 0 |
| Resultado da execução | passou: 2; falhou: 12 |
| Tamanho médio da entrada da LLM | 4486 caracteres; 54,5 linhas |
| Cobertura média de URLs no grafo | 100,0% |
| Cobertura média de textos no grafo | 90,8% |

## Como interpretar

- **Estrutura mínima** verifica apenas a presença de importação do Playwright, bloco de teste e asserção.
- **Risco dos seletores** é uma heurística: seletores semânticos reduzem o risco; XPath e esperas fixas elevam o risco.
- **Cobertura pelo grafo** indica se URLs e textos de locators foram encontrados nas evidências coletadas. Uma ausência é um ponto para revisão, não prova de erro.
- **Rubrica humana** deve receber notas de 0 (não atende), 1 (atende parcialmente) ou 2 (atende completamente).

## 1. fluxo_computadores_desktops

| Identificação | Valor |
| --- | --- |
| Abordagem | structured_context |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/structured_context_playwright_locators_20260724_02/fluxo_computadores_desktops.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_prompts_playwright_locators_20260724_02/fluxo_computadores_desktops.structured_context.prompt.md` |

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
| Ações de usuário | 1 | cliques, preenchimentos e ações similares |
| Locators | 2 | total identificado estaticamente |
| Locators semânticos | 1 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demowebshop.tricentis.com/`

**Textos extraídos dos locators:**

- `Digital downloads`
- `h1`

### Pontos para revisão contra o grafo

**URLs não encontradas:**

- _nenhuma_

**Textos de locators não encontrados:**

- _nenhum_

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 3504 caracteres; 35 linhas |
| Estado da execução | passou |
| Duração | 4.050 s |
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
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/structured_context_playwright_locators_20260724_02/suite_adicionar_carrinho.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_prompts_playwright_locators_20260724_02/suite_adicionar_carrinho.structured_context.prompt.md` |

### Leitura rápida

- ✅ Estrutura mínima do Playwright reconhecida.
- ✅ O teste contém asserção.
- ✅ Não usa espera fixa.
- **Risco estimado dos seletores:** baixo.
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
| Locators semânticos | 4 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demowebshop.tricentis.com/`

**Textos extraídos dos locators:**

- `Blue Jeans`
- `Search`
- `The product has been added to your shopping cart`
- `Shopping cart`

### Pontos para revisão contra o grafo

**URLs não encontradas:**

- _nenhuma_

**Textos de locators não encontrados:**

- _nenhum_

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 4570 caracteres; 57 linhas |
| Estado da execução | falhou |
| Duração | 11.127 s |
| Tipo de erro | assertion_failure |
| Mensagem | Error: expect(page).toHaveURL(expected) failed Expected: "https://demowebshop.tricentis.com/blue-jeans" Received: "https://demowebshop.tricentis.com/search?q=Blue+Jeans" Timeout: 7000ms Call log: - Expect "toHaveURL" with timeout 7000ms 17 × unexpected value "https://demowebshop.tricentis.com/search?q=Blue+Jeans" 9 \| 10 \| // Etapa 2: Abre a página do produto Blue Jeans > 11 \| await expect(page).toHaveURL('https://demowebshop.tricentis.com/blue-jeans'); \| ^ 12 \| 13 \| // Etapa 3: Adiciona o produ… |

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
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/structured_context_playwright_locators_20260724_02/suite_adicionar_wishlist.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_prompts_playwright_locators_20260724_02/suite_adicionar_wishlist.structured_context.prompt.md` |

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
| Ações de usuário | 5 | cliques, preenchimentos e ações similares |
| Locators | 7 | total identificado estaticamente |
| Locators semânticos | 3 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demowebshop.tricentis.com/`

**Textos extraídos dos locators:**

- `Camera`
- `Search`
- `The product has been added to your wishlist.`
- `Wishlist`

### Pontos para revisão contra o grafo

**URLs não encontradas:**

- _nenhuma_

**Textos de locators não encontrados:**

- _nenhum_

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 4703 caracteres; 58 linhas |
| Estado da execução | falhou |
| Duração | 4.484 s |
| Tipo de erro | selector_ambiguity |
| Mensagem | Error: locator.click: Error: strict mode violation: locator('[href="/digital-slr-camera"]') resolved to 2 elements: 1) <a href="/digital-slr-camera" title="Show details for Digital SLR Camera 12.2 Mpixel">…</a> aka getByRole('link', { name: 'Picture of Digital SLR Camera' }) 2) <a href="/digital-slr-camera">Digital SLR Camera 12.2 Mpixel</a> aka getByRole('link', { name: 'Digital SLR Camera 12.2 Mpixel', exact: true }) Call log: - waiting for locator('[href="/digital-slr-camera"]') 12 \| // Etap… |

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
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/structured_context_playwright_locators_20260724_02/suite_busca_blue_jeans.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_prompts_playwright_locators_20260724_02/suite_busca_blue_jeans.structured_context.prompt.md` |

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
| Locators semânticos | 1 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demowebshop.tricentis.com/`

**Textos extraídos dos locators:**

- `Blue Jeans`
- `Search`

### Pontos para revisão contra o grafo

**URLs não encontradas:**

- _nenhuma_

**Textos de locators não encontrados:**

- _nenhum_

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 3934 caracteres; 45 linhas |
| Estado da execução | falhou |
| Duração | 11.083 s |
| Tipo de erro | assertion_failure |
| Mensagem | Error: expect(locator).toContainText(expected) failed Locator: locator('.product-list-item-name') Expected substring: "Blue Jeans" Timeout: 7000ms Error: element(s) not found Call log: - Expect "toContainText" with timeout 7000ms - waiting for locator('.product-list-item-name') 10 \| // Etapa 3: Verificar que os resultados da busca contêm Blue Jeans 11 \| const searchResults = page.locator('.product-list-item-name'); > 12 \| await expect(searchResults).toContainText('Blue Jeans'); \| ^ 13 \| 14 \| //… |

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
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/structured_context_playwright_locators_20260724_02/suite_checkout_blue_jeans.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_prompts_playwright_locators_20260724_02/suite_checkout_blue_jeans.structured_context.prompt.md` |

### Leitura rápida

- ✅ Estrutura mínima do Playwright reconhecida.
- ✅ O teste contém asserção.
- ✅ Não usa espera fixa.
- **Risco estimado dos seletores:** médio.
- **URLs fundamentadas no grafo:** 100,0%.
- **Textos de locators fundamentados no grafo:** 42,3%.

### Estrutura e seletores

| Métrica | Resultado | Leitura |
| --- | --- | --- |
| Importa `@playwright/test` | sim | necessário para execução |
| Possui bloco `test(...)` | sim | estrutura do caso de teste |
| Possui `expect(...)` | sim | indício de verificação do resultado |
| Ações de usuário | 31 | cliques, preenchimentos e ações similares |
| Locators | 34 | total identificado estaticamente |
| Locators semânticos | 8 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demowebshop.tricentis.com/`

**Textos extraídos dos locators:**

- `Blue Jeans`
- `Search`
- `Shopping cart`
- `h1`
- `I agree with the terms`
- `Checkout`
- `John`
- `Doe`
- `john.doe@example.com`
- `United States`
- `Alabama`
- `Montgomery`
- `123 Main St`
- `36104`
- `radio`
- `Next Day Air`
- `Credit Card (Visa, MasterCard)`
- `John Doe`
- `4111111111111111`
- `01`
- `2025`
- `123`
- `Continue`
- `Order review`
- `Confirm`
- `Your order has been successfully processed!`

### Pontos para revisão contra o grafo

**URLs não encontradas:**

- _nenhuma_

**Textos de locators não encontrados:**

- `Checkout`
- `John`
- `john.doe@example.com`
- `United States`
- `Alabama`
- `Montgomery`
- `123 Main St`
- `36104`
- `radio`
- `Credit Card (Visa, MasterCard)`
- `John Doe`
- `4111111111111111`
- `2025`
- `Continue`
- `Your order has been successfully processed!`

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 5011 caracteres; 62 linhas |
| Estado da execução | falhou |
| Duração | 11.413 s |
| Tipo de erro | assertion_failure |
| Mensagem | Error: expect(page).toHaveURL(expected) failed Expected: "https://demowebshop.tricentis.com/blue-jeans" Received: "https://demowebshop.tricentis.com/search?q=Blue+Jeans" Timeout: 7000ms Call log: - Expect "toHaveURL" with timeout 7000ms 17 × unexpected value "https://demowebshop.tricentis.com/search?q=Blue+Jeans" 7 \| await page.locator("[id=\"small-searchterms\"]").fill('Blue Jeans'); 8 \| await page.getByRole("button", { name: "Search", exact: true }).click(); > 9 \| await expect(page).toHaveURL… |

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
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/structured_context_playwright_locators_20260724_02/suite_configurar_desktop.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_prompts_playwright_locators_20260724_02/suite_configurar_desktop.structured_context.prompt.md` |

### Leitura rápida

- ✅ Estrutura mínima do Playwright reconhecida.
- ✅ O teste contém asserção.
- ✅ Não usa espera fixa.
- **Risco estimado dos seletores:** baixo.
- **URLs fundamentadas no grafo:** 100,0%.
- **Textos de locators fundamentados no grafo:** 90,0%.

### Estrutura e seletores

| Métrica | Resultado | Leitura |
| --- | --- | --- |
| Importa `@playwright/test` | sim | necessário para execução |
| Possui bloco `test(...)` | sim | estrutura do caso de teste |
| Possui `expect(...)` | sim | indício de verificação do resultado |
| Ações de usuário | 8 | cliques, preenchimentos e ações similares |
| Locators | 10 | total identificado estaticamente |
| Locators semânticos | 8 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demowebshop.tricentis.com/`

**Textos extraídos dos locators:**

- `Computers`
- `Desktops`
- `Fast`
- `4GB [+$25.00]`
- `400GB [+$10.00]`
- `Microsoft Office Suite [+$79.00]`
- `Add to cart`
- `The product has been added to your shopping cart`
- `Shopping cart`
- `Desktop`

### Pontos para revisão contra o grafo

**URLs não encontradas:**

- _nenhuma_

**Textos de locators não encontrados:**

- `400GB [+$10.00]`

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 4400 caracteres; 55 linhas |
| Estado da execução | falhou |
| Duração | 14.717 s |
| Tipo de erro | locator_timeout |
| Mensagem | TimeoutError: locator.click: Timeout 10000ms exceeded. Call log: - waiting for getByText('Fast', { exact: true }) 13 \| 14 \| // Step 3: Select options for Fast processor, 4 GB memory, 400 GB disk, and Office Suite software > 15 \| await page.getByText("Fast", { exact: true }).click(); \| ^ 16 \| await page.getByText("4GB [+$25.00]", { exact: true }).click(); 17 \| await page.getByText("400GB [+$10.00]", { exact: true }).click(); 18 \| await page.getByText("Microsoft Office Suite [+$79.00]", { exact:… |

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
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/structured_context_playwright_locators_20260724_02/suite_detalhes_fiction.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_prompts_playwright_locators_20260724_02/suite_detalhes_fiction.structured_context.prompt.md` |

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
| Ações de usuário | 2 | cliques, preenchimentos e ações similares |
| Locators | 4 | total identificado estaticamente |
| Locators semânticos | 1 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demowebshop.tricentis.com/`

**Textos extraídos dos locators:**

- `Search`
- `h1`
- `Fiction`
- `span.price`

### Pontos para revisão contra o grafo

**URLs não encontradas:**

- _nenhuma_

**Textos de locators não encontrados:**

- _nenhum_

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 3932 caracteres; 45 linhas |
| Estado da execução | falhou |
| Duração | 11.472 s |
| Tipo de erro | assertion_failure |
| Mensagem | Error: expect(page).toHaveURL(expected) failed Expected: "https://demowebshop.tricentis.com/fiction" Received: "https://demowebshop.tricentis.com/search?q=Fiction" Timeout: 7000ms Call log: - Expect "toHaveURL" with timeout 7000ms 17 × unexpected value "https://demowebshop.tricentis.com/search?q=Fiction" 12 \| 13 \| // Etapa 2: The user opens the product Fiction in the search results. > 14 \| await expect(page).toHaveURL('https://demowebshop.tricentis.com/fiction'); \| ^ 15 \| 16 \| // Etapa 3: The s… |

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
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/structured_context_playwright_locators_20260724_02/suite_limpar_carrinho.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_prompts_playwright_locators_20260724_02/suite_limpar_carrinho.structured_context.prompt.md` |

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
| Locators semânticos | 2 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demowebshop.tricentis.com/blue-jeans`

**Textos extraídos dos locators:**

- `Shopping cart`
- `Update shopping cart`

### Pontos para revisão contra o grafo

**URLs não encontradas:**

- _nenhuma_

**Textos de locators não encontrados:**

- _nenhum_

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 3873 caracteres; 45 linhas |
| Estado da execução | falhou |
| Duração | 14.160 s |
| Tipo de erro | locator_timeout |
| Mensagem | TimeoutError: locator.click: Timeout 10000ms exceeded. Call log: - waiting for locator('[name="removefromcart_1"]') 12 \| 13 \| // Etapa 3: Marcar Blue Jeans para remoção > 14 \| await page.locator("[name=\"removefromcart_1\"]").click(); \| ^ 15 \| 16 \| // Etapa 4: Selecionar Atualizar Carrinho 17 \| await page.getByRole("button", { name: "Update shopping cart" }).click(); at /home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/structured_context_playwright… |

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
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/structured_context_playwright_locators_20260724_02/suite_limpar_wishlist.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_prompts_playwright_locators_20260724_02/suite_limpar_wishlist.structured_context.prompt.md` |

### Leitura rápida

- ✅ Estrutura mínima do Playwright reconhecida.
- ✅ O teste contém asserção.
- ✅ Não usa espera fixa.
- **Risco estimado dos seletores:** baixo.
- **URLs fundamentadas no grafo:** 100,0%.
- **Textos de locators fundamentados no grafo:** 100,0%.

### Estrutura e seletores

| Métrica | Resultado | Leitura |
| --- | --- | --- |
| Importa `@playwright/test` | sim | necessário para execução |
| Possui bloco `test(...)` | sim | estrutura do caso de teste |
| Possui `expect(...)` | sim | indício de verificação do resultado |
| Ações de usuário | 3 | cliques, preenchimentos e ações similares |
| Locators | 5 | total identificado estaticamente |
| Locators semânticos | 4 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demowebshop.tricentis.com/`

**Textos extraídos dos locators:**

- `Wishlist`
- `Camera`
- `Remove from Wishlist`
- `Update Wishlist`
- `h1`

### Pontos para revisão contra o grafo

**URLs não encontradas:**

- _nenhuma_

**Textos de locators não encontrados:**

- _nenhum_

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 3674 caracteres; 41 linhas |
| Estado da execução | falhou |
| Duração | 13.905 s |
| Tipo de erro | locator_timeout |
| Mensagem | TimeoutError: locator.click: Timeout 10000ms exceeded. Call log: - waiting for getByText('Camera').getByRole('button', { name: 'Remove from Wishlist' }) 13 \| 14 \| // Step 4: The user marks the Camera product for removal > 15 \| await page.getByText('Camera').getByRole("button", { name: "Remove from Wishlist" }).click(); \| ^ 16 \| 17 \| // Step 5: The user selects Update wishlist 18 \| await page.getByRole("button", { name: "Update Wishlist" }).click(); at /home/martinsspn/dissertacao_e2e_semantico/… |

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
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/structured_context_playwright_locators_20260724_02/suite_login_invalido.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_prompts_playwright_locators_20260724_02/suite_login_invalido.structured_context.prompt.md` |

### Leitura rápida

- ✅ Estrutura mínima do Playwright reconhecida.
- ✅ O teste contém asserção.
- ✅ Não usa espera fixa.
- **Risco estimado dos seletores:** baixo.
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
| Locators semânticos | 5 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demowebshop.tricentis.com/`

**Textos extraídos dos locators:**

- `Log in`
- `Email:`
- `Password:`
- `Login was unsuccessful. Please correct the errors and try again.`

### Pontos para revisão contra o grafo

**URLs não encontradas:**

- _nenhuma_

**Textos de locators não encontrados:**

- _nenhum_

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 4326 caracteres; 51 linhas |
| Estado da execução | passou |
| Duração | 4.291 s |
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
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/structured_context_playwright_locators_20260724_02/suite_login_valido.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_prompts_playwright_locators_20260724_02/suite_login_valido.structured_context.prompt.md` |

### Leitura rápida

- ✅ Estrutura mínima do Playwright reconhecida.
- ✅ O teste contém asserção.
- ✅ Não usa espera fixa.
- **Risco estimado dos seletores:** baixo.
- **URLs fundamentadas no grafo:** 100,0%.
- **Textos de locators fundamentados no grafo:** 80,0%.

### Estrutura e seletores

| Métrica | Resultado | Leitura |
| --- | --- | --- |
| Importa `@playwright/test` | sim | necessário para execução |
| Possui bloco `test(...)` | sim | estrutura do caso de teste |
| Possui `expect(...)` | sim | indício de verificação do resultado |
| Ações de usuário | 4 | cliques, preenchimentos e ações similares |
| Locators | 4 | total identificado estaticamente |
| Locators semânticos | 4 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demowebshop.tricentis.com/`

**Textos extraídos dos locators:**

- `Log in`
- `Email:`
- `test@example.com`
- `Password:`
- `password123`

### Pontos para revisão contra o grafo

**URLs não encontradas:**

- _nenhuma_

**Textos de locators não encontrados:**

- `password123`

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 4278 caracteres; 51 linhas |
| Estado da execução | falhou |
| Duração | 4.104 s |
| Tipo de erro | assertion_failure |
| Mensagem | Error: expect(received).toBe(expected) // Object.is equality - Expected - 1 + Received + 3 - Welcome, Please Sign In! + + Categories + 7 \| await page.getByText("Log in", { exact: true }).first().click(); 8 \| expect(page).toHaveURL('https://demowebshop.tricentis.com/login'); > 9 \| expect(await page.textContent('.title')).toBe('Welcome, Please Sign In!'); \| ^ 10 \| 11 \| // Etapa 2: Preencher os campos de email e senha 12 \| await page.getByLabel("Email:", { exact: true }).fill(process.env.EMAIL \|\|… |

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
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/structured_context_playwright_locators_20260724_02/suite_logout.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_prompts_playwright_locators_20260724_02/suite_logout.structured_context.prompt.md` |

### Leitura rápida

- ✅ Estrutura mínima do Playwright reconhecida.
- ✅ O teste contém asserção.
- ✅ Não usa espera fixa.
- **Risco estimado dos seletores:** baixo.
- **URLs fundamentadas no grafo:** 100,0%.
- **Textos de locators fundamentados no grafo:** 83,3%.

### Estrutura e seletores

| Métrica | Resultado | Leitura |
| --- | --- | --- |
| Importa `@playwright/test` | sim | necessário para execução |
| Possui bloco `test(...)` | sim | estrutura do caso de teste |
| Possui `expect(...)` | sim | indício de verificação do resultado |
| Ações de usuário | 4 | cliques, preenchimentos e ações similares |
| Locators | 5 | total identificado estaticamente |
| Locators semânticos | 5 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demowebshop.tricentis.com/`

**Textos extraídos dos locators:**

- `Email:`
- `test@example.com`
- `Password:`
- `password`
- `Log in`
- `Logout`

### Pontos para revisão contra o grafo

**URLs não encontradas:**

- _nenhuma_

**Textos de locators não encontrados:**

- `Logout`

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 3285 caracteres; 31 linhas |
| Estado da execução | falhou |
| Duração | 13.377 s |
| Tipo de erro | locator_timeout |
| Mensagem | TimeoutError: locator.fill: Timeout 10000ms exceeded. Call log: - waiting for getByLabel('Email:', { exact: true }) 5 \| // Step 1: The user is authenticated with valid credentials provided by the testing environment. 6 \| await page.goto('https://demowebshop.tricentis.com/'); > 7 \| await page.getByLabel('Email:', { exact: true }).fill(process.env.TEST_EMAIL \|\| 'test@example.com'); \| ^ 8 \| await page.getByLabel('Password:', { exact: true }).fill(process.env.TEST_PASSWORD \|\| 'password'); 9 \| await… |

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
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/structured_context_playwright_locators_20260724_02/suite_registro_usuario.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_prompts_playwright_locators_20260724_02/suite_registro_usuario.structured_context.prompt.md` |

### Leitura rápida

- ✅ Estrutura mínima do Playwright reconhecida.
- ✅ O teste contém asserção.
- ✅ Não usa espera fixa.
- **Risco estimado dos seletores:** baixo.
- **URLs fundamentadas no grafo:** 100,0%.
- **Textos de locators fundamentados no grafo:** 88,9%.

### Estrutura e seletores

| Métrica | Resultado | Leitura |
| --- | --- | --- |
| Importa `@playwright/test` | sim | necessário para execução |
| Possui bloco `test(...)` | sim | estrutura do caso de teste |
| Possui `expect(...)` | sim | indício de verificação do resultado |
| Ações de usuário | 9 | cliques, preenchimentos e ações similares |
| Locators | 10 | total identificado estaticamente |
| Locators semânticos | 8 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demowebshop.tricentis.com/`

**Textos extraídos dos locators:**

- `Register`
- `Gender`
- `First name:`
- `Last name:`
- `Email:`
- `Password:`
- `Confirm password:`
- `Your registration completed`
- `Continue`

### Pontos para revisão contra o grafo

**URLs não encontradas:**

- _nenhuma_

**Textos de locators não encontrados:**

- `Continue`

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 5424 caracteres; 69 linhas |
| Estado da execução | falhou |
| Duração | 5.823 s |
| Tipo de erro | assertion_failure |
| Mensagem | Error: expect(page).toHaveURL(expected) failed Expected: "https://demowebshop.tricentis.com/" Received: "" Call log: - Expect "toHaveURL" with timeout 7000ms 35 \| // Etapa 8: Seleciona Continue e retorna à loja autenticada 36 \| await page.getByRole('button', { name: 'Continue' }).click(); > 37 \| expect(page).toHaveURL('https://demowebshop.tricentis.com/'); \| ^ 38 \| }); 39 \| }); 40 \| at /home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/structured_co… |

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
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/structured_context_playwright_locators_20260724_02/user_registration_book_purchase.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_prompts_playwright_locators_20260724_02/user_registration_book_purchase.structured_context.prompt.md` |

### Leitura rápida

- ✅ Estrutura mínima do Playwright reconhecida.
- ✅ O teste contém asserção.
- ✅ Não usa espera fixa.
- **Risco estimado dos seletores:** médio.
- **URLs fundamentadas no grafo:** 100,0%.
- **Textos de locators fundamentados no grafo:** 86,7%.

### Estrutura e seletores

| Métrica | Resultado | Leitura |
| --- | --- | --- |
| Importa `@playwright/test` | sim | necessário para execução |
| Possui bloco `test(...)` | sim | estrutura do caso de teste |
| Possui `expect(...)` | sim | indício de verificação do resultado |
| Ações de usuário | 11 | cliques, preenchimentos e ações similares |
| Locators | 17 | total identificado estaticamente |
| Locators semânticos | 9 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demowebshop.tricentis.com/`

**Textos extraídos dos locators:**

- `Register`
- `h1`
- `Email:`
- `test@example.com`
- `Password:`
- `P@ssw0rd!`
- `Confirm password:`
- `First name:`
- `John`
- `Last name:`
- `Doe`
- `Books`
- `Health Book`
- `The product has been added to your shopping cart`
- `Shopping cart`

### Pontos para revisão contra o grafo

**URLs não encontradas:**

- _nenhuma_

**Textos de locators não encontrados:**

- `P@ssw0rd!`
- `John`

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 7893 caracteres; 118 linhas |
| Estado da execução | falhou |
| Duração | 8.452 s |
| Tipo de erro | assertion_failure |
| Mensagem | Error: expect(page).toHaveURL(expected) failed Expected: "https://demowebshop.tricentis.com/cart" Received: "" Call log: - Expect "toHaveURL" with timeout 7000ms 47 \| // Step 19: Navigate to the shopping cart to check the added item 48 \| await page.getByRole("link", { name: "Shopping cart", exact: true }).click(); > 49 \| expect(page).toHaveURL('https://demowebshop.tricentis.com/cart'); \| ^ 50 \| expect(page.locator('h1')).toContainText('Shopping cart'); 51 \| 52 \| // Step 20: The system displays… |

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
