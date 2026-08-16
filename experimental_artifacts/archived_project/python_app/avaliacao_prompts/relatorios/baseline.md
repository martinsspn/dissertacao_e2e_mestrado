# Relatório auxiliar de avaliação dos testes E2E

> Este relatório é uma ferramenta não oficial de apoio à análise. As métricas automáticas são evidências; não constituem, isoladamente, uma avaliação de correção semântica.

## Visão geral

| Indicador | Resultado |
| --- | --- |
| Testes analisados | 12 |
| Com estrutura mínima reconhecida | 12 de 12 (100,0%) |
| Com pelo menos uma asserção | 12 de 12 (100,0%) |
| Com espera fixa `waitForTimeout` | 0 de 12 (0,0%) |
| Risco dos seletores | baixo: 6; médio: 6; alto: 0; não aplicável: 0 |
| Resultado da execução | passou: 7; falhou: 5 |
| Tamanho médio da entrada da LLM | 386 caracteres; 1,0 linhas |
| Cobertura média de URLs no grafo | 100,0% |
| Cobertura média de textos no grafo | 88,2% |

## Como interpretar

- **Estrutura mínima** verifica apenas a presença de importação do Playwright, bloco de teste e asserção.
- **Risco dos seletores** é uma heurística: seletores semânticos reduzem o risco; XPath e esperas fixas elevam o risco.
- **Cobertura pelo grafo** indica se URLs e textos de locators foram encontrados nas evidências coletadas. Uma ausência é um ponto para revisão, não prova de erro.
- **Rubrica humana** deve receber notas de 0 (não atende), 1 (atende parcialmente) ou 2 (atende completamente).

## 1. teste_adicionar_carrinho_baseline

| Identificação | Valor |
| --- | --- |
| Abordagem | baseline |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline/teste_adicionar_carrinho_baseline.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/specs/suite_adicionar_carrinho.txt` |

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
| Locators | 11 | total identificado estaticamente |
| Locators semânticos | 5 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demowebshop.tricentis.com/`

**Textos extraídos dos locators:**

- `input.search-box-button`
- `Blue Jeans`
- `Add to cart`

### Pontos para revisão contra o grafo

**URLs não encontradas:**

- _nenhuma_

**Textos de locators não encontrados:**

- _nenhum_

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 370 caracteres; 1 linhas |
| Estado da execução | falhou |
| Duração | 4.586 s |
| Tipo de erro | selector_ambiguity |
| Mensagem | Error: locator.click: Error: strict mode violation: locator('input[value="Add to cart"]') resolved to 4 elements: 1) <input type="button" value="Add to cart" data-productid="36" id="add-to-cart-button-36" class="button-1 add-to-cart-button" onclick="AjaxCart.addproducttocart_details('/addproducttocart/details/36/1', '#product-details-form');return false;"/> aka locator('#add-to-cart-button-36') 2) <input type="button" value="Add to cart" class="button-2 product-box-add-to-cart-button" onclick="… |

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

## 2. teste_buscar_blue_jeans_baseline

| Identificação | Valor |
| --- | --- |
| Abordagem | baseline |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline/teste_buscar_blue_jeans_baseline.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/specs/suite_busca_blue_jeans.txt` |

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
| Locators | 6 | total identificado estaticamente |
| Locators semânticos | 4 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demowebshop.tricentis.com/`

**Textos extraídos dos locators:**

- `input.search-box-button`

### Pontos para revisão contra o grafo

**URLs não encontradas:**

- _nenhuma_

**Textos de locators não encontrados:**

- _nenhum_

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 279 caracteres; 1 linhas |
| Estado da execução | passou |
| Duração | 5.041 s |
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

## 3. teste_checkout_blue_jeans_baseline

