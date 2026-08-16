# Relatório auxiliar de avaliação dos testes E2E

> Este relatório é uma ferramenta não oficial de apoio à análise. As métricas automáticas são evidências; não constituem, isoladamente, uma avaliação de correção semântica.

## Visão geral

| Indicador | Resultado |
| --- | --- |
| Testes analisados | 20 |
| Com estrutura mínima reconhecida | 20 de 20 (100,0%) |
| Com pelo menos uma asserção | 20 de 20 (100,0%) |
| Com espera fixa `waitForTimeout` | 0 de 20 (0,0%) |
| Risco dos seletores | baixo: 0; médio: 11; alto: 0; não aplicável: 9 |
| Resultado da execução | falhou: 20 |
| Tamanho médio da entrada da LLM | 362 caracteres; 1,0 linhas |
| Conformidade com o grafo | não analisada |

## Como interpretar

- **Estrutura mínima** verifica apenas a presença de importação do Playwright, bloco de teste e asserção.
- **Risco dos seletores** é uma heurística: seletores semânticos reduzem o risco; XPath e esperas fixas elevam o risco.
- **Cobertura pelo grafo** indica se URLs e textos de locators foram encontrados nas evidências coletadas. Uma ausência é um ponto para revisão, não prova de erro.
- **Rubrica humana** deve receber notas de 0 (não atende), 1 (atende parcialmente) ou 2 (atende completamente).

## 1. fluxo_computadores_desktops

| Identificação | Valor |
| --- | --- |
| Abordagem | baseline |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline_qwen25coder_demowebshop20_20260727_01/fluxo_computadores_desktops.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/tmp/qwen-demowebshop20-inputs/specs/fluxo_computadores_desktops.txt` |

### Leitura rápida

- ✅ Estrutura mínima do Playwright reconhecida.
- ✅ O teste contém asserção.
- ✅ Não usa espera fixa.
- **Risco estimado dos seletores:** médio.
- **Conformidade com o grafo:** não analisada nesta execução.

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

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 144 caracteres; 1 linhas |
| Estado da execução | falhou |
| Duração | 11.791 s |
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

## 2. suite_adicionar_dois_produtos_carrinho

| Identificação | Valor |
| --- | --- |
| Abordagem | baseline |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline_qwen25coder_demowebshop20_20260727_01/suite_adicionar_dois_produtos_carrinho.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/tmp/qwen-demowebshop20-inputs/specs/suite_adicionar_dois_produtos_carrinho.txt` |

### Leitura rápida

- ✅ Estrutura mínima do Playwright reconhecida.
- ✅ O teste contém asserção.
- ✅ Não usa espera fixa.
- **Risco estimado dos seletores:** médio.
- **Conformidade com o grafo:** não analisada nesta execução.

### Estrutura e seletores

| Métrica | Resultado | Leitura |
| --- | --- | --- |
| Importa `@playwright/test` | sim | necessário para execução |
| Possui bloco `test(...)` | sim | estrutura do caso de teste |
| Possui `expect(...)` | sim | indício de verificação do resultado |
| Ações de usuário | 5 | cliques, preenchimentos e ações similares |
| Locators | 5 | total identificado estaticamente |
| Locators semânticos | 0 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://examplestore.com`

**Textos extraídos dos locators:**

- `Computing`
- `Fiction`
- `$20.00`

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 284 caracteres; 1 linhas |
| Estado da execução | falhou |
| Duração | 13.823 s |
| Tipo de erro | locator_timeout |
| Mensagem | TimeoutError: page.click: Timeout 10000ms exceeded. Call log: - waiting for locator('#computing-product') 7 \| 8 \| // Add Computing product to the cart > 9 \| await page.click('#computing-product'); \| ^ 10 \| await page.click('#add-to-cart-computing'); 11 \| 12 \| // Add Fiction product to the cart at /home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline_qwen25coder_demowebshop20_20260727_01/suite_adicionar_dois_produtos_carrinho.spec.ts:9:16 |

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

## 3. suite_atualizar_quantidade_carrinho

