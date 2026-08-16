# Relatório auxiliar de avaliação dos testes E2E

> Este relatório é uma ferramenta não oficial de apoio à análise. As métricas automáticas são evidências; não constituem, isoladamente, uma avaliação de correção semântica.

## Visão geral

| Indicador | Resultado |
| --- | --- |
| Testes analisados | 14 |
| Com estrutura mínima reconhecida | 14 de 14 (100,0%) |
| Com pelo menos uma asserção | 14 de 14 (100,0%) |
| Com espera fixa `waitForTimeout` | 0 de 14 (0,0%) |
| Risco dos seletores | baixo: 0; médio: 12; alto: 0; não aplicável: 2 |
| Resultado da execução | falhou: 14 |
| Tamanho médio da entrada da LLM | 386 caracteres; 1,0 linhas |
| Cobertura média de URLs no grafo | 60,7% |
| Cobertura média de textos no grafo | 91,1% |

## Como interpretar

- **Estrutura mínima** verifica apenas a presença de importação do Playwright, bloco de teste e asserção.
- **Risco dos seletores** é uma heurística: seletores semânticos reduzem o risco; XPath e esperas fixas elevam o risco.
- **Cobertura pelo grafo** indica se URLs e textos de locators foram encontrados nas evidências coletadas. Uma ausência é um ponto para revisão, não prova de erro.
- **Rubrica humana** deve receber notas de 0 (não atende), 1 (atende parcialmente) ou 2 (atende completamente).

## 1. fluxo_computadores_desktops

| Identificação | Valor |
| --- | --- |
| Abordagem | baseline |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline_playwright_locators_20260724_02/fluxo_computadores_desktops.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | não localizada/informada |

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
| Ações de usuário | 0 | cliques, preenchimentos e ações similares |
| Locators | 2 | total identificado estaticamente |
| Locators semânticos | 0 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `/digital-downloads`

**Textos extraídos dos locators:**

- `h1`

### Pontos para revisão contra o grafo

**URLs não encontradas:**

- _nenhuma_

**Textos de locators não encontrados:**

- _nenhum_

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | não disponível |
| Estado da execução | falhou |
| Duração | 10.132 s |
| Tipo de erro | assertion_failure |
| Mensagem | Error: expect(locator).toBeVisible() failed Locator: locator('.digital-item') Expected: visible Timeout: 7000ms Error: element(s) not found Call log: - Expect "toBeVisible" with timeout 7000ms - waiting for locator('.digital-item') 8 \| // Wait for the digital items to be visible 9 \| const digitalItems = page.locator('.digital-item'); > 10 \| await expect(digitalItems).toBeVisible(); \| ^ 11 \| 12 \| // Validate that the digital downloads page is visible 13 \| const pageTitle = page.locator('h1'); at… |

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
| Abordagem | baseline |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline_playwright_locators_20260724_02/suite_adicionar_carrinho.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/specs/suite_adicionar_carrinho.txt` |

### Leitura rápida

- ✅ Estrutura mínima do Playwright reconhecida.
- ✅ O teste contém asserção.
- ✅ Não usa espera fixa.
- **Risco estimado dos seletores:** médio.
- **URLs fundamentadas no grafo:** 0,0%.
- **Textos de locators fundamentados no grafo:** 75,0%.

### Estrutura e seletores

| Métrica | Resultado | Leitura |
| --- | --- | --- |
| Importa `@playwright/test` | sim | necessário para execução |
| Possui bloco `test(...)` | sim | estrutura do caso de teste |
| Possui `expect(...)` | sim | indício de verificação do resultado |
| Ações de usuário | 5 | cliques, preenchimentos e ações similares |
| Locators | 3 | total identificado estaticamente |
| Locators semânticos | 0 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://example.com`

**Textos extraídos dos locators:**

- `product-link`
- `Blue Jeans`
- `cart-confirmation`
- `cart-item`

### Pontos para revisão contra o grafo

**URLs não encontradas:**

- `https://example.com`

**Textos de locators não encontrados:**

