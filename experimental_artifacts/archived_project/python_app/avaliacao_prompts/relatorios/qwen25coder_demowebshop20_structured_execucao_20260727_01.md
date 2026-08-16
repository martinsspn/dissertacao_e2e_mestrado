# Relatório auxiliar de avaliação dos testes E2E

> Este relatório é uma ferramenta não oficial de apoio à análise. As métricas automáticas são evidências; não constituem, isoladamente, uma avaliação de correção semântica.

## Visão geral

| Indicador | Resultado |
| --- | --- |
| Testes analisados | 20 |
| Com estrutura mínima reconhecida | 20 de 20 (100,0%) |
| Com pelo menos uma asserção | 20 de 20 (100,0%) |
| Com espera fixa `waitForTimeout` | 0 de 20 (0,0%) |
| Risco dos seletores | baixo: 11; médio: 9; alto: 0; não aplicável: 0 |
| Resultado da execução | passou: 2; falhou: 18 |
| Tamanho médio da entrada da LLM | 4188 caracteres; 48,6 linhas |
| Conformidade com o grafo | não analisada |

## Como interpretar

- **Estrutura mínima** verifica apenas a presença de importação do Playwright, bloco de teste e asserção.
- **Risco dos seletores** é uma heurística: seletores semânticos reduzem o risco; XPath e esperas fixas elevam o risco.
- **Cobertura pelo grafo** indica se URLs e textos de locators foram encontrados nas evidências coletadas. Uma ausência é um ponto para revisão, não prova de erro.
- **Rubrica humana** deve receber notas de 0 (não atende), 1 (atende parcialmente) ou 2 (atende completamente).

## 1. fluxo_computadores_desktops

| Identificação | Valor |
| --- | --- |
| Abordagem | structured_context |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/structured_context_qwen25coder_demowebshop20_20260727_01/fluxo_computadores_desktops.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/tmp/qwen-demowebshop20-inputs/prompts/fluxo_computadores_desktops.structured_context.prompt.md` |

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
| Locators semânticos | 1 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demowebshop.tricentis.com/`

**Textos extraídos dos locators:**

- `Digital downloads`
- `h1`

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 3504 caracteres; 35 linhas |
| Estado da execução | passou |
| Duração | 3.991 s |
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

## 2. suite_adicionar_dois_produtos_carrinho

| Identificação | Valor |
| --- | --- |
| Abordagem | structured_context |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/structured_context_qwen25coder_demowebshop20_20260727_01/suite_adicionar_dois_produtos_carrinho.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/tmp/qwen-demowebshop20-inputs/prompts/suite_adicionar_dois_produtos_carrinho.structured_context.prompt.md` |

### Leitura rápida

- ✅ Estrutura mínima do Playwright reconhecida.
- ✅ O teste contém asserção.
- ✅ Não usa espera fixa.
- **Risco estimado dos seletores:** baixo.
- **Conformidade com o grafo:** não analisada nesta execução.

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

- `https://demowebshop.tricentis.com/computing-and-internet`
- `https://demowebshop.tricentis.com/fiction`
- `https://demowebshop.tricentis.com/cart`

**Textos extraídos dos locators:**