| Identificação | Valor |
| --- | --- |
| Abordagem | baseline |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline_qwen25coder_demowebshop20_20260727_01/suite_atualizar_quantidade_carrinho.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/tmp/qwen-demowebshop20-inputs/specs/suite_atualizar_quantidade_carrinho.txt` |

### Leitura rápida

- ✅ Estrutura mínima do Playwright reconhecida.
- ✅ O teste contém asserção.
- ✅ Não usa espera fixa.
- **Risco estimado dos seletores:** não aplicável.
- **Conformidade com o grafo:** não analisada nesta execução.

### Estrutura e seletores

| Métrica | Resultado | Leitura |
| --- | --- | --- |
| Importa `@playwright/test` | sim | necessário para execução |
| Possui bloco `test(...)` | sim | estrutura do caso de teste |
| Possui `expect(...)` | sim | indício de verificação do resultado |
| Ações de usuário | 6 | cliques, preenchimentos e ações similares |
| Locators | 0 | total identificado estaticamente |
| Locators semânticos | 0 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `/products`

**Textos extraídos dos locators:**

- _nenhum texto de locator identificado_

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 382 caracteres; 1 linhas |
| Estado da execução | falhou |
| Duração | 12.870 s |
| Tipo de erro | locator_timeout |
| Mensagem | TimeoutError: page.click: Timeout 10000ms exceeded. Call log: - waiting for locator('text=Computing and Internet') 5 \| // Add Computing and Internet to the cart 6 \| await page.goto('/products'); > 7 \| await page.click('text=Computing and Internet'); \| ^ 8 \| await page.click('button=add-to-cart'); 9 \| 10 \| // Access Shopping cart at /home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline_qwen25coder_demowebshop20_20260727_01/suite_atualizar_quant… |

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

## 4. suite_busca_sem_resultados

| Identificação | Valor |
| --- | --- |
| Abordagem | baseline |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline_qwen25coder_demowebshop20_20260727_01/suite_busca_sem_resultados.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/tmp/qwen-demowebshop20-inputs/specs/suite_busca_sem_resultados.txt` |

### Leitura rápida

- ✅ Estrutura mínima do Playwright reconhecida.
- ✅ O teste contém asserção.
- ✅ Não usa espera fixa.
- **Risco estimado dos seletores:** médio.
- **Conformidade com o grafo:** não analisada nesta execução.

### Estrutura e seletores

| Métrica | Resultado | Leitura |
| --- | --- | --- |
| Importa `@playwright/test` | sim | necessário para execução |
| Possui bloco `test(...)` | sim | estrutura do caso de teste |
| Possui `expect(...)` | sim | indício de verificação do resultado |
| Ações de usuário | 2 | cliques, preenchimentos e ações similares |
| Locators | 3 | total identificado estaticamente |
| Locators semânticos | 0 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `/search`

**Textos extraídos dos locators:**

- _nenhum texto de locator identificado_

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 257 caracteres; 1 linhas |
| Estado da execução | falhou |
| Duração | 13.923 s |
| Tipo de erro | locator_timeout |
| Mensagem | TimeoutError: locator.fill: Timeout 10000ms exceeded. Call log: - waiting for locator('#search-input') 8 \| // Enter a unique term that does not correspond to any product 9 \| const searchInput = page.locator('#search-input'); > 10 \| await searchInput.fill('nonexistent-product-term'); \| ^ 11 \| 12 \| // Submit the search 13 \| const searchButton = page.locator('#search-button'); at /home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline_qwen25coder_d… |

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

## 5. suite_cadastro_campos_obrigatorios

| Identificação | Valor |
| --- | --- |
| Abordagem | baseline |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline_qwen25coder_demowebshop20_20260727_01/suite_cadastro_campos_obrigatorios.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/tmp/qwen-demowebshop20-inputs/specs/suite_cadastro_campos_obrigatorios.txt` |

### Leitura rápida

- ✅ Estrutura mínima do Playwright reconhecida.
- ✅ O teste contém asserção.
- ✅ Não usa espera fixa.
- **Risco estimado dos seletores:** médio.
- **Conformidade com o grafo:** não analisada nesta execução.

### Estrutura e seletores

| Métrica | Resultado | Leitura |
| --- | --- | --- |
| Importa `@playwright/test` | sim | necessário para execução |
| Possui bloco `test(...)` | sim | estrutura do caso de teste |
| Possui `expect(...)` | sim | indício de verificação do resultado |
| Ações de usuário | 10 | cliques, preenchimentos e ações similares |
| Locators | 5 | total identificado estaticamente |
| Locators semânticos | 0 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demowebshop.tricentis.com/register`

