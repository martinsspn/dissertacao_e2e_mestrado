# Reavaliação — locators Playwright executáveis no contexto

## Intervenção

O `prompt_builder` foi alterado para emitir todos os seletores como expressões
Playwright TypeScript completas:

- `page.getByRole(...)`;
- `page.getByLabel(...)`;
- `page.getByText(...)`;
- `page.locator(...)`;
- `page.getByPlaceholder(...)`;
- `page.getByTestId(...)`.

O prompt também passou a proibir explicitamente engines descritivas como
`role_name:`, `label:`, `id:`, `tag=` e strings contendo `page.getByRole(...)`.
As instruções mostram que a ação deve ser chamada diretamente no locator.

Foram adicionados testes de regressão. A suíte do gerador passou com 40/40
testes. Os 14 novos prompts foram gerados em diretório separado e todos os seus
campos `locator_playwright` começam com uma expressão `page.*`.

## Controle experimental

- Modelo: `qwen2.5-coder:7b`.
- Seed: `20260724`; temperatura: `0`; contexto: `8192`.
- Uso observado: 79% GPU e 21% CPU.
- Chamadas Ollama stateless, sem reuso do `context` entre casos.
- Baseline e contexto estruturado em diretórios independentes.
- Mesmo Chromium, URL base, credenciais sintéticas e timeouts nas duas condições.
- Os 14 arquivos baseline novos são byte a byte idênticos aos 14 da rodada
  anterior. Isso confirma que a intervenção não contaminou o controle.

## Resultado da nova rodada

| Métrica | Baseline | Estruturado corrigido |
| --- | ---: | ---: |
| Arquivos coletados pelo Playwright | 14/14 | 14/14 |
| Testes aprovados | 0/14 (0,0%) | 2/14 (14,3%) |
| Testes reprovados | 14/14 | 12/14 |
| Erros de sintaxe em runtime | 0 | 0 |
| Falhas de geração entre os reprovados | 14/14 | 12/12 |
| Duração da suíte | 181,08 s | 149,17 s |
| Cobertura média de URLs no grafo | 60,7% | 100,0% |
| Cobertura média de textos no grafo | 91,1% | 90,8% |
| Risco baixo dos seletores | 0/14 | 7/14 |
| URLs de outros domínios | 4/14 | 0/14 |
| Vazamentos da DSL no código | 0 | 0 |
| Nota humana média | 4,43/12 | 7,43/12 |

Os testes aprovados foram:

1. `fluxo_computadores_desktops`;
2. `suite_login_invalido`.

O primeiro não verifica explicitamente a existência dos itens digitais, embora
navegue e valide a página correta. O segundo usa um email inexistente e uma
senha fixa. Assim, ambos passam tecnicamente, mas nenhum recebe conformidade
semântica máxima.

## Efeito isolado da modificação

| Métrica estruturada | Antes | Depois | Efeito |
| --- | ---: | ---: | ---: |
| Aprovação | 0/14 | 2/14 | +14,3 p.p. |
| Erros de sintaxe em runtime | 4 | 0 | -100% |
| Arquivos com DSL copiada/interpretada | 7/14 | 0/14 | -100% |
| Ocorrências da DSL | 24 | 0 | -100% |
| Risco baixo | 0/14 | 7/14 | +50,0 p.p. |
| Cobertura textual no grafo | 85,1% | 90,8% | +5,7 p.p. |
| Nota humana | 6,00/12 | 7,43/12 | +1,43 |
| Asserções no código | 70 | 58 | -12 |
| Chamadas `expect` sem `await` | 13 | 22 | +9 |

A intervenção eliminou exatamente a classe de defeito pretendida. Todos os
casos que antes falhavam ao interpretar `role_name`, `label`, `id`, `tag` ou uma
string `page.getByRole` agora conseguem usar locators válidos. O modelo também
passou a usar mais locators semânticos, refletido na nova classificação de risco.

Por outro lado, a qualidade das asserções assíncronas piorou. Os fluxos de
registro chegam muito mais longe, mas falham porque `toHaveURL` e outros
matchers Playwright não são aguardados. A contagem sem `await` inclui também
asserções escalares síncronas; a inspeção manual confirma, contudo, matchers web
assíncronos sem espera nos casos de registro e compra de livro.

## Execução por especificação