- `cart-confirmation`

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 370 caracteres; 1 linhas |
| Estado da execução | falhou |
| Duração | 10.430 s |
| Tipo de erro | locator_timeout |
| Mensagem | TimeoutError: page.fill: Timeout 10000ms exceeded. Call log: - waiting for locator('[data-test="search-input"]') 5 \| // Step 1: Search for the product "Blue Jeans" 6 \| await page.goto('https://example.com'); > 7 \| await page.fill('[data-test="search-input"]', 'Blue Jeans'); \| ^ 8 \| await page.click('[data-test="search-button"]'); 9 \| 10 \| // Step 2: Open the product "Blue Jeans" in search results at /home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests… |

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
| Abordagem | baseline |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline_playwright_locators_20260724_02/suite_adicionar_wishlist.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/specs/suite_adicionar_wishlist.txt` |

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
| Ações de usuário | 7 | cliques, preenchimentos e ações similares |
| Locators | 3 | total identificado estaticamente |
| Locators semânticos | 0 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `/login`
- `/wishlist`

**Textos extraídos dos locators:**

- `Camera`
- `Product added to wishlist`

### Pontos para revisão contra o grafo

**URLs não encontradas:**

- _nenhuma_

**Textos de locators não encontrados:**

- _nenhum_

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 440 caracteres; 1 linhas |
| Estado da execução | falhou |
| Duração | 12.806 s |
| Tipo de erro | locator_timeout |
| Mensagem | TimeoutError: page.fill: Timeout 10000ms exceeded. Call log: - waiting for locator('#username') 5 \| // Assuming there's a fixture for authentication with valid credentials 6 \| await page.goto('/login'); > 7 \| await page.fill('#username', 'validUsername'); \| ^ 8 \| await page.fill('#password', 'validPassword'); 9 \| await page.click('button[type="submit"]'); 10 \| await expect(page).toHaveURL('/dashboard'); at /home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generate… |

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
| Abordagem | baseline |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline_playwright_locators_20260724_02/suite_busca_blue_jeans.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/specs/suite_busca_blue_jeans.txt` |

### Leitura rápida

- ✅ Estrutura mínima do Playwright reconhecida.
- ✅ O teste contém asserção.
- ✅ Não usa espera fixa.
- **Risco estimado dos seletores:** médio.
- **URLs fundamentadas no grafo:** 0,0%.
- **Textos de locators fundamentados no grafo:** 100,0%.

### Estrutura e seletores

| Métrica | Resultado | Leitura |
| --- | --- | --- |
| Importa `@playwright/test` | sim | necessário para execução |
| Possui bloco `test(...)` | sim | estrutura do caso de teste |
| Possui `expect(...)` | sim | indício de verificação do resultado |
| Ações de usuário | 3 | cliques, preenchimentos e ações similares |
| Locators | 3 | total identificado estaticamente |
| Locators semânticos | 0 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://examplestore.com`

**Textos extraídos dos locators:**

- _nenhum texto de locator identificado_

### Pontos para revisão contra o grafo

**URLs não encontradas:**

- `https://examplestore.com`

**Textos de locators não encontrados:**

- _nenhum_

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 279 caracteres; 1 linhas |
| Estado da execução | falhou |
| Duração | 12.859 s |
| Tipo de erro | locator_timeout |
| Mensagem | TimeoutError: locator.fill: Timeout 10000ms exceeded. Call log: - waiting for locator('#search-input') 8 \| // Search for 'Blue Jeans' 9 \| const searchInput = page.locator('#search-input'); > 10 \| await searchInput.fill('Blue Jeans'); \| ^ 11 \| await searchInput.press('Enter'); 12 \| 13 \| // Wait for results to load at /home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline_playwright_locators_20260724_02/suite_busca_blue_jeans.spec.ts:10:23 |

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
| Abordagem | baseline |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline_playwright_locators_20260724_02/suite_checkout_blue_jeans.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/specs/suite_checkout_blue_jeans.txt` |

### Leitura rápida

- ✅ Estrutura mínima do Playwright reconhecida.
- ✅ O teste contém asserção.
- ✅ Não usa espera fixa.
- **Risco estimado dos seletores:** médio.
- **URLs fundamentadas no grafo:** 0,0%.
- **Textos de locators fundamentados no grafo:** 50,0%.

### Estrutura e seletores

| Métrica | Resultado | Leitura |
| --- | --- | --- |
| Importa `@playwright/test` | sim | necessário para execução |
| Possui bloco `test(...)` | sim | estrutura do caso de teste |
| Possui `expect(...)` | sim | indício de verificação do resultado |
| Ações de usuário | 15 | cliques, preenchimentos e ações similares |
| Locators | 2 | total identificado estaticamente |
| Locators semânticos | 0 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://example.com/login`
- `https://example.com/search?q=Blue+Jeans`