**Textos extraídos dos locators:**

- `First name is required.`
- `Last name is required.`
- `Email is required.`
- `Password is required.`
- `Confirm password is required.`

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 361 caracteres; 1 linhas |
| Estado da execução | falhou |
| Duração | 13.146 s |
| Tipo de erro | locator_timeout |
| Mensagem | TimeoutError: page.click: Timeout 10000ms exceeded. Call log: - waiting for locator('button[type="submit"]') 17 \| 18 \| // Submit the form > 19 \| await page.click('button[type="submit"]'); \| ^ 20 \| 21 \| // Check for validation messages 22 \| await expect(page.locator('.message-error')).toHaveText('First name is required.'); at /home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline_qwen25coder_demowebshop20_20260727_01/suite_cadastro_campos_obriga… |

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

## 6. suite_cadastro_confirmacao_senha

| Identificação | Valor |
| --- | --- |
| Abordagem | baseline |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline_qwen25coder_demowebshop20_20260727_01/suite_cadastro_confirmacao_senha.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/tmp/qwen-demowebshop20-inputs/specs/suite_cadastro_confirmacao_senha.txt` |

### Leitura rápida

- ✅ Estrutura mínima do Playwright reconhecida.
- ✅ O teste contém asserção.
- ✅ Não usa espera fixa.
- **Risco estimado dos seletores:** não aplicável.
- **Conformidade com o grafo:** não analisada nesta execução.

### Estrutura e seletores

| Métrica | Resultado | Leitura |
| --- | --- | --- |
| Importa `@playwright/test` | sim | necessário para execução |
| Possui bloco `test(...)` | sim | estrutura do caso de teste |
| Possui `expect(...)` | sim | indício de verificação do resultado |
| Ações de usuário | 6 | cliques, preenchimentos e ações similares |
| Locators | 0 | total identificado estaticamente |
| Locators semânticos | 0 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `/register`

**Textos extraídos dos locators:**

- _nenhum texto de locator identificado_

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 462 caracteres; 1 linhas |
| Estado da execução | falhou |
| Duração | 13.067 s |
| Tipo de erro | locator_timeout |
| Mensagem | TimeoutError: page.fill: Timeout 10000ms exceeded. Call log: - waiting for locator('#firstName') 7 \| 8 \| // Fill in First name and Last name with valid data > 9 \| await page.fill('#firstName', 'John'); \| ^ 10 \| await page.fill('#lastName', 'Doe'); 11 \| 12 \| // Fill in Email with a unique address generated for this execution at /home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline_qwen25coder_demowebshop20_20260727_01/suite_cadastro_confirmacao… |

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

## 7. suite_cadastro_senha_curta

| Identificação | Valor |
| --- | --- |
| Abordagem | baseline |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline_qwen25coder_demowebshop20_20260727_01/suite_cadastro_senha_curta.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/tmp/qwen-demowebshop20-inputs/specs/suite_cadastro_senha_curta.txt` |

### Leitura rápida

- ✅ Estrutura mínima do Playwright reconhecida.
- ✅ O teste contém asserção.
- ✅ Não usa espera fixa.
- **Risco estimado dos seletores:** médio.
- **Conformidade com o grafo:** não analisada nesta execução.

### Estrutura e seletores

| Métrica | Resultado | Leitura |
| --- | --- | --- |
| Importa `@playwright/test` | sim | necessário para execução |
| Possui bloco `test(...)` | sim | estrutura do caso de teste |
| Possui `expect(...)` | sim | indício de verificação do resultado |
| Ações de usuário | 6 | cliques, preenchimentos e ações similares |
| Locators | 1 | total identificado estaticamente |
| Locators semânticos | 0 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `/register`

**Textos extraídos dos locators:**

- _nenhum texto de locator identificado_

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 468 caracteres; 1 linhas |
| Estado da execução | falhou |
| Duração | 12.894 s |
| Tipo de erro | locator_timeout |
| Mensagem | TimeoutError: page.fill: Timeout 10000ms exceeded. Call log: - waiting for locator('#firstName') 7 \| 8 \| // Fill in First name and Last name with valid data > 9 \| await page.fill('#firstName', 'John'); \| ^ 10 \| await page.fill('#lastName', 'Doe'); 11 \| 12 \| // Fill in Email with a unique address generated for this execution at /home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline_qwen25coder_demowebshop20_20260727_01/suite_cadastro_senha_curta… |

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