| Identificação | Valor |
| --- | --- |
| Abordagem | baseline |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline/teste_checkout_blue_jeans_baseline.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/specs/suite_checkout_blue_jeans.txt` |

### Leitura rápida

- ✅ Estrutura mínima do Playwright reconhecida.
- ✅ O teste contém asserção.
- ✅ Não usa espera fixa.
- **Risco estimado dos seletores:** médio.
- **URLs fundamentadas no grafo:** 100,0%.
- **Textos de locators fundamentados no grafo:** 80,0%.

### Estrutura e seletores

| Métrica | Resultado | Leitura |
| --- | --- | --- |
| Importa `@playwright/test` | sim | necessário para execução |
| Possui bloco `test(...)` | sim | estrutura do caso de teste |
| Possui `expect(...)` | sim | indício de verificação do resultado |
| Ações de usuário | 31 | cliques, preenchimentos e ações similares |
| Locators | 36 | total identificado estaticamente |
| Locators semânticos | 9 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demowebshop.tricentis.com/`

**Textos extraídos dos locators:**

- `Log in`
- `input.login-button`
- `input.search-box-button`
- `Add to cart`
- `Your order has been successfully processed!`

### Pontos para revisão contra o grafo

**URLs não encontradas:**

- _nenhuma_

**Textos de locators não encontrados:**

- `Your order has been successfully processed!`

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 794 caracteres; 1 linhas |
| Estado da execução | falhou |
| Duração | 19.026 s |
| Tipo de erro | locator_timeout |
| Mensagem | TimeoutError: locator.click: Timeout 10000ms exceeded. Call log: - waiting for locator('#shipping-buttons-container input') - locator resolved to <input type="button" title="Continue" value="Continue" onclick="Shipping.save()" class="button-1 new-address-next-step-button"/> - attempting click action 2 × waiting for element to be visible, enabled and stable - element is not visible - retrying click action - waiting 20ms 2 × waiting for element to be visible, enabled and stable - element is not v… |

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

## 4. teste_configurar_desktop_baseline

| Identificação | Valor |
| --- | --- |
| Abordagem | baseline |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline/teste_configurar_desktop_baseline.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/specs/suite_configurar_desktop.txt` |

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
| Ações de usuário | 9 | cliques, preenchimentos e ações similares |
| Locators | 18 | total identificado estaticamente |
| Locators semânticos | 13 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demowebshop.tricentis.com/`

**Textos extraídos dos locators:**

- `Computers`
- `Desktops`
- `Fast`
- `4 GB`
- `400 GB`
- `Office Suite`
- `Add to cart`

### Pontos para revisão contra o grafo

**URLs não encontradas:**

- _nenhuma_

**Textos de locators não encontrados:**

- _nenhum_

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 474 caracteres; 1 linhas |
| Estado da execução | falhou |
| Duração | 17.018 s |
| Tipo de erro | locator_timeout |
| Mensagem | TimeoutError: locator.check: Timeout 10000ms exceeded. Call log: - waiting for getByLabel('Fast', { exact: true }) 45 \| ).toBeVisible(); 46 \| > 47 \| await page.getByLabel('Fast', { exact: true }).check(); \| ^ 48 \| await page.getByLabel('4 GB', { exact: true }).check(); 49 \| await page.getByLabel('400 GB', { exact: true }).check(); 50 \| await page.getByLabel('Office Suite', { exact: true }).check(); at /home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tes… |

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

## 5. teste_detalhes_fiction_baseline

| Identificação | Valor |
| --- | --- |
| Abordagem | baseline |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline/teste_detalhes_fiction_baseline.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/specs/suite_detalhes_fiction.txt` |

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
| Locators | 7 | total identificado estaticamente |
| Locators semânticos | 3 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demowebshop.tricentis.com/`

**Textos extraídos dos locators:**

- `input.search-box-button`

### Pontos para revisão contra o grafo

**URLs não encontradas:**

- _nenhuma_

**Textos de locators não encontrados:**

- _nenhum_

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 284 caracteres; 1 linhas |
| Estado da execução | passou |
| Duração | 4.952 s |
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

## 6. teste_limpar_carrinho_baseline