- `Fiction`
- `Shopping cart`
- `Computing and Internet`

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 4274 caracteres; 51 linhas |
| Estado da execução | falhou |
| Duração | 21.565 s |
| Tipo de erro | assertion_failure |
| Mensagem | Error: expect(locator).toBeVisible() failed Locator: getByText('Computing and Internet') Expected: visible Timeout: 7000ms Error: element(s) not found Call log: - Expect "toBeVisible" with timeout 7000ms - waiting for getByText('Computing and Internet') 22 \| test('Verificar itens no carrinho', async ({ page }) => { 23 \| await page.goto('https://demowebshop.tricentis.com/cart'); > 24 \| await expect(page.getByText("Computing and Internet")).toBeVisible(); \| ^ 25 \| await expect(page.getByText("Fic… |

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
| Abordagem | structured_context |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/structured_context_qwen25coder_demowebshop20_20260727_01/suite_atualizar_quantidade_carrinho.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/tmp/qwen-demowebshop20-inputs/prompts/suite_atualizar_quantidade_carrinho.structured_context.prompt.md` |

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
| Ações de usuário | 4 | cliques, preenchimentos e ações similares |
| Locators | 7 | total identificado estaticamente |
| Locators semânticos | 1 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demowebshop.tricentis.com/computing-and-internet`

**Textos extraídos dos locators:**

- `Shopping cart`

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 4037 caracteres; 44 linhas |
| Estado da execução | falhou |
| Duração | 10.132 s |
| Tipo de erro | assertion_failure |
| Mensagem | Error: expect(page).toHaveURL(expected) failed Expected: "https://demowebshop.tricentis.com/cart" Received: "https://demowebshop.tricentis.com/computing-and-internet" Timeout: 7000ms Call log: - Expect "toHaveURL" with timeout 7000ms 17 × unexpected value "https://demowebshop.tricentis.com/computing-and-internet" 6 \| await page.goto('https://demowebshop.tricentis.com/computing-and-internet'); 7 \| await page.locator("[id=\"add-to-cart-button-13\"]").click(); > 8 \| await expect(page).toHaveURL('h… |

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
| Abordagem | structured_context |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/structured_context_qwen25coder_demowebshop20_20260727_01/suite_busca_sem_resultados.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/tmp/qwen-demowebshop20-inputs/prompts/suite_busca_sem_resultados.structured_context.prompt.md` |

### Leitura rápida

- ✅ Estrutura mínima do Playwright reconhecida.
- ✅ O teste contém asserção.
- ✅ Não usa espera fixa.
- **Risco estimado dos seletores:** baixo.
- **Conformidade com o grafo:** não analisada nesta execução.

### Estrutura e seletores

| Métrica | Resultado | Leitura |
| --- | --- | --- |
| Importa `@playwright/test` | sim | necessário para execução |
| Possui bloco `test(...)` | sim | estrutura do caso de teste |
| Possui `expect(...)` | sim | indício de verificação do resultado |
| Ações de usuário | 2 | cliques, preenchimentos e ações similares |
| Locators | 3 | total identificado estaticamente |
| Locators semânticos | 2 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demowebshop.tricentis.com/`

**Textos extraídos dos locators:**

- `Search`
- `No products were found that matched your criteria!`

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 3690 caracteres; 38 linhas |
| Estado da execução | falhou |
| Duração | 15.735 s |
| Tipo de erro | assertion_failure |
| Mensagem | Error: expect(locator).toBeVisible() failed Locator: getByText('No products were found that matched your criteria!') Expected: visible Timeout: 7000ms Error: element(s) not found Call log: - Expect "toBeVisible" with timeout 7000ms - waiting for getByText('No products were found that matched your criteria!') 17 \| // Verificação de que não há produtos correspondentes 18 \| const noResultsMessage = page.getByText('No products were found that matched your criteria!'); > 19 \| await expect(noResultsM… |

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
| Abordagem | structured_context |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/structured_context_qwen25coder_demowebshop20_20260727_01/suite_cadastro_campos_obrigatorios.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/tmp/qwen-demowebshop20-inputs/prompts/suite_cadastro_campos_obrigatorios.structured_context.prompt.md` |

### Leitura rápida

- ✅ Estrutura mínima do Playwright reconhecida.
- ✅ O teste contém asserção.
- ✅ Não usa espera fixa.
- **Risco estimado dos seletores:** baixo.
- **Conformidade com o grafo:** não analisada nesta execução.

### Estrutura e seletores

| Métrica | Resultado | Leitura |
| --- | --- | --- |
| Importa `@playwright/test` | sim | necessário para execução |
| Possui bloco `test(...)` | sim | estrutura do caso de teste |
| Possui `expect(...)` | sim | indício de verificação do resultado |
| Ações de usuário | 6 | cliques, preenchimentos e ações similares |
| Locators | 11 | total identificado estaticamente |
| Locators semânticos | 10 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demowebshop.tricentis.com/`

**Textos extraídos dos locators:**

- `Register`
- `First name:`
- `Last name:`
- `Email:`
- `Password:`
- `First name is required`
- `Last name is required`
- `Email is required`
- `Password is required`
- `Confirm password is required`

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 4875 caracteres; 58 linhas |
| Estado da execução | falhou |
| Duração | 4.072 s |
| Tipo de erro | selector_ambiguity |
| Mensagem | Error: expect(locator).toBeVisible() failed Locator: getByText('Password is required') Expected: visible Error: strict mode violation: getByText('Password is required') resolved to 2 elements: 1) <span class="" for="Password">Password is required.</span> aka getByText('Password is required.').first() 2) <span class="" for="ConfirmPassword">Password is required.</span> aka getByText('Password is required.').nth(1) Call log: - Expect "toBeVisible" with timeout 7000ms - waiting for getByText('Pass… |

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
| Abordagem | structured_context |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/structured_context_qwen25coder_demowebshop20_20260727_01/suite_cadastro_confirmacao_senha.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/tmp/qwen-demowebshop20-inputs/prompts/suite_cadastro_confirmacao_senha.structured_context.prompt.md` |

### Leitura rápida

- ✅ Estrutura mínima do Playwright reconhecida.
- ✅ O teste contém asserção.
- ✅ Não usa espera fixa.
- **Risco estimado dos seletores:** baixo.
- **Conformidade com o grafo:** não analisada nesta execução.

### Estrutura e seletores

| Métrica | Resultado | Leitura |
| --- | --- | --- |
| Importa `@playwright/test` | sim | necessário para execução |
| Possui bloco `test(...)` | sim | estrutura do caso de teste |
| Possui `expect(...)` | sim | indício de verificação do resultado |
| Ações de usuário | 7 | cliques, preenchimentos e ações similares |
| Locators | 8 | total identificado estaticamente |
| Locators semânticos | 7 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demowebshop.tricentis.com/`

**Textos extraídos dos locators:**

- `Register`
- `First name:`
- `Last name:`
- `Email:`
- `Password:`
- `Confirm password:`
- `The specified passwords do not match.`

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 5285 caracteres; 64 linhas |
| Estado da execução | falhou |
| Duração | 11.087 s |
| Tipo de erro | assertion_failure |
| Mensagem | Error: expect(locator).toBeVisible() failed Locator: getByText('The specified passwords do not match.') Expected: visible Timeout: 7000ms Error: element(s) not found Call log: - Expect "toBeVisible" with timeout 7000ms - waiting for getByText('The specified passwords do not match.') 28 \| // Verifica se a mensagem de erro é exibida 29 \| expect(page).toHaveURL('https://demowebshop.tricentis.com/register'); > 30 \| await expect(page.getByText("The specified passwords do not match.")).toBeVisible();… |

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
| Abordagem | structured_context |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/structured_context_qwen25coder_demowebshop20_20260727_01/suite_cadastro_senha_curta.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/tmp/qwen-demowebshop20-inputs/prompts/suite_cadastro_senha_curta.structured_context.prompt.md` |

### Leitura rápida

- ✅ Estrutura mínima do Playwright reconhecida.
- ✅ O teste contém asserção.
- ✅ Não usa espera fixa.
- **Risco estimado dos seletores:** baixo.
- **Conformidade com o grafo:** não analisada nesta execução.

### Estrutura e seletores

| Métrica | Resultado | Leitura |
| --- | --- | --- |
| Importa `@playwright/test` | sim | necessário para execução |
| Possui bloco `test(...)` | sim | estrutura do caso de teste |
| Possui `expect(...)` | sim | indício de verificação do resultado |
| Ações de usuário | 7 | cliques, preenchimentos e ações similares |
| Locators | 7 | total identificado estaticamente |
| Locators semânticos | 6 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demowebshop.tricentis.com/`

**Textos extraídos dos locators:**

- `Register`
- `First name:`
- `Last name:`
- `Email:`
- `Password:`
- `Confirm password:`

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 5289 caracteres; 64 linhas |
| Estado da execução | falhou |
| Duração | 3.947 s |
| Tipo de erro | assertion_failure |
| Mensagem | Error: toHaveText can be only used with Locator object, was called with _Page <ref *1> _Page { _events: [Object: null prototype] { close: [Function: bound _handle] { listener: [Function (anonymous)] }, crash: [Function: bound _handle] { listener: [Function (anonymous)] } }, _eventsCount: 2, _maxListeners: 0, _pendingHandlers: Map(0) {}, _platform: { name: 'node', boxedStackPrefixes: [Function: boxedStackPrefixes], calculateSha1: [Function: calculateSha1], colors: { themes: {}, styles: [Object],… |

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
| Abordagem | structured_context |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/structured_context_qwen25coder_demowebshop20_20260727_01/suite_carrinho_inicialmente_vazio.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/tmp/qwen-demowebshop20-inputs/prompts/suite_carrinho_inicialmente_vazio.structured_context.prompt.md` |

### Leitura rápida

- ✅ Estrutura mínima do Playwright reconhecida.
- ✅ O teste contém asserção.
- ✅ Não usa espera fixa.
- **Risco estimado dos seletores:** baixo.
- **Conformidade com o grafo:** não analisada nesta execução.

### Estrutura e seletores

| Métrica | Resultado | Leitura |
| --- | --- | --- |
| Importa `@playwright/test` | sim | necessário para execução |
| Possui bloco `test(...)` | sim | estrutura do caso de teste |
| Possui `expect(...)` | sim | indício de verificação do resultado |
| Ações de usuário | 1 | cliques, preenchimentos e ações similares |
| Locators | 3 | total identificado estaticamente |
| Locators semânticos | 2 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demowebshop.tricentis.com/`

**Textos extraídos dos locators:**

- `Shopping cart`
- `h1`
- `No items added to your shopping cart`

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 3664 caracteres; 39 linhas |
| Estado da execução | falhou |
| Duração | 10.914 s |
| Tipo de erro | assertion_failure |
| Mensagem | Error: expect(locator).toBeVisible() failed Locator: getByRole('heading', { name: 'No items added to your shopping cart' }) Expected: visible Timeout: 7000ms Error: element(s) not found Call log: - Expect "toBeVisible" with timeout 7000ms - waiting for getByRole('heading', { name: 'No items added to your shopping cart' }) 10 \| // Etapa 2: Verificar que o carrinho está vazio 11 \| await expect(page.locator('h1')).toHaveText('Shopping cart'); > 12 \| await expect(page.getByRole('heading', { name: '… |

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
| Abordagem | structured_context |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/structured_context_qwen25coder_demowebshop20_20260727_01/suite_comparar_produtos.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/tmp/qwen-demowebshop20-inputs/prompts/suite_comparar_produtos.structured_context.prompt.md` |

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
| Ações de usuário | 3 | cliques, preenchimentos e ações similares |
| Locators | 7 | total identificado estaticamente |
| Locators semânticos | 3 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demowebshop.tricentis.com/computing-and-internet`
- `https://demowebshop.tricentis.com/fiction`

**Textos extraídos dos locators:**

- `Add to compare list`
- `Fiction`
- `Computing and Internet`
- `Clear list`

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 4020 caracteres; 45 linhas |
| Estado da execução | falhou |
| Duração | 11.577 s |
| Tipo de erro | assertion_failure |
| Mensagem | Error: expect(locator).toBeVisible() failed Locator: locator('.compare-products-page') Expected: visible Timeout: 7000ms Error: element(s) not found Call log: - Expect "toBeVisible" with timeout 7000ms - waiting for locator('.compare-products-page') 14 \| 15 \| // Etapa 3: Verifica se os produtos estão sendo comparados > 16 \| await expect(page.locator('.compare-products-page')).toBeVisible(); \| ^ 17 \| await expect(page.locator('.product-name', { hasText: 'Computing and Internet' })).toBeVisible()… |

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
| Abordagem | structured_context |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/structured_context_qwen25coder_demowebshop20_20260727_01/suite_enquete_sem_resposta.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/tmp/qwen-demowebshop20-inputs/prompts/suite_enquete_sem_resposta.structured_context.prompt.md` |

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
| Locators | 1 | total identificado estaticamente |
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
| Tamanho da entrada | 3563 caracteres; 38 linhas |
| Estado da execução | falhou |
| Duração | 10.385 s |
| Tipo de erro | assertion_failure |
| Mensagem | Error: expect(locator).toBeDisabled() failed Locator: locator('[id="vote-poll-1"]') Expected: disabled Received: enabled Timeout: 7000ms Call log: - Expect "toBeDisabled" with timeout 7000ms - waiting for locator('[id="vote-poll-1"]') 18 × locator resolved to <input value="Vote" type="button" id="vote-poll-1" class="button-2 vote-poll-button"/> - unexpected value "enabled" 9 \| await voteButton.click(); 10 \| > 11 \| await expect(voteButton).toBeDisabled(); \| ^ 12 \| await expect(page).toHaveText('… |

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
| Abordagem | structured_context |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/structured_context_qwen25coder_demowebshop20_20260727_01/suite_exibir_quatro_livros.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/tmp/qwen-demowebshop20-inputs/prompts/suite_exibir_quatro_livros.structured_context.prompt.md` |

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
| Locators semânticos | 1 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demowebshop.tricentis.com/`

**Textos extraídos dos locators:**

- `Books`

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 3619 caracteres; 41 linhas |
| Estado da execução | falhou |
| Duração | 10.754 s |
| Tipo de erro | assertion_failure |
| Mensagem | Error: expect(locator).toHaveCount(expected) failed Locator: locator('.product-item') Expected: 4 Received: 6 Timeout: 7000ms Call log: - Expect "toHaveCount" with timeout 7000ms - waiting for locator('.product-item') 18 × locator resolved to 6 elements - unexpected value "6" 10 \| // Etapa 3: Verify no more than four product items are displayed 11 \| const productItems = page.locator('.product-item'); > 12 \| await expect(productItems).toHaveCount(4); \| ^ 13 \| }); 14 \| }); 15 \| at /home/martinssp… |

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
| Abordagem | structured_context |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/structured_context_qwen25coder_demowebshop20_20260727_01/suite_filtrar_livros_abaixo_25.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/tmp/qwen-demowebshop20-inputs/prompts/suite_filtrar_livros_abaixo_25.structured_context.prompt.md` |

### Leitura rápida

- ✅ Estrutura mínima do Playwright reconhecida.
- ✅ O teste contém asserção.
- ✅ Não usa espera fixa.
- **Risco estimado dos seletores:** baixo.
- **Conformidade com o grafo:** não analisada nesta execução.

### Estrutura e seletores

| Métrica | Resultado | Leitura |
| --- | --- | --- |
| Importa `@playwright/test` | sim | necessário para execução |
| Possui bloco `test(...)` | sim | estrutura do caso de teste |
| Possui `expect(...)` | sim | indício de verificação do resultado |
| Ações de usuário | 2 | cliques, preenchimentos e ações similares |
| Locators | 4 | total identificado estaticamente |
| Locators semânticos | 3 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demowebshop.tricentis.com/`

**Textos extraídos dos locators:**

- `Books`
- `Under 25.00`
- `Add to cart`

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 3902 caracteres; 46 linhas |
| Estado da execução | falhou |
| Duração | 4.701 s |
| Tipo de erro | assertion_failure |
| Mensagem | Error: expect(received).toBeLessThan(expected) Expected: < 25 Received: NaN 16 \| for (let product of await products.all()) { 17 \| const priceText = await product.getByRole('button', { name: 'Add to cart' }).first().textContent(); > 18 \| expect(parseFloat(priceText.replace('$', ''))).toBeLessThan(25); \| ^ 19 \| } 20 \| }); 21 \| }); at /home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/structured_context_qwen25coder_demowebshop20_20260727_01/suite_filtr… |

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
| Abordagem | structured_context |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/structured_context_qwen25coder_demowebshop20_20260727_01/suite_navegar_cartoes_presente.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/tmp/qwen-demowebshop20-inputs/prompts/suite_navegar_cartoes_presente.structured_context.prompt.md` |

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
| Locators semânticos | 1 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demowebshop.tricentis.com/`

**Textos extraídos dos locators:**

- `Gift Cards`
- `h1`

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 3654 caracteres; 41 linhas |
| Estado da execução | falhou |
| Duração | 20.687 s |
| Tipo de erro | locator_timeout |
| Mensagem | TimeoutError: locator.click: Timeout 10000ms exceeded. Call log: - waiting for getByText('Gift Cards', { exact: true }).first() 8 \| 9 \| test('The user selects Gift Cards in the main category menu', async ({ page }) => { > 10 \| await page.getByText("Gift Cards", { exact: true }).first().click(); \| ^ 11 \| await expect(page).toHaveURL('https://demowebshop.tricentis.com/gift-cards'); 12 \| }); 13 \| at /home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/st… |

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
| Abordagem | structured_context |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/structured_context_qwen25coder_demowebshop20_20260727_01/suite_navegar_categoria_livros.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/tmp/qwen-demowebshop20-inputs/prompts/suite_navegar_categoria_livros.structured_context.prompt.md` |

### Leitura rápida

- ✅ Estrutura mínima do Playwright reconhecida.
- ✅ O teste contém asserção.
- ✅ Não usa espera fixa.
- **Risco estimado dos seletores:** baixo.
- **Conformidade com o grafo:** não analisada nesta execução.

### Estrutura e seletores

| Métrica | Resultado | Leitura |
| --- | --- | --- |
| Importa `@playwright/test` | sim | necessário para execução |
| Possui bloco `test(...)` | sim | estrutura do caso de teste |
| Possui `expect(...)` | sim | indício de verificação do resultado |
| Ações de usuário | 1 | cliques, preenchimentos e ações similares |
| Locators | 3 | total identificado estaticamente |
| Locators semânticos | 2 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demowebshop.tricentis.com/`

**Textos extraídos dos locators:**

- `Books`
- `h1`

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 3697 caracteres; 42 linhas |
| Estado da execução | falhou |
| Duração | 4.073 s |
| Tipo de erro | assertion_failure |
| Mensagem | Error: expect(page).toHaveURL(expected) failed Expected: "https://demowebshop.tricentis.com/books" Received: "" Call log: - Expect "toHaveURL" with timeout 7000ms 12 \| 13 \| // Verifica se foi redirecionado para a página de categorias de livros > 14 \| expect(page).toHaveURL('https://demowebshop.tricentis.com/books'); \| ^ 15 \| expect(page.locator('h1')).toHaveText('Books'); 16 \| 17 \| // Etapa 3: Confirma que os subcategorias estão disponíveis at /home/martinsspn/dissertacao_e2e_semantico/python_a… |

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
| Abordagem | structured_context |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/structured_context_qwen25coder_demowebshop20_20260727_01/suite_navegar_sobre_nos.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/tmp/qwen-demowebshop20-inputs/prompts/suite_navegar_sobre_nos.structured_context.prompt.md` |

### Leitura rápida

- ✅ Estrutura mínima do Playwright reconhecida.
- ✅ O teste contém asserção.
- ✅ Não usa espera fixa.
- **Risco estimado dos seletores:** baixo.
- **Conformidade com o grafo:** não analisada nesta execução.

### Estrutura e seletores

| Métrica | Resultado | Leitura |
| --- | --- | --- |
| Importa `@playwright/test` | sim | necessário para execução |
| Possui bloco `test(...)` | sim | estrutura do caso de teste |
| Possui `expect(...)` | sim | indício de verificação do resultado |
| Ações de usuário | 1 | cliques, preenchimentos e ações similares |
| Locators | 1 | total identificado estaticamente |
| Locators semânticos | 1 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demowebshop.tricentis.com/`

**Textos extraídos dos locators:**

- `About us`

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 3541 caracteres; 39 linhas |
| Estado da execução | passou |
| Duração | 3.914 s |
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

## 16. suite_ordenar_livros_por_preco

| Identificação | Valor |
| --- | --- |
| Abordagem | structured_context |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/structured_context_qwen25coder_demowebshop20_20260727_01/suite_ordenar_livros_por_preco.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/tmp/qwen-demowebshop20-inputs/prompts/suite_ordenar_livros_por_preco.structured_context.prompt.md` |

### Leitura rápida

- ✅ Estrutura mínima do Playwright reconhecida.
- ✅ O teste contém asserção.
- ✅ Não usa espera fixa.
- **Risco estimado dos seletores:** baixo.
- **Conformidade com o grafo:** não analisada nesta execução.

### Estrutura e seletores

| Métrica | Resultado | Leitura |
| --- | --- | --- |
| Importa `@playwright/test` | sim | necessário para execução |
| Possui bloco `test(...)` | sim | estrutura do caso de teste |
| Possui `expect(...)` | sim | indício de verificação do resultado |
| Ações de usuário | 2 | cliques, preenchimentos e ações similares |
| Locators | 3 | total identificado estaticamente |
| Locators semânticos | 2 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demowebshop.tricentis.com/`

**Textos extraídos dos locators:**

- `Books`
- `Sort by price: Low to High`

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 3663 caracteres; 41 linhas |
| Estado da execução | falhou |
| Duração | 14.127 s |
| Tipo de erro | locator_timeout |
| Mensagem | TimeoutError: locator.click: Timeout 10000ms exceeded. Call log: - waiting for getByRole('button', { name: 'Sort by price: Low to High' }) 9 \| 10 \| // Etapa 2: Seleciona a opção de ordenar por preço baixo para alto > 11 \| await page.getByRole('button', { name: 'Sort by price: Low to High' }).click(); \| ^ 12 \| 13 \| // Verifica se os livros estão em ordem crescente de preço 14 \| const prices = await page.locator('.product-box .price').allTextContents(); at /home/martinsspn/dissertacao_e2e_semanti… |

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
| Abordagem | structured_context |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/structured_context_qwen25coder_demowebshop20_20260727_01/suite_persistencia_carrinho_apos_login.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/tmp/qwen-demowebshop20-inputs/prompts/suite_persistencia_carrinho_apos_login.structured_context.prompt.md` |

### Leitura rápida

- ✅ Estrutura mínima do Playwright reconhecida.
- ✅ O teste contém asserção.
- ✅ Não usa espera fixa.
- **Risco estimado dos seletores:** baixo.
- **Conformidade com o grafo:** não analisada nesta execução.

### Estrutura e seletores

| Métrica | Resultado | Leitura |
| --- | --- | --- |
| Importa `@playwright/test` | sim | necessário para execução |
| Possui bloco `test(...)` | sim | estrutura do caso de teste |
| Possui `expect(...)` | sim | indício de verificação do resultado |
| Ações de usuário | 12 | cliques, preenchimentos e ações similares |
| Locators | 6 | total identificado estaticamente |
| Locators semânticos | 6 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demowebshop.tricentis.com/`

**Textos extraídos dos locators:**

- `Log in`
- `Computing and Internet`
- `Shopping cart`

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 4097 caracteres; 48 linhas |
| Estado da execução | falhou |
| Duração | 14.075 s |
| Tipo de erro | locator_timeout |
| Mensagem | TimeoutError: page.click: Timeout 10000ms exceeded. Call log: - waiting for locator('button[type="submit"]') 8 \| await page.fill('input[name="Email"]', process.env.TEST_EMAIL); 9 \| await page.fill('input[name="Password"]', process.env.TEST_PASSWORD); > 10 \| await page.click('button[type="submit"]'); \| ^ 11 \| await expect(page).toHaveURL('https://demowebshop.tricentis.com/'); 12 \| 13 \| // Etapa 2: Adicionar produto ao carrinho at /home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt… |

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
| Abordagem | structured_context |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/structured_context_qwen25coder_demowebshop20_20260727_01/suite_produtos_visualizados_recentemente.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/tmp/qwen-demowebshop20-inputs/prompts/suite_produtos_visualizados_recentemente.structured_context.prompt.md` |

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
| Locators semânticos | 1 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demowebshop.tricentis.com/blue-jeans`

**Textos extraídos dos locators:**

- `Recently viewed products`

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 3833 caracteres; 39 linhas |
| Estado da execução | falhou |
| Duração | 4.105 s |
| Tipo de erro | assertion_failure |
| Mensagem | Error: expect(received).toContain(expected) // indexOf Matcher error: received value must not be null nor undefined Received has value: undefined 14 \| const productItems = await page.locator('.product-item').allInnerTexts(); 15 \| expect(productItems[0]).toContain('Blue Jeans'); > 16 \| expect(productItems[1]).toContain('Fiction'); \| ^ 17 \| }); 18 \| }); 19 \| at /home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/structured_context_qwen25coder_demowebsh… |

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
| Abordagem | structured_context |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/structured_context_qwen25coder_demowebshop20_20260727_01/suite_visualizacao_livros_em_lista.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/tmp/qwen-demowebshop20-inputs/prompts/suite_visualizacao_livros_em_lista.structured_context.prompt.md` |

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
| Locators semânticos | 1 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demowebshop.tricentis.com/`

**Textos extraídos dos locators:**

- `Books`
- `List`

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 3651 caracteres; 41 linhas |
| Estado da execução | falhou |
| Duração | 4.146 s |
| Tipo de erro | selector_ambiguity |
| Mensagem | Error: expect(locator).toBeVisible() failed Locator: locator('.product-item') Expected: visible Error: strict mode violation: locator('.product-item') resolved to 6 elements: 1) <div data-productid="13" class="product-item">…</div> aka locator('.product-item').first() 2) <div data-productid="79" class="product-item">…</div> aka locator('div:nth-child(2) > .product-item') 3) <div data-productid="45" class="product-item">…</div> aka locator('div:nth-child(3) > .product-item') 4) <div data-product… |

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
| Abordagem | structured_context |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/structured_context_qwen25coder_demowebshop20_20260727_01/user_registration_book_purchase.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/tmp/qwen-demowebshop20-inputs/prompts/user_registration_book_purchase.structured_context.prompt.md` |

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

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 7893 caracteres; 118 linhas |
| Estado da execução | falhou |
| Duração | 8.248 s |
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