## 8. suite_carrinho_inicialmente_vazio

| Identificação | Valor |
| --- | --- |
| Abordagem | baseline |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline_qwen25coder_demowebshop20_20260727_01/suite_carrinho_inicialmente_vazio.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/tmp/qwen-demowebshop20-inputs/specs/suite_carrinho_inicialmente_vazio.txt` |

### Leitura rápida

- ✅ Estrutura mínima do Playwright reconhecida.
- ✅ O teste contém asserção.
- ✅ Não usa espera fixa.
- **Risco estimado dos seletores:** não aplicável.
- **Conformidade com o grafo:** não analisada nesta execução.

### Estrutura e seletores

| Métrica | Resultado | Leitura |
| --- | --- | --- |
| Importa `@playwright/test` | sim | necessário para execução |
| Possui bloco `test(...)` | sim | estrutura do caso de teste |
| Possui `expect(...)` | sim | indício de verificação do resultado |
| Ações de usuário | 0 | cliques, preenchimentos e ações similares |
| Locators | 0 | total identificado estaticamente |
| Locators semânticos | 0 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `/shopping-cart`

**Textos extraídos dos locators:**

- _nenhum texto de locator identificado_

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 232 caracteres; 1 linhas |
| Estado da execução | falhou |
| Duração | 12.753 s |
| Tipo de erro | locator_timeout |
| Mensagem | TimeoutError: page.textContent: Timeout 10000ms exceeded. Call log: - waiting for locator('.item-count') 7 \| 8 \| // Check if the item count is displayed as zero > 9 \| const itemCount = await page.textContent('.item-count'); \| ^ 10 \| expect(itemCount).toBe('0'); 11 \| 12 \| // Check if the empty cart message is displayed at /home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline_qwen25coder_demowebshop20_20260727_01/suite_carrinho_inicialmente_vazi… |

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

## 9. suite_comparar_produtos

| Identificação | Valor |
| --- | --- |
| Abordagem | baseline |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline_qwen25coder_demowebshop20_20260727_01/suite_comparar_produtos.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/tmp/qwen-demowebshop20-inputs/specs/suite_comparar_produtos.txt` |

### Leitura rápida

- ✅ Estrutura mínima do Playwright reconhecida.
- ✅ O teste contém asserção.
- ✅ Não usa espera fixa.
- **Risco estimado dos seletores:** não aplicável.
- **Conformidade com o grafo:** não analisada nesta execução.

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

- `/computing-and-internet`
- `/fiction`
- `/compare-products`

**Textos extraídos dos locators:**

- _nenhum texto de locator identificado_

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 388 caracteres; 1 linhas |
| Estado da execução | falhou |
| Duração | 13.817 s |
| Tipo de erro | locator_timeout |
| Mensagem | TimeoutError: page.click: Timeout 10000ms exceeded. Call log: - waiting for locator('#addToCompareButton') 6 \| await page.goto('/computing-and-internet'); 7 \| // Select Add to compare list > 8 \| await page.click('#addToCompareButton'); \| ^ 9 \| 10 \| // Navigate to Fiction product page 11 \| await page.goto('/fiction'); at /home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline_qwen25coder_demowebshop20_20260727_01/suite_comparar_produtos.spec.ts:8… |

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

## 10. suite_enquete_sem_resposta

| Identificação | Valor |
| --- | --- |
| Abordagem | baseline |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline_qwen25coder_demowebshop20_20260727_01/suite_enquete_sem_resposta.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/tmp/qwen-demowebshop20-inputs/specs/suite_enquete_sem_resposta.txt` |

### Leitura rápida

- ✅ Estrutura mínima do Playwright reconhecida.
- ✅ O teste contém asserção.
- ✅ Não usa espera fixa.
- **Risco estimado dos seletores:** não aplicável.
- **Conformidade com o grafo:** não analisada nesta execução.

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

- `https://demowebshop.tricentis.com/`

**Textos extraídos dos locators:**

