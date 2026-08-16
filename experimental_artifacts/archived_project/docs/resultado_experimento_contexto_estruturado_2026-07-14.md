# Resultado Do Experimento De Contexto Estruturado — 2026-07-14

## Objetivo

Este experimento verifica se os refinamentos no crawler e na selecao de contexto
produzem prompts mais corretos e compactos para as 14 especificacoes atuais.

O artefato chamado **antes** neste documento e a versao anterior do prompt com
contexto estruturado. Ele nao e o baseline experimental da dissertacao. No
experimento com LLM, o baseline continua sendo somente a especificacao original,
enviada diretamente ao mesmo modelo.

Tambem nao foi calculado score de specification coverage. As contagens abaixo sao
apenas descricoes observaveis dos artefatos.

## Execucao Controlada Do Crawler

A exploracao final usou a configuracao registrada em
`output_crawljax/crawl_run_manifest.json`:

- inicio: `2026-07-13T23:34:04.663866483Z`;
- limite: 45 minutos, profundidade 8 e 400 estados;
- prioridade `SHALLOW_FIRST`, sem ordem aleatoria;
- `click_once=true`;
- execucao somente de links `a`;
- espera de 3000 ms apos recarga e 2200 ms apos evento;
- exclusao das regioes dinamicas `slider-wrapper` e
  `block-recently-viewed-products`.

A execucao terminou pelo limite de tempo e persistiu:

| Dado observado | Quantidade |
|---|---:|
| URLs consolidadas | 134 |
| Estados Crawljax consolidados | 135 |
| Controles extraidos do HTML | 7.566 |
| Transicoes `NAVIGATES_TO` | 371 |
| Transicoes com texto observado | 281 |

O grafo contem, entre outras, as paginas `/blue-jeans`, `/fiction`, `/health`,
`/digital-downloads`, `/cart`, `/login` e `/register`. Ele nao contem `/search`
nem `/checkout`.

Foram encontrados tres campos de senha, todos com valor persistido vazio.

## Evolucao Dos Artefatos

| Configuracao | Paginas | Controles | Transicoes | Etapas com algum contexto | Itens de contexto |
|---|---:|---:|---:|---:|---:|
| Implementacao anterior | 28 | 1.592 | 88 | 29/93 | 41 |
| Seletor refinado, mesmo grafo | 28 | 1.592 | 88 | 27/93 | 38 |
| Piloto do crawler estabilizado | 32 | 1.793 | 55 | 29/93 | 40 |
| Execucao final | 134 | 7.566 | 371 | 30/93 | 41 |

Uma etapa com contexto e apenas uma etapa que recebeu pelo menos um controle,
resultado observado ou evidencia de pagina. Essa contagem nao representa uma
nota de qualidade.

O aumento nominal de 29 para 30 etapas esconde a principal mudanca: associacoes
incorretas foram removidas e substituidas por evidencias diretamente aplicaveis.

## Auditoria Manual Dos Prompts Finais

Nos 14 prompts finais foram inspecionadas as 93 etapas e todos os 30 blocos que
receberam contexto:

| Classificacao descritiva | Etapas |
|---|---:|
| Contexto diretamente util e suficiente para a acao descrita | 20 |
| Contexto pertinente, mas incompleto para uma acao composta | 10 |
| Contexto inteiramente enganoso ou associado ao controle errado | 0 |
| Sem contexto observado | 63 |

Os 41 itens finais sao 30 controles, 10 resultados observados e uma evidencia
explicita de pagina. Resultado e evidencia identicos sao deduplicados.

Exemplos de melhora:

- `Update shopping cart` nao recebe mais o link de navegacao `Shopping cart`;
- uma verificacao de logout nao recebe mais um clique em `Log in`;
- verificacoes de `Health Book` nao recebem mais links de tags com a palavra
  `book`;
- login passou a receber o campo real `Password`;
- cadastro passou a receber `Gender`, `Email`, `ConfirmPassword` e o botao real
  `#register-button`;
- a etapa `Add to cart` de `Health Book` passou a receber
  `#add-to-cart-button-22` na pagina `/health`;
- `form_action` continua identificado como dado do formulario, mas nao e mais
  apresentado como destino de navegacao observado.

Os dez casos parciais decorrem principalmente da regra atual de no maximo um
controle por etapa. Exemplos: `Email and Password`, `First name and Last name`,
`Computers and Desktops` e preencher o campo de busca sem informar tambem o
botao ou a tecla que a submete.

### Cenario `suite_adicionar_carrinho`

No cenario atualmente aberto, a quantidade permaneceu em duas das seis etapas:

- R1 recebe o campo `#small-searchterms` e a operacao `fill`;
- R5 recebe o link `href:/cart`, seu destino e o resultado observado;
- R2, R3, R4 e R6 permanecem sem contexto.

O prompt anterior e o final possuem tres itens nesse cenario. A melhora foi de
precisao: o preenchimento nao exibe mais `/search` como se fosse uma navegacao
observada. Embora `/blue-jeans` exista no grafo final, o seletor nao salta da
home para essa pagina sem uma transicao causal. Como `/search` nao foi submetida
pelo crawler, nao ha evidencia suficiente para ligar os resultados, o produto e
o botao `Add to cart` a esta sequencia especifica.

## Tamanho Dos Prompts

| Medida em caracteres | Antes | Final |
|---|---:|---:|
| Total dos 14 prompts | 23.430 | 23.659 |
| Media por prompt | 1.673,57 | 1.689,93 |
| Mediana | 1.370,5 | 1.516 |
| Maior prompt | 4.506 | 4.021 |

O total cresceu 229 caracteres, aproximadamente 0,98%, enquanto o maior prompt
diminuiu 485 caracteres, aproximadamente 10,76%. As especificacoes puras somam
6.155 caracteres e tem media de 439,64; portanto, o prompt final medio possui
aproximadamente 3,84 vezes o texto original. Essa razao inclui instrucoes fixas e
a segmentacao em etapas, nao apenas o contexto.

## Interpretacao

O teste sustenta que o refinamento melhorou a **precisao do contexto produzido**:
os falsos positivos conhecidos desapareceram, controles reais foram adicionados
e o tamanho total quase nao mudou. O ganho nao veio de maximizar a quantidade de
etapas contextualizadas.

O teste tambem mostra que ampliar o grafo, isoladamente, nao resolve as lacunas.
Como a exploracao executa somente links, ela registra o campo de busca no
inventario, mas nao submete `/search`; tambem nao monta carrinho, sessao
autenticada ou checkout.
Isso explica a ausencia de contexto nas etapas posteriores desses fluxos e deve
ser registrado como limitacao, sem transformar o projeto em otimizador do
Crawljax.

Este resultado ainda nao prova que a LLM gerara testes melhores. Para avaliar o
efeito final, cada especificacao deve ser enviada nas duas condicoes — texto puro
e prompt estruturado — para a mesma LLM, com modelo, parametros e repeticoes
controlados. Os testes produzidos devem ser compilados, executados e avaliados
quanto a aderencia ao cenario e, posteriormente, capacidade de detectar defeitos.

## Observacoes De Rastreabilidade

- O arquivo `fluxo_computadores_desktops.txt` atualmente descreve Digital
  downloads; o nome deve ser corrigido antes da coleta experimental.
- No momento deste snapshot ainda existiam prompts antigos sem o sufixo
  `.structured_context` no diretorio de saida. Eles foram removidos no
  refinamento orientado a interface; a coleta experimental continua restrita
  aos 14 prompts estruturados.
- A reproducao da comparacao entre snapshots pode usar
  `tools/compare_context_prompts.py`.