| Identificação | Valor |
| --- | --- |
| Abordagem | baseline |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline/teste_limpar_carrinho_baseline.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/specs/suite_limpar_carrinho.txt` |

### Leitura rápida

- ✅ Estrutura mínima do Playwright reconhecida.
- ✅ O teste contém asserção.
- ✅ Não usa espera fixa.
- **Risco estimado dos seletores:** médio.
- **URLs fundamentadas no grafo:** 100,0%.
- **Textos de locators fundamentados no grafo:** 60,0%.

### Estrutura e seletores

| Métrica | Resultado | Leitura |
| --- | --- | --- |
| Importa `@playwright/test` | sim | necessário para execução |
| Possui bloco `test(...)` | sim | estrutura do caso de teste |
| Possui `expect(...)` | sim | indício de verificação do resultado |
| Ações de usuário | 7 | cliques, preenchimentos e ações similares |
| Locators | 14 | total identificado estaticamente |
| Locators semânticos | 6 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demowebshop.tricentis.com/`

**Textos extraídos dos locators:**

- `input.search-box-button`
- `Add to cart`
- `removefromcart`
- `updatecart`
- `Your Shopping Cart is empty!`

### Pontos para revisão contra o grafo

**URLs não encontradas:**

- _nenhuma_

**Textos de locators não encontrados:**

- `removefromcart`
- `updatecart`

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 260 caracteres; 1 linhas |
| Estado da execução | passou |
| Duração | 5.765 s |
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

## 7. teste_limpar_wishlist_baseline

| Identificação | Valor |
| --- | --- |
| Abordagem | baseline |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline/teste_limpar_wishlist_baseline.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/specs/suite_limpar_wishlist.txt` |

### Leitura rápida

- ✅ Estrutura mínima do Playwright reconhecida.
- ✅ O teste contém asserção.
- ✅ Não usa espera fixa.
- **Risco estimado dos seletores:** médio.
- **URLs fundamentadas no grafo:** 100,0%.
- **Textos de locators fundamentados no grafo:** 71,4%.

### Estrutura e seletores

| Métrica | Resultado | Leitura |
| --- | --- | --- |
| Importa `@playwright/test` | sim | necessário para execução |
| Possui bloco `test(...)` | sim | estrutura do caso de teste |
| Possui `expect(...)` | sim | indício de verificação do resultado |
| Ações de usuário | 11 | cliques, preenchimentos e ações similares |
| Locators | 18 | total identificado estaticamente |
| Locators semânticos | 8 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demowebshop.tricentis.com/`

**Textos extraídos dos locators:**

- `Log in`
- `input.login-button`
- `input.search-box-button`
- `Add to wishlist`
- `removefromcart`
- `updatecart`
- `The wishlist is empty!`

### Pontos para revisão contra o grafo

**URLs não encontradas:**

- _nenhuma_

**Textos de locators não encontrados:**

- `removefromcart`
- `updatecart`

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 350 caracteres; 1 linhas |
| Estado da execução | falhou |
| Duração | 8.977 s |
| Tipo de erro | selector_ambiguity |
| Mensagem | Error: locator.click: Error: strict mode violation: locator('input[value="Add to wishlist"]') resolved to 2 elements: 1) <input type="button" data-productid="18" value="Add to wishlist" id="add-to-wishlist-button-18" class="button-2 add-to-wishlist-button" onclick="AjaxCart.addproducttocart_details('/addproducttocart/details/18/2', '#product-details-form');return false;"/> aka locator('#add-to-wishlist-button-18') 2) <input type="button" data-productid="19" value="Add to wishlist" id="add-to-wi… |

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

## 8. teste_login_invalido_baseline

| Identificação | Valor |
| --- | --- |
| Abordagem | baseline |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline/teste_login_invalido_baseline.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/specs/suite_login_invalido.txt` |

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
| Locators | 9 | total identificado estaticamente |
| Locators semânticos | 6 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demowebshop.tricentis.com/`

**Textos extraídos dos locators:**