- _nenhum texto de locator identificado_

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 300 caracteres; 1 linhas |
| Estado da execução | falhou |
| Duração | 13.422 s |
| Tipo de erro | locator_timeout |
| Mensagem | TimeoutError: page.click: Timeout 10000ms exceeded. Call log: - waiting for locator('text="Community polls"') 7 \| 8 \| // Navigate to the Community poll titled "Do you like nopCommerce?" > 9 \| await page.click('text="Community polls"'); \| ^ 10 \| await page.click('text="Do you like nopCommerce?"'); 11 \| 12 \| // Attempt to vote without selecting an answer at /home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline_qwen25coder_demowebshop20_20260727_… |

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

## 11. suite_exibir_quatro_livros

| Identificação | Valor |
| --- | --- |
| Abordagem | baseline |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline_qwen25coder_demowebshop20_20260727_01/suite_exibir_quatro_livros.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/tmp/qwen-demowebshop20-inputs/specs/suite_exibir_quatro_livros.txt` |

### Leitura rápida

- ✅ Estrutura mínima do Playwright reconhecida.
- ✅ O teste contém asserção.
- ✅ Não usa espera fixa.
- **Risco estimado dos seletores:** médio.
- **Conformidade com o grafo:** não analisada nesta execução.

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

- `/books`

**Textos extraídos dos locators:**

- _nenhum texto de locator identificado_

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 240 caracteres; 1 linhas |
| Estado da execução | falhou |
| Duração | 13.005 s |
| Tipo de erro | locator_timeout |
| Mensagem | TimeoutError: locator.selectOption: Timeout 10000ms exceeded. Call log: - waiting for locator('#display-control') 8 \| test('displays no more than four product items when 4 is selected in the Display control', async ({ page }) => { 9 \| // Select 4 in the Display control > 10 \| await page.locator('#display-control').selectOption('4'); \| ^ 11 \| 12 \| // Wait for the products to update 13 \| await page.waitForSelector('.product-item'); at /home/martinsspn/dissertacao_e2e_semantico/python_app/teste_pr… |

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

## 12. suite_filtrar_livros_abaixo_25

| Identificação | Valor |
| --- | --- |
| Abordagem | baseline |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline_qwen25coder_demowebshop20_20260727_01/suite_filtrar_livros_abaixo_25.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/tmp/qwen-demowebshop20-inputs/specs/suite_filtrar_livros_abaixo_25.txt` |

### Leitura rápida

- ✅ Estrutura mínima do Playwright reconhecida.
- ✅ O teste contém asserção.
- ✅ Não usa espera fixa.
- **Risco estimado dos seletores:** não aplicável.
- **Conformidade com o grafo:** não analisada nesta execução.

### Estrutura e seletores

| Métrica | Resultado | Leitura |
| --- | --- | --- |
| Importa `@playwright/test` | sim | necessário para execução |
| Possui bloco `test(...)` | sim | estrutura do caso de teste |
| Possui `expect(...)` | sim | indício de verificação do resultado |
| Ações de usuário | 1 | cliques, preenchimentos e ações similares |
| Locators | 0 | total identificado estaticamente |
| Locators semânticos | 0 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `/books`

**Textos extraídos dos locators:**

- _nenhum texto de locator identificado_

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 223 caracteres; 1 linhas |
| Estado da execução | falhou |
| Duração | 13.978 s |
| Tipo de erro | locator_timeout |
| Mensagem | TimeoutError: page.textContent: Timeout 10000ms exceeded. Call log: - waiting for locator('.product-price') 13 \| 14 \| // Verify that only products under 25.00 are displayed > 15 \| const productPrices = await page.textContent('.product-price'); \| ^ 16 \| expect(productPrices).not.toContain('Over 25.00'); 17 \| }); 18 \| }); at /home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline_qwen25coder_demowebshop20_20260727_01/suite_filtrar_livros_abaixo_25… |

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

## 13. suite_navegar_cartoes_presente

| Identificação | Valor |
| --- | --- |
| Abordagem | baseline |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline_qwen25coder_demowebshop20_20260727_01/suite_navegar_cartoes_presente.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/tmp/qwen-demowebshop20-inputs/specs/suite_navegar_cartoes_presente.txt` |

### Leitura rápida

- ✅ Estrutura mínima do Playwright reconhecida.
- ✅ O teste contém asserção.
- ✅ Não usa espera fixa.
- **Risco estimado dos seletores:** médio.
- **Conformidade com o grafo:** não analisada nesta execução.

### Estrutura e seletores

| Métrica | Resultado | Leitura |
| --- | --- | --- |
| Importa `@playwright/test` | sim | necessário para execução |
| Possui bloco `test(...)` | sim | estrutura do caso de teste |
| Possui `expect(...)` | sim | indício de verificação do resultado |
| Ações de usuário | 1 | cliques, preenchimentos e ações similares |
| Locators | 3 | total identificado estaticamente |
| Locators semânticos | 0 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demowebshop.tricentis.com/`

