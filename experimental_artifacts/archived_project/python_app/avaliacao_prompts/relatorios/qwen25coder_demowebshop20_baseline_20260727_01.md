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
| Resultado da execução | não executado: 20 |
| Tamanho médio da entrada da LLM | 317 caracteres; 1,0 linhas |
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
| Entrada da LLM | não localizada/informada |

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
| Tamanho da entrada | não disponível |
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
| Abordagem | baseline |
| Arquivo de teste | `/home/martinsspn/dissertacao_e2e_semantico/python_app/teste_prompt_e2e_semantico/generated_tests/baseline_qwen25coder_demowebshop20_20260727_01/user_registration_book_purchase.spec.ts` |
| URL base | https://demowebshop.tricentis.com/ |
| Entrada da LLM | não localizada/informada |

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
| Tamanho da entrada | não disponível |
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