- `Log in`
- `Welcome, Please Sign In!`
- `input.login-button`
- `Login was unsuccessful. Please correct the errors and try again.`
- `The credentials provided are incorrect`

### Pontos para revisão contra o grafo

**URLs não encontradas:**

- _nenhuma_

**Textos de locators não encontrados:**

- `The credentials provided are incorrect`

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 354 caracteres; 1 linhas |
| Estado da execução | passou |
| Duração | 3.827 s |
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

## 9. teste_login_valido_baseline

| Identificação | Valor |
| --- | --- |
| Abordagem | baseline |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline/teste_login_valido_baseline.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/specs/suite_login_valido.txt` |

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
| Locators | 8 | total identificado estaticamente |
| Locators semânticos | 5 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demowebshop.tricentis.com/`

**Textos extraídos dos locators:**

- `Log in`
- `input.login-button`

### Pontos para revisão contra o grafo

**URLs não encontradas:**

- _nenhuma_

**Textos de locators não encontrados:**

- _nenhum_

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 298 caracteres; 1 linhas |
| Estado da execução | passou |
| Duração | 4.414 s |
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

## 10. teste_logout_baseline

| Identificação | Valor |
| --- | --- |
| Abordagem | baseline |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline/teste_logout_baseline.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/specs/suite_logout.txt` |

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
| Ações de usuário | 5 | cliques, preenchimentos e ações similares |
| Locators | 10 | total identificado estaticamente |
| Locators semânticos | 7 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demowebshop.tricentis.com/`

**Textos extraídos dos locators:**

- `Log in`
- `input.login-button`
- `Log out`

### Pontos para revisão contra o grafo

**URLs não encontradas:**

- _nenhuma_

**Textos de locators não encontrados:**

- _nenhum_

### Prompt e execução

| Item | Resultado |
| --- | --- |
| Tamanho da entrada | 216 caracteres; 1 linhas |
| Estado da execução | passou |
| Duração | 5.267 s |
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

## 11. teste_registro_usuario_baseline

| Identificação | Valor |
| --- | --- |
| Abordagem | baseline |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline/teste_registro_usuario_baseline.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/specs/suite_registro_usuario.txt` |

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
| Ações de usuário | 9 | cliques, preenchimentos e ações similares |
| Locators | 14 | total identificado estaticamente |
| Locators semânticos | 7 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demowebshop.tricentis.com/`

**Textos extraídos dos locators:**

- `Register`
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
| Tamanho da entrada | 515 caracteres; 1 linhas |
| Estado da execução | passou |
| Duração | 6.437 s |
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

## 12. teste_wishlist_baseline

| Identificação | Valor |
| --- | --- |
| Abordagem | baseline |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline/teste_wishlist_baseline.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/specs/suite_adicionar_wishlist.txt` |

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
| Ações de usuário | 9 | cliques, preenchimentos e ações similares |
| Locators | 13 | total identificado estaticamente |
| Locators semânticos | 8 | role, label, texto, placeholder etc. |
| XPath | 0 | valores maiores que zero merecem revisão |
| Espera fixa | não | ausente |

### Evidências encontradas no código

**URLs usadas em `page.goto`:**

- `https://demowebshop.tricentis.com/`

**Textos extraídos dos locators:**

- `Log in`
- `Search store`
- `Search`
- `Camera`
- `Add to wishlist`

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
| Duração | 14.513 s |
| Tipo de erro | locator_timeout |
| Mensagem | TimeoutError: locator.fill: Timeout 10000ms exceeded. Call log: - waiting for getByRole('textbox', { name: 'Search store' }) 22 \| 23 \| const searchField = page.getByRole('textbox', { name: 'Search store' }); > 24 \| await searchField.fill('Camera'); \| ^ 25 \| await page.getByRole('button', { name: 'Search' }).click(); 26 \| 27 \| const cameraProduct = page at /home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline/teste_wishlist_baseline.spec.ts:24:… |

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