**Textos extraídos dos locators:**

- `h1`
- `Gift Cards`
- `Home > Gift Cards`

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 240 caracteres; 1 linhas |
| Estado da execução | falhou |
| Duração | 12.148 s |
| Tipo de erro | assertion_failure |
| Mensagem | Error: expect(locator).toContainText(expected) failed Locator: locator('.breadcrumb') Timeout: 7000ms - Expected substring - 1 + Received string + 9 - Home > Gift Cards + + + Home + / + + Gift Cards + + + Call log: - Expect "toContainText" with timeout 7000ms - waiting for locator('.breadcrumb') 18 × locator resolved to <div class="breadcrumb">…</div> - unexpected value " Home / Gift Cards " 11 \| // System displays the Gift Cards category page, its breadcrumb, and the available gift card produc… |

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

## 14. suite_navegar_categoria_livros

| Identificação | Valor |
| --- | --- |
| Abordagem | baseline |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline_qwen25coder_demowebshop20_20260727_01/suite_navegar_categoria_livros.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/tmp/qwen-demowebshop20-inputs/specs/suite_navegar_categoria_livros.txt` |

### Leitura rápida

- ✅ Estrutura mínima do Playwright reconhecida.
- ✅ O teste contém asserção.
- ✅ Não usa espera fixa.
- **Risco estimado dos seletores:** médio.
- **Conformidade com o grafo:** não analisada nesta execução.

### Estrutura e seletores

| Métrica | Resultado | Leitura |
| --- | --- | --- |
| Importa `@playwright/test` | sim | necessário para execução |
| Possui bloco `test(...)` | sim | estrutura do caso de teste |
| Possui `expect(...)` | sim | indício de verificação do resultado |
| Ações de usuário | 1 | cliques, preenchimentos e ações similares |
| Locators | 5 | total identificado estaticamente |
| Locators semânticos | 0 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demowebshop.tricentis.com/`

**Textos extraídos dos locators:**

- `Home > Books`
- `Computing and Internet`
- `Fiction`
- `Health Book`

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 280 caracteres; 1 linhas |
| Estado da execução | falhou |
| Duração | 10.873 s |
| Tipo de erro | assertion_failure |
| Mensagem | Error: expect(locator).toContainText(expected) failed Locator: locator('.breadcrumb') Timeout: 7000ms - Expected substring - 1 + Received string + 9 - Home > Books + + + Home + / + + Books + + + Call log: - Expect "toContainText" with timeout 7000ms - waiting for locator('.breadcrumb') 18 × locator resolved to <div class="breadcrumb">…</div> - unexpected value " Home / Books " 10 \| 11 \| // System displays the Books category page, its breadcrumb, and the available book products > 12 \| await expe… |

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

## 15. suite_navegar_sobre_nos

| Identificação | Valor |
| --- | --- |
| Abordagem | baseline |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline_qwen25coder_demowebshop20_20260727_01/suite_navegar_sobre_nos.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/tmp/qwen-demowebshop20-inputs/specs/suite_navegar_sobre_nos.txt` |

### Leitura rápida

- ✅ Estrutura mínima do Playwright reconhecida.
- ✅ O teste contém asserção.
- ✅ Não usa espera fixa.
- **Risco estimado dos seletores:** médio.
- **Conformidade com o grafo:** não analisada nesta execução.

### Estrutura e seletores

| Métrica | Resultado | Leitura |
| --- | --- | --- |
| Importa `@playwright/test` | sim | necessário para execução |
| Possui bloco `test(...)` | sim | estrutura do caso de teste |
| Possui `expect(...)` | sim | indício de verificação do resultado |
| Ações de usuário | 2 | cliques, preenchimentos e ações similares |
| Locators | 1 | total identificado estaticamente |
| Locators semânticos | 0 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demo.webshopapp.com`

**Textos extraídos dos locators:**

