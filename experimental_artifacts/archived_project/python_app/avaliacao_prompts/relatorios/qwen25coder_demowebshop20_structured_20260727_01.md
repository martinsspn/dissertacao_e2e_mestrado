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
| Resultado da execução | não executado: 20 |
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