**Textos extraídos dos locators:**

- `Blue Jeans`
- `Order processed successfully`

### Pontos para revisão contra o grafo

**URLs não encontradas:**

- `https://example.com/login`
- `https://example.com/search?q=Blue+Jeans`

**Textos de locators não encontrados:**

- `Order processed successfully`

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 794 caracteres; 1 linhas |
| Estado da execução | falhou |
| Duração | 10.361 s |
| Tipo de erro | locator_timeout |
| Mensagem | TimeoutError: page.fill: Timeout 10000ms exceeded. Call log: - waiting for locator('#username') 5 \| // Assuming authentication is handled by a fixture or setup function 6 \| await page.goto('https://example.com/login'); > 7 \| await page.fill('#username', 'testuser'); \| ^ 8 \| await page.fill('#password', 'testpass'); 9 \| await page.click('#login-button'); 10 \| }); at /home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline_playwright_locators_20260… |

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
| Abordagem | baseline |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline_playwright_locators_20260724_02/suite_configurar_desktop.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/specs/suite_configurar_desktop.txt` |

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
| Ações de usuário | 8 | cliques, preenchimentos e ações similares |
| Locators | 2 | total identificado estaticamente |
| Locators semânticos | 0 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `/computers`

**Textos extraídos dos locators:**

- `Product added to cart`
- `Configured Desktop`

### Pontos para revisão contra o grafo

**URLs não encontradas:**

- _nenhuma_

**Textos de locators não encontrados:**

- `Configured Desktop`

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 474 caracteres; 1 linhas |
| Estado da execução | falhou |
| Duração | 13.467 s |
| Tipo de erro | locator_timeout |
| Mensagem | TimeoutError: page.click: Timeout 10000ms exceeded. Call log: - waiting for locator('text=Desktops') - locator resolved to 4 elements. Proceeding with the first one: <a href="/desktops">Desktops↵ </a> - attempting click action 2 × waiting for element to be visible, enabled and stable - element is not visible - retrying click action - waiting 20ms 2 × waiting for element to be visible, enabled and stable - element is not visible - retrying click action - waiting 100ms 19 × waiting for element to… |

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
| Abordagem | baseline |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline_playwright_locators_20260724_02/suite_detalhes_fiction.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/specs/suite_detalhes_fiction.txt` |

### Leitura rápida

- ✅ Estrutura mínima do Playwright reconhecida.
- ✅ O teste contém asserção.
- ✅ Não usa espera fixa.
- **Risco estimado dos seletores:** médio.
- **URLs fundamentadas no grafo:** 0,0%.
- **Textos de locators fundamentados no grafo:** 100,0%.

### Estrutura e seletores

| Métrica | Resultado | Leitura |
| --- | --- | --- |
| Importa `@playwright/test` | sim | necessário para execução |
| Possui bloco `test(...)` | sim | estrutura do caso de teste |
| Possui `expect(...)` | sim | indício de verificação do resultado |
| Ações de usuário | 3 | cliques, preenchimentos e ações similares |
| Locators | 2 | total identificado estaticamente |
| Locators semânticos | 0 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://example.com/search`

**Textos extraídos dos locators:**

- `/fiction`

### Pontos para revisão contra o grafo

**URLs não encontradas:**

- `https://example.com/search`

**Textos de locators não encontrados:**