- `h1`

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 229 caracteres; 1 linhas |
| Estado da execução | falhou |
| Duração | 11.169 s |
| Tipo de erro | locator_timeout |
| Mensagem | TimeoutError: page.click: Timeout 10000ms exceeded. Call log: - waiting for locator('footer a:has-text("Information")') 7 \| 8 \| // Select About us in the Information section of the footer > 9 \| await page.click('footer a:has-text("Information")'); \| ^ 10 \| await page.click('a:has-text("About us")'); 11 \| 12 \| // Verify that the About us page is displayed at /home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline_qwen25coder_demowebshop20_2026072… |

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

## 16. suite_ordenar_livros_por_preco

| Identificação | Valor |
| --- | --- |
| Abordagem | baseline |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline_qwen25coder_demowebshop20_20260727_01/suite_ordenar_livros_por_preco.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/tmp/qwen-demowebshop20-inputs/specs/suite_ordenar_livros_por_preco.txt` |

### Leitura rápida

- ✅ Estrutura mínima do Playwright reconhecida.
- ✅ O teste contém asserção.
- ✅ Não usa espera fixa.
- **Risco estimado dos seletores:** médio.
- **Conformidade com o grafo:** não analisada nesta execução.

### Estrutura e seletores

| Métrica | Resultado | Leitura |
| --- | --- | --- |
| Importa `@playwright/test` | sim | necessário para execução |
| Possui bloco `test(...)` | sim | estrutura do caso de teste |
| Possui `expect(...)` | sim | indício de verificação do resultado |
| Ações de usuário | 2 | cliques, preenchimentos e ações similares |
| Locators | 1 | total identificado estaticamente |
| Locators semânticos | 0 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `/books`

**Textos extraídos dos locators:**

- _nenhum texto de locator identificado_

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 265 caracteres; 1 linhas |
| Estado da execução | falhou |
| Duração | 13.191 s |
| Tipo de erro | locator_timeout |
| Mensagem | TimeoutError: page.click: Timeout 10000ms exceeded. Call log: - waiting for locator('text=Price: Low to High') - locator resolved to <option value="https://demowebshop.tricentis.com/books?orderby=10">Price: Low to High</option> - attempting click action 2 × waiting for element to be visible, enabled and stable - element is not visible - retrying click action - waiting 20ms 2 × waiting for element to be visible, enabled and stable - element is not visible - retrying click action - waiting 100ms… |

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

## 17. suite_persistencia_carrinho_apos_login

| Identificação | Valor |
| --- | --- |
| Abordagem | baseline |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline_qwen25coder_demowebshop20_20260727_01/suite_persistencia_carrinho_apos_login.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/tmp/qwen-demowebshop20-inputs/specs/suite_persistencia_carrinho_apos_login.txt` |

### Leitura rápida

- ✅ Estrutura mínima do Playwright reconhecida.
- ✅ O teste contém asserção.
- ✅ Não usa espera fixa.
- **Risco estimado dos seletores:** não aplicável.
- **Conformidade com o grafo:** não analisada nesta execução.

### Estrutura e seletores

| Métrica | Resultado | Leitura |
| --- | --- | --- |
| Importa `@playwright/test` | sim | necessário para execução |
| Possui bloco `test(...)` | sim | estrutura do caso de teste |
| Possui `expect(...)` | sim | indício de verificação do resultado |
| Ações de usuário | 10 | cliques, preenchimentos e ações similares |
| Locators | 0 | total identificado estaticamente |
| Locators semânticos | 0 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://example.com/login`
- `https://example.com/cart`
- `https://example.com/products`
- `https://example.com/logout`

**Textos extraídos dos locators:**

- _nenhum texto de locator identificado_

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 467 caracteres; 1 linhas |
| Estado da execução | falhou |
| Duração | 10.349 s |
| Tipo de erro | locator_timeout |
| Mensagem | TimeoutError: page.fill: Timeout 10000ms exceeded. Call log: - waiting for locator('#username') 15 \| // Authenticate with valid credentials 16 \| await page.goto('https://example.com/login'); > 17 \| await page.fill('#username', 'testuser'); \| ^ 18 \| await page.fill('#password', 'testpass'); 19 \| await page.click('#login-button'); 20 \| at /home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline_qwen25coder_demowebshop20_20260727_01/suite_persistenc… |

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

## 18. suite_produtos_visualizados_recentemente