| Especificação | Antes da correção | Depois da correção |
| --- | --- | --- |
| `fluxo_computadores_desktops` | Link ambíguo | **Passou** usando `.first()` |
| `suite_adicionar_carrinho` | Sintaxe inválida em `role_name` | Busca funciona; falha por não abrir o resultado |
| `suite_adicionar_wishlist` | Sintaxe inválida em `role_name` | Busca funciona; falha por href ambíguo |
| `suite_busca_blue_jeans` | Timeout em `role=Search` | Busca funciona; classe de resultado inventada |
| `suite_checkout_blue_jeans` | Sintaxe inválida em `role_name` | Busca funciona; espera redirecionamento direto |
| `suite_configurar_desktop` | Controle de atributo inexistente | Navega às categorias; omite abertura do produto |
| `suite_detalhes_fiction` | Timeout em `role=Search` | Busca funciona; omite abertura do resultado |
| `suite_limpar_carrinho` | Seletor de remoção inexistente | Continua falhando em nome de remoção inventado |
| `suite_limpar_wishlist` | Wishlist não preparada | Continua omitindo autenticação e preparação |
| `suite_login_invalido` | Id da mensagem inventado | **Passou** com locator textual real |
| `suite_login_valido` | Rota de conta inventada | Falha antes do login em `.title` inventado |
| `suite_logout` | Formulário procurado na página errada | Mesmo erro de pré-condição/navegação |
| `suite_registro_usuario` | Sintaxe inválida em `text:Register` | Completa registro; falha por `expect` sem `await` |
| `user_registration_book_purchase` | Engine `tag` inexistente | Avança até o carrinho; falha por `expect` sem `await` |

## Conformidade humana

| Critério (máximo 2) | Baseline | Estruturado antes | Estruturado corrigido |
| --- | ---: | ---: | ---: |
| Fluxo correto | 1,79 | 1,29 | 1,21 |
| Alvo correto | 0,43 | 0,71 | 1,21 |
| Asserção correta | 0,93 | 1,07 | 1,14 |
| Aderência ao grafo | 0,71 | 1,93 | 1,86 |
| Robustez prática | 0,29 | 0,36 | 1,14 |
| Utilidade geral | 0,29 | 0,64 | 0,86 |
| **Total** | **4,43/12** | **6,00/12** | **7,43/12** |

O ganho principal agora aparece em alvo correto e robustez prática, justamente
os critérios afetados pela intervenção. A nota de fluxo não melhora porque o
modelo ainda omite ações que o grafo não representa como sequência causal:
abrir um resultado de busca, abrir o produto configurável, autenticar e preparar
wishlist.

## Custo da nova geração

| Métrica | Baseline | Estruturado corrigido | Diferença |
| --- | ---: | ---: | ---: |
| Caracteres médios da entrada | 386 | 4.486 | +1.062% |
| Tokens de entrada | 2.970 | 18.596 | +526,1% |
| Tokens de saída | 3.472 | 5.452 | +57,0% |
| Tempo cliente total | 201,01 s | 326,50 s | +62,4% |
| Tempo médio por teste | 14,36 s | 23,32 s | +62,4% |

Em relação ao contexto estruturado anterior, a nova versão usou 19,5% mais
tokens de entrada e 3,8% mais tokens de saída, mas levou 5,5% menos tempo. Essa
variação de tempo não deve ser atribuída à intervenção: carga do modelo e
desempenho do hardware não foram controlados em laboratório.

## Conclusão e próxima intervenção recomendada

A modificação foi eficaz no alvo definido: removeu integralmente o vazamento da
DSL, eliminou os erros de sintaxe associados, aumentou a robustez dos locators e
produziu os primeiros testes tecnicamente aprovados.

Ela não resolve três problemas independentes:

1. o modelo confunde submissão de busca com navegação direta ao produto;
2. pré-condições descritas como “usuário autenticado” não viram setup;
3. matchers Playwright são emitidos sem `await`.

Para preservar causalidade experimental, esses pontos não foram corrigidos nesta
rodada. A próxima intervenção deve ser separada e pequena: exigir `await` para
todos os matchers web e representar explicitamente no contexto que `Search`
produz uma página de resultados, não a página do produto.

## Artefatos

- `resultados_qwen_playwright_locators_20260724_02/baseline.playwright.json`
- `resultados_qwen_playwright_locators_20260724_02/structured_context.playwright.json`
- `resultados_qwen_playwright_locators_20260724_02/human_review.csv`
- `relatorios/qwen_playwright_locators_baseline_20260724_02.md`
- `relatorios/qwen_playwright_locators_structured_20260724_02.md`