- _nenhum_

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 284 caracteres; 1 linhas |
| Estado da execução | falhou |
| Duração | 10.361 s |
| Tipo de erro | locator_timeout |
| Mensagem | TimeoutError: page.fill: Timeout 10000ms exceeded. Call log: - waiting for locator('input[name="search"]') 7 \| 8 \| // Search for the product "Fiction" > 9 \| await page.fill('input[name="search"]', 'Fiction'); \| ^ 10 \| await page.click('button[type="submit"]'); 11 \| 12 \| // Open the product details page at /home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline_playwright_locators_20260724_02/suite_detalhes_fiction.spec.ts:9:16 |

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
| Abordagem | baseline |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline_playwright_locators_20260724_02/suite_limpar_carrinho.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/specs/suite_limpar_carrinho.txt` |

### Leitura rápida

- ✅ Estrutura mínima do Playwright reconhecida.
- ✅ O teste contém asserção.
- ✅ Não usa espera fixa.
- **Risco estimado dos seletores:** médio.
- **URLs fundamentadas no grafo:** 0,0%.
- **Textos de locators fundamentados no grafo:** 100,0%.

### Estrutura e seletores

| Métrica | Resultado | Leitura |
| --- | --- | --- |
| Importa `@playwright/test` | sim | necessário para execução |
| Possui bloco `test(...)` | sim | estrutura do caso de teste |
| Possui `expect(...)` | sim | indício de verificação do resultado |
| Ações de usuário | 5 | cliques, preenchimentos e ações similares |
| Locators | 1 | total identificado estaticamente |
| Locators semânticos | 0 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `/products`

**Textos extraídos dos locators:**

- _nenhum texto de locator identificado_

### Pontos para revisão contra o grafo

**URLs não encontradas:**

- `/products`

**Textos de locators não encontrados:**

- _nenhum_

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 260 caracteres; 1 linhas |
| Estado da execução | falhou |
| Duração | 12.908 s |
| Tipo de erro | locator_timeout |
| Mensagem | TimeoutError: page.click: Timeout 10000ms exceeded. Call log: - waiting for locator('text=Blue Jeans') 5 \| // Add Blue Jeans to the cart 6 \| await page.goto('/products'); > 7 \| await page.click('text=Blue Jeans'); \| ^ 8 \| await page.click('button=add-to-cart'); 9 \| }); 10 \| at /home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline_playwright_locators_20260724_02/suite_limpar_carrinho.spec.ts:7:16 |

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
| Abordagem | baseline |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline_playwright_locators_20260724_02/suite_limpar_wishlist.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/specs/suite_limpar_wishlist.txt` |

### Leitura rápida

- ✅ Estrutura mínima do Playwright reconhecida.
- ✅ O teste contém asserção.
- ✅ Não usa espera fixa.
- **Risco estimado dos seletores:** médio.
- **URLs fundamentadas no grafo:** 50,0%.
- **Textos de locators fundamentados no grafo:** 100,0%.

### Estrutura e seletores

| Métrica | Resultado | Leitura |
| --- | --- | --- |
| Importa `@playwright/test` | sim | necessário para execução |
| Possui bloco `test(...)` | sim | estrutura do caso de teste |
| Possui `expect(...)` | sim | indício de verificação do resultado |
| Ações de usuário | 4 | cliques, preenchimentos e ações similares |
| Locators | 1 | total identificado estaticamente |
| Locators semânticos | 0 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `/products`
- `/wishlist`

**Textos extraídos dos locators:**

- _nenhum texto de locator identificado_

### Pontos para revisão contra o grafo

**URLs não encontradas:**

- `/products`

**Textos de locators não encontrados:**