| Identificação | Valor |
| --- | --- |
| Abordagem | baseline |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline_qwen25coder_demowebshop20_20260727_01/suite_produtos_visualizados_recentemente.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/tmp/qwen-demowebshop20-inputs/specs/suite_produtos_visualizados_recentemente.txt` |

### Leitura rápida

- ✅ Estrutura mínima do Playwright reconhecida.
- ✅ O teste contém asserção.
- ✅ Não usa espera fixa.
- **Risco estimado dos seletores:** não aplicável.
- **Conformidade com o grafo:** não analisada nesta execução.

### Estrutura e seletores

| Métrica | Resultado | Leitura |
| --- | --- | --- |
| Importa `@playwright/test` | sim | necessário para execução |
| Possui bloco `test(...)` | sim | estrutura do caso de teste |
| Possui `expect(...)` | sim | indício de verificação do resultado |
| Ações de usuário | 2 | cliques, preenchimentos e ações similares |
| Locators | 0 | total identificado estaticamente |
| Locators semânticos | 0 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- _nenhuma URL literal identificada_

**Textos extraídos dos locators:**

- _nenhum texto de locator identificado_

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 386 caracteres; 1 linhas |
| Estado da execução | falhou |
| Duração | 10.511 s |
| Tipo de erro | locator_timeout |
| Mensagem | TimeoutError: page.click: Timeout 10000ms exceeded. Call log: - waiting for locator('text=Customer Service') 14 \| 15 \| // Select Recently viewed products in the Customer service section > 16 \| await newPage.click('text=Customer Service'); \| ^ 17 \| await newPage.click('text=Recently Viewed Products'); 18 \| 19 \| // Check if both products are displayed at /home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline_qwen25coder_demowebshop20_20260727_01/… |

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

## 19. suite_visualizacao_livros_em_lista

| Identificação | Valor |
| --- | --- |
| Abordagem | baseline |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline_qwen25coder_demowebshop20_20260727_01/suite_visualizacao_livros_em_lista.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/tmp/qwen-demowebshop20-inputs/specs/suite_visualizacao_livros_em_lista.txt` |

### Leitura rápida

- ✅ Estrutura mínima do Playwright reconhecida.
- ✅ O teste contém asserção.
- ✅ Não usa espera fixa.
- **Risco estimado dos seletores:** médio.
- **Conformidade com o grafo:** não analisada nesta execução.

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

- `/books`

**Textos extraídos dos locators:**

- _nenhum texto de locator identificado_

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 247 caracteres; 1 linhas |
| Estado da execução | falhou |
| Duração | 10.254 s |
| Tipo de erro | assertion_failure |
| Mensagem | Error: expect(locator).toBeVisible() failed Locator: locator('.grid-view') Expected: visible Timeout: 7000ms Error: element(s) not found Call log: - Expect "toBeVisible" with timeout 7000ms - waiting for locator('.grid-view') 8 \| // Verify initial Grid view 9 \| const gridView = page.locator('.grid-view'); > 10 \| expect(gridView).toBeVisible(); \| ^ 11 \| 12 \| // Select List view 13 \| await page.click('button.view-as-list'); at /home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e… |

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

## 20. user_registration_book_purchase

| Identificação | Valor |
| --- | --- |
| Abordagem | baseline |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline_qwen25coder_demowebshop20_20260727_01/user_registration_book_purchase.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/tmp/qwen-demowebshop20-inputs/specs/user_registration_book_purchase.txt` |

### Leitura rápida

- ✅ Estrutura mínima do Playwright reconhecida.
- ✅ O teste contém asserção.
- ✅ Não usa espera fixa.
- **Risco estimado dos seletores:** não aplicável.
- **Conformidade com o grafo:** não analisada nesta execução.

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

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 1377 caracteres; 1 linhas |
| Estado da execução | falhou |
| Duração | 14.057 s |
| Tipo de erro | locator_timeout |
| Mensagem | TimeoutError: page.click: Timeout 10000ms exceeded. Call log: - waiting for locator('button[type="submit"]') 25 \| 26 \| // Click on the Register button to complete the registration > 27 \| await page.click('button[type="submit"]'); \| ^ 28 \| 29 \| // Verify that the user is logged in and redirected to the home page 30 \| expect(page.url()).toContain('/customer/account'); at /home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline_qwen25coder_demowebsh… |

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
