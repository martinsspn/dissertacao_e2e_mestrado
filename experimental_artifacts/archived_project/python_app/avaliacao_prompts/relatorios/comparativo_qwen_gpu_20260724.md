# Análise comparativa — baseline versus contexto estruturado

## Escopo e controle experimental

Foram avaliados os 14 pares gerados pelo `qwen2.5-coder:7b` na execução
`ollama_qwen25coder_gpu_20260724_01`.

- Cada condição foi executada em um processo Playwright separado.
- Cada teste recebeu um contexto de navegador novo.
- As duas condições usaram o mesmo Chromium, a mesma URL base, os mesmos
  timeouts e a mesma conta sintética válida.
- Os resultados foram gravados em arquivos JSON separados. Não houve reuso de
  carrinho, wishlist, cookies ou `storageState` entre os testes ou condições.
- A rubrica humana predefinida em `docs/protocolo_avaliacao_hibrida.md` foi
  aplicada por um avaliador, com notas de 0 a 2. Portanto, essas notas devem ser
  tratadas como julgamento auditável, não como verdade automática.

## Resultado principal

| Métrica | Baseline | Contexto estruturado | Leitura |
| --- | ---: | ---: | --- |
| Arquivos carregados pelo Playwright | 14/14 | 14/14 | Empate na estrutura mínima |
| Testes aprovados | 0/14 | 0/14 | Nenhuma condição produziu teste pronto para uso |
| Falhas | 14/14 | 10/14 | O número menor no estruturado não é melhora: há mais 4 erros de sintaxe em runtime |
| Erros de sintaxe em runtime | 0/14 | 4/14 | Regressão causada por seletores mal traduzidos |
| Falhas classificadas como `generated_test_failure` | 14/14 | 14/14 | Não houve evidência de falha da aplicação ou do ambiente |
| Duração total da suíte | 185,46 s | 149,47 s | O estruturado terminou antes porque vários casos falharam cedo |
| Cobertura média de URLs no grafo | 60,7% | 100,0% | Ganho claro de fundamentação de rotas |
| Cobertura média de textos no grafo | 91,1% | 85,1% | O ganho de rotas não se repetiu para textos |
| Nota humana média | 4,43/12 | 6,00/12 | +1,57 ponto; 36,9% para 50,0% |
| Testes com `expect(...)` | 14/14 | 14/14 | Presença não implica qualidade |
| Asserções no código | 29 | 70 | O contexto induziu mais verificações |
| Asserções sem `await` | 9/29 | 13/70 | 31,0% versus 18,6% |
| Asserções vazias | 2 | 0 | Pequeno ganho do estruturado |
| Arquivos com URL de outro domínio | 4/14 | 0/14 | O contexto eliminou esta alucinação |
| Arquivos com vazamento da notação do contexto | 0/14 | 7/14 | 24 ocorrências no estruturado |

O contexto estruturado melhorou a escolha do domínio, das rotas e de alguns ids,
mas não melhorou a executabilidade final. O benefício semântico foi neutralizado
pela incapacidade do modelo de traduzir a representação intermediária do grafo
para a API do Playwright.

## Execução por especificação

| Especificação | Baseline | Contexto estruturado |
| --- | --- | --- |
| `fluxo_computadores_desktops` | Falhou: `.digital-item` inexistente | Falhou: link `Digital downloads` ambíguo (3 elementos) |
| `suite_adicionar_carrinho` | Falhou: `example.com` e `data-test` inventados | Erro de sintaxe: `role_name:Search` usado como CSS |
| `suite_adicionar_wishlist` | Falhou: login e dashboard inventados | Erro de sintaxe: `role_name:Search` usado como CSS |
| `suite_busca_blue_jeans` | Falhou: domínio e campo de busca inventados | Falhou: `role=Search` não localiza o botão |
| `suite_checkout_blue_jeans` | Falhou: domínio e login inventados | Erro de sintaxe: `role_name:Search` usado como CSS |
| `suite_configurar_desktop` | Falhou: link escolhido não estava visível; controles seguintes também são inventados | Falhou: `#product_attribute_1` não existe |
| `suite_detalhes_fiction` | Falhou: domínio e campo de busca inventados | Falhou: `role=Search` não localiza o botão |
| `suite_limpar_carrinho` | Falhou: rota `/products` e controles inventados | Falhou: `removefromcart_36` não existe |
| `suite_limpar_wishlist` | Falhou em runtime: função de autenticação indefinida | Falhou: não prepara a wishlist e não encontra `Camera` |
| `suite_login_invalido` | Falhou: `#login-button` não existe | Falhou: mensagem real não possui id `#message-error` |
| `suite_login_valido` | Falhou: procura `button[type=submit]`, mas o controle real é um `input` | Falhou depois de autenticar: espera a rota inexistente `/Account/Manage` |
| `suite_logout` | Falhou: interface de login/logout inventada | Falhou: tenta preencher login na página inicial sem navegar ao formulário |
| `suite_registro_usuario` | Falhou depois de registrar: usa Log out no lugar de Continue | Erro de sintaxe: `text:Register` usado como CSS |
| `user_registration_book_purchase` | Falhou: seletor genérico de submit não encontra o Register | Falhou: engine inexistente `tag=...` |