- _nenhum_

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 350 caracteres; 1 linhas |
| Estado da execução | falhou |
| Duração | 0.187 s |
| Tipo de erro | runtime_failure |
| Mensagem | ReferenceError: authenticateWithValidCredentials is not defined 4 \| test.beforeEach(async ({ page }) => { 5 \| // Assuming there's a function to authenticate with valid credentials > 6 \| await authenticateWithValidCredentials(page); \| ^ 7 \| }); 8 \| 9 \| test('Removal of all products from the wishlist', async ({ page }) => { at /home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline_playwright_locators_20260724_02/suite_limpar_wishlist.spec.ts:6:5 |

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
| Abordagem | baseline |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline_playwright_locators_20260724_02/suite_login_invalido.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/specs/suite_login_invalido.txt` |

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
| Ações de usuário | 3 | cliques, preenchimentos e ações similares |
| Locators | 0 | total identificado estaticamente |
| Locators semânticos | 0 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demowebshop.tricentis.com/login`

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
| Tamanho da entrada | 354 caracteres; 1 linhas |
| Estado da execução | falhou |
| Duração | 12.999 s |
| Tipo de erro | locator_timeout |
| Mensagem | TimeoutError: page.click: Timeout 10000ms exceeded. Call log: - waiting for locator('#login-button') 13 \| 14 \| // Submit the login form > 15 \| await page.click('#login-button'); \| ^ 16 \| 17 \| // Verify that the user is kept unauthenticated and informed of failed login 18 \| const errorMessage = await page.textContent('.message-error'); at /home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline_playwright_locators_20260724_02/suite_login_invalido.… |

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
| Abordagem | baseline |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline_playwright_locators_20260724_02/suite_login_valido.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/specs/suite_login_valido.txt` |

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
| Locators | 2 | total identificado estaticamente |
| Locators semânticos | 0 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demowebshop.tricentis.com/login`

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
| Tamanho da entrada | 298 caracteres; 1 linhas |
| Estado da execução | falhou |
| Duração | 12.938 s |
| Tipo de erro | locator_timeout |
| Mensagem | TimeoutError: page.click: Timeout 10000ms exceeded. Call log: - waiting for locator('button[type="submit"]') 11 \| 12 \| // Submit the login form > 13 \| await page.click('button[type="submit"]'); \| ^ 14 \| 15 \| // The system authenticates the user and displays the account and Log out links 16 \| await expect(page.locator('.account')).toBeVisible(); at /home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline_playwright_locators_20260724_02/suite_login… |

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
| Abordagem | baseline |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline_playwright_locators_20260724_02/suite_logout.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/specs/suite_logout.txt` |

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
| Locators | 2 | total identificado estaticamente |
| Locators semânticos | 0 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `/login`

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
| Tamanho da entrada | 216 caracteres; 1 linhas |
| Estado da execução | falhou |
| Duração | 12.994 s |
| Tipo de erro | locator_timeout |
| Mensagem | TimeoutError: page.fill: Timeout 10000ms exceeded. Call log: - waiting for locator('#username') 7 \| 8 \| // Fill in valid credentials and submit the form > 9 \| await page.fill('#username', 'validUsername'); \| ^ 10 \| await page.fill('#password', 'validPassword'); 11 \| await page.click('button[type="submit"]'); 12 \| at /home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline_playwright_locators_20260724_02/suite_logout.spec.ts:9:16 |

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
| Abordagem | baseline |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline_playwright_locators_20260724_02/suite_registro_usuario.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/specs/suite_registro_usuario.txt` |

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
| Locators semânticos | 0 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demowebshop.tricentis.com/register`

**Textos extraídos dos locators:**

- `Your registration completed`

### Pontos para revisão contra o grafo

**URLs não encontradas:**

- _nenhuma_

**Textos de locators não encontrados:**

- _nenhum_

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 515 caracteres; 1 linhas |
| Estado da execução | falhou |
| Duração | 15.014 s |
| Tipo de erro | locator_timeout |
| Mensagem | TimeoutError: page.fill: Timeout 10000ms exceeded. Call log: - waiting for locator('#Email') 30 \| // User selects Continue and returns to the store authenticated 31 \| await page.click('a[href="/logout"]'); > 32 \| await page.fill('#Email', email); \| ^ 33 \| await page.fill('#Password', password); 34 \| await page.click('#login-button'); 35 \| await expect(page.locator('.account')).toContainText(email); at /home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tes… |

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
| Abordagem | baseline |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline_playwright_locators_20260724_02/user_registration_book_purchase.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | não localizada/informada |

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
| Ações de usuário | 11 | cliques, preenchimentos e ações similares |
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
| Tamanho da entrada | não disponível |
| Estado da execução | falhou |
| Duração | 14.106 s |
| Tipo de erro | locator_timeout |
| Mensagem | TimeoutError: page.click: Timeout 10000ms exceeded. Call log: - waiting for locator('button[type="submit"]') 25 \| 26 \| // Click on the Register button to complete the registration > 27 \| await page.click('button[type="submit"]'); \| ^ 28 \| 29 \| // Verify that the user is logged in and redirected to the home page 30 \| expect(page.url()).toContain('/customer/account'); at /home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline_playwright_locators_2… |

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