Todos os testes chegaram a ser coletados e iniciados pelo Playwright. Assim, os
erros acima são de geração do teste, não de instalação do navegador, rede ou
indisponibilidade do site.

## Conformidade com a especificação

| Critério da rubrica (máximo 2) | Média baseline | Média estruturado | Diferença |
| --- | ---: | ---: | ---: |
| Fluxo correto | 1,79 | 1,29 | -0,50 |
| Alvo correto | 0,43 | 0,71 | +0,28 |
| Asserção correta | 0,93 | 1,07 | +0,14 |
| Aderência ao grafo | 0,71 | 1,93 | +1,22 |
| Robustez prática | 0,29 | 0,36 | +0,07 |
| Utilidade geral | 0,29 | 0,64 | +0,35 |
| **Total por teste (máximo 12)** | **4,43** | **6,00** | **+1,57** |

A maior melhora está concentrada em aderência ao grafo. A nota de fluxo diminui
porque vários testes estruturados omitiram pré-condições ou etapas explícitas:
autenticação, preparação da wishlist, abertura do resultado de busca, confirmação
da notificação e `Continue` após registro. Portanto, maior cobertura do grafo não
equivale a maior conformidade com a especificação.

Os casos estruturados mais próximos de uso foram `suite_login_invalido` (9/12) e
`suite_limpar_carrinho` (8/12). Ainda assim, ambos falharam por seletores
incorretos. No baseline, `suite_login_invalido` também atingiu 9/12, mas falhou
por um id de botão inexistente.

## Qualidade das asserções

O avaliador automático anterior media apenas se havia pelo menos um
`expect(...)`; isso produziu 100% nas duas condições e ocultou problemas:

- o baseline contém 9 asserções sem `await` e duas chamadas vazias, como
  `expect(await page.isVisible(...));`, que não verificam valor algum;
- o estruturado contém 13 asserções sem `await`, sobretudo `toHaveURL`,
  `textContent()` e verificações do fluxo de registro;
- o estruturado aumentou de 29 para 70 asserções, mas muitas verificam
  transições incorretas, como busca redirecionar diretamente ao produto e login
  redirecionar para `/Account/Manage`;
- presença, quantidade e cobertura textual de asserções não substituem a
  avaliação do oráculo esperado na especificação.

## Métrica adicional: custo e tempo de geração

Tempo e custo de geração estavam prometidos no protocolo, mas não constavam do
relatório web executado. O manifesto do Ollama permite medir:

| Métrica de geração | Baseline | Contexto estruturado | Variação |
| --- | ---: | ---: | ---: |
| Tokens de entrada (`prompt_eval_count`) | 2.970 | 15.564 | +424,0% |
| Média de tokens de entrada por teste | 212,1 | 1.111,7 | +424,0% |
| Tokens de saída | 3.472 | 5.250 | +51,2% |
| Tempo cliente total | 204,48 s | 345,36 s | +68,9% |
| Tempo cliente médio por teste | 14,61 s | 24,67 s | +68,9% |
| Custo monetário marginal | local; não medido | local; não medido | não aplicável |

O prompt estruturado custou aproximadamente 5,24 vezes mais tokens de entrada e
1,69 vez mais tempo, sem produzir teste aprovado nesta amostra. Não há dado de
energia ou custo de hardware no manifesto; portanto, “custo zero” não deve ser
inferido da execução local.

## Métrica diagnóstica: fidelidade de tradução do contexto

Em 7 dos 14 testes estruturados há 24 ocorrências nas quais a notação do prompt
foi copiada ou interpretada como seletor Playwright:

- `role_name:Search`;
- `role=Search`;
- `label:Email:`;
- `id:register-button`;
- `tag=a, text=Register, href=/register`;
- a string literal `page.getByRole(...)`.

Quatro casos terminaram classificados como erro de sintaxe em runtime e outros
dois como timeout de locator já no botão Search. Esta métrica mostra uma lacuna
entre “o elemento correto aparece no contexto” e “o modelo sabe convertê-lo em
código executável”.

## Conclusão

Para esta execução, o contexto estruturado oferece evidência de melhora parcial,
não de superioridade global:

1. elimina URLs de domínios inventados e aumenta fortemente a aderência ao
   grafo;
2. melhora modestamente a rubrica humana e a qualidade formal das asserções;
3. não melhora a taxa de aprovação, que permanece em 0%;
4. introduz uma classe nova de defeito: copiar a DSL do contexto como seletor;
5. exige muito mais tokens e 68,9% mais tempo de geração.

Antes de uma nova rodada, a intervenção de maior impacto é tornar os seletores
recomendados diretamente copiáveis como expressões Playwright válidas, ou
incluir no prompt uma tabela de tradução obrigatória com exemplos negativos.
Também convém validar o resultado gerado com `tsc` e uma checagem estática de
seletores proibidos antes da execução.

## Artefatos

- `resultados_qwen_gpu_20260724/baseline.playwright.json`
- `resultados_qwen_gpu_20260724/structured_context.playwright.json`
- `resultados_qwen_gpu_20260724/human_review.csv`
- `relatorios/qwen_gpu_baseline_execucao.md`
- `relatorios/qwen_gpu_structured_execucao.md`
