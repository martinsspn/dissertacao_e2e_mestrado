# Projeto Da Melhoria: Contexto Estruturado Por Etapa

## Status

Implementado. O crawler persiste o inventario `UiElement`, resultados observados e o
manifesto de execucao; o gerador associa o contexto separadamente a cada etapa
com uma estrategia orientada a interface e produz somente prompts da condicao
com contexto estruturado.

## Objetivo

Produzir um contexto curto, rastreavel e diretamente relacionado a cada etapa da especificacao. A unidade operacional e a interface ativa: uma etapa pode interagir com varios controles da mesma pagina sem produzir uma nova rota. Para um cenario de busca e adicao ao carrinho, o contexto deve priorizar controles realmente presentes nas paginas visitadas, como o campo e o botao de busca, o produto, o botao de adicao e o link do carrinho. Evidencias de resultado so podem ser incluidas quando a exploracao efetivamente executou a transicao que as produziu.

A melhoria nao deve introduzir:

- LLM na decomposicao ou na selecao de contexto;
- dicionario entre portugues e ingles;
- scores, pesos, facetas ou specification coverage;
- nova exploracao orientada por uma especificacao;
- envio do grafo completo para a LLM;
- tentativa de garantir que a abordagem estruturada seja superior ao baseline.

## Diagnostico Do Desenho Anterior

O grafo atual preserva principalmente paginas e transicoes que o Crawljax executou. Elementos que nao produzem navegacao, como campos de texto e botoes AJAX, podem nao aparecer como transicoes. A selecao combina os termos de todas as etapas, ordena transicoes pela quantidade de coincidencias e calcula um caminho ate a primeira transicao selecionada.

No cenario `suite_adicionar_carrinho`, esse comportamento selecionou varias copias do link global `Shopping cart(0)` e introduziu `Notebooks` como prefixo de um caminho. O contexto nao trouxe `Search store`, `Blue Jeans`, `Add to cart` nem a notificacao de sucesso.

O problema possui duas causas diferentes:

1. o artefato de exploracao nao conserva todos os controles relevantes das paginas visitadas;
2. a selecao global nao mantem a correspondencia entre uma etapa e o elemento que a fundamenta.

## Decisoes De Projeto

### D1. Contexto Organizado Por Etapa

Cada item de contexto indica explicitamente qual etapa fundamenta. As secoes genericas `Caminho navegacional` e `Elementos relacionados` foram substituidas por `Contexto por etapa`.

### D2. Inventario De Interface Separado Das Transicoes

Uma pagina visitada deve conservar seus controles de interface mesmo quando eles nao causarem uma nova URL ou um novo estado reconhecido pelo Crawljax.

O perfil atual executa somente links navegacionais. Botoes, campos e outros
controles sao consumidos do DOM como dados estruturados da interface, sem que sua
presenca em `HAS_ELEMENT` implique que tenham sido acionados pelo crawler.

### D3. Correspondencia Literal E Deterministica

Os rotulos visiveis preservados na especificacao, como `Search store`, `Blue Jeans`, `Add to cart` e `Shopping cart`, sao comparados com os dados extraidos do HTML. A correspondencia exata continua sendo a regra principal; uma normalizacao morfologica geral e limitada pode reconhecer a forma da acao, sem vocabulario de dominio. Ausencia de correspondencia produz ausencia de contexto, e nao um candidato escolhido por proximidade numerica.

Para evitar coincidencias incidentais, a correspondencia literal de rotulos de
uma unica palavra preserva a forma escrita da especificacao. Separadamente, a
regra de acao pode reconhecer flexoes gerais, como `searches` para `Search`,
quando esse e o verbo que inicia a acao do usuario. Ela nao contem sinonimos nem
termos do Demo Web Shop. Assim, o link `Search` nao fundamenta a expressao
generica `search results`, e a tag `jeans` nao substitui o produto `Blue Jeans`.
Um controle sem seletor identificavel tambem nao e enviado.

Uma referencia de uma palavra tambem pode ser aceita sem distinguir maiusculas
quando a propria frase explicita o papel do controle, por exemplo `email field`
ou `Register button`. Essa regra sintatica nao se aplica a `search results`, que
nao nomeia um campo, botao ou link.

Controles `radio` exigem que a opcao concreta esteja escrita na etapa. Mencionar
somente o nome do grupo, como `Gender option`, nao permite escolher `Female` ou
qualquer outro valor. Essa ausencia de contexto e preferivel a inserir uma
decisao arbitraria na entrada da LLM.

### D4. Contexto Compacto Por Etapa

Uma etapa pode receber, no total:

- de zero a quatro controles distintos para executar as interacoes mencionadas;
- dentre esses controles, quando aplicavel, um elemento estruturalmente relacionado, como o unico campo textual do formulario cujo botao de envio foi identificado;
- um resultado observavel causalmente ligado a cada controle executado pelo crawler;
- uma evidencia literal curta de `h1`, `title` ou texto visivel da pagina.

Esse limite decorre da estrutura da etapa, nao de um score configuravel.

### D5. Nenhuma Consulta Ao Site Durante A Geracao

O gerador usa exclusivamente o artefato de uma exploracao controlada anterior. Consultar o site a partir dos termos da especificacao equivaleria a uma exploracao direcionada e alteraria a comparacao experimental.

### D6. Falta De Contexto E Um Resultado Valido

Se uma pagina ou um elemento nao foi observado, o gerador nao deve inventa-lo. A limitacao deve ser registrada e considerada na analise do efeito da exploracao sobre os resultados.

### D7. Rotas Como Evidencia Auxiliar

O cursor da pagina ativa organiza a busca por controles, mas a existencia de uma
etapa nao depende de uma rota homonima. Acoes como `fill`, `check` e cliques
locais permanecem na interface corrente. Uma mudanca de pagina so e sustentada
por um link com `href`, por uma transicao observada ou por uma pagina identificada
literalmente e de modo univoco por `h1` ou `title`. Quando a etapa informa apenas
parte do nome da pagina, uma consulta de uma unica etapa adiante pode identifica-la
somente se o proximo controle citado existir em uma unica pagina observada cujo
`h1` ou `title` contenha esse termo. Se houver mais de uma pagina possivel, nenhum
contexto e acrescentado.

O atributo `form_action` relaciona controles que pertencem ao mesmo formulario e
pode ajudar a desambiguar seu botao de envio. Ele nao constitui evidencia de que
o crawler submeteu o formulario nem de que o navegador chegou a essa rota.

## Fluxo Implementado

| Atividade | Consome | Produz |
|---|---|---|
| Exploracao controlada | URL e perfil fixo do Crawljax | estados, transicoes de links e manifesto |
| Extracao de interface | DOM dos estados visitados | controles estruturados por pagina |
| Extracao de resultados | DOM anterior e posterior a uma acao | pequenos resultados observaveis associados a transicoes |
| Persistencia | paginas, controles, transicoes e resultados | grafo de navegacao e interface no Neo4j |
| Segmentacao | especificacao em linguagem natural | etapas textuais ordenadas |
| Associacao por etapa | etapas, paginas, controles e transicoes | zero a quatro interacoes, seus resultados e evidencia de pagina por etapa |
| Montagem do prompt | etapas e itens associados | prompt estruturado compacto |

O baseline permanece inalterado: a especificacao original e enviada diretamente a mesma LLM.

## Modelo De Dados

### Pagina

O no `PageState` continua consolidado por URL:

```text
PageState
- id
- url
- title
- h1
- state_count
```

`visible_text_excerpt` pode fornecer somente um trecho literal curto para uma
verificacao. `interactive_count` e `screenshot_path` permanecem como dados de
diagnostico. Nenhum desses campos e usado para calcular scores ou pesos.

Essa consolidacao por URL possui uma limitacao importante: dois estados DOM
diferentes na mesma URL, por exemplo antes e depois de uma atualizacao AJAX,
alimentam o mesmo `PageState`. Seus controles sao unidos no inventario e a ordem
temporal em que apareceram nao e preservada. Portanto, a presenca conjunta de
dois controles no artefato nao demonstra que ambos estavam disponiveis ao mesmo
tempo.

### Controle De Interface

O no `UiElement` representa um controle extraido:

```text
UiElement
- id
- page_url
- kind
- tag
- text
- title
- label
- data_testid
- id_attribute
- name
- input_type
- value
- href
- role
- aria_label
- placeholder
- form_action
- form_method
```

Relacionamento:

```text
(:PageState)-[:HAS_ELEMENT]->(:UiElement)
```

`kind` e derivado por uma tabela fixa:

| Condicao | kind | operacao sugerida |
|---|---|---|
| `input` textual ou `textarea` | `text_input` | `fill` |
| `select` | `select` | `selectOption` |
| `input[type=checkbox]` | `checkbox` | `check` |
| `input[type=radio]` | `radio` | `check` |
| `button`, `input[type=button|submit]` | `button` | `click` |
| `a[href]` | `link` | `click` |
| regiao de feedback identificavel | `feedback` | `assert` |

A operacao e somente uma traducao tecnica do tipo HTML para a API Playwright. Ela nao interpreta a intencao da especificacao.

### Transicao

`NAVIGATES_TO` representa um link navegacional executado. Seus campos de elemento apontam para os mesmos atributos usados em `UiElement` quando possivel. A operacao sugerida de um `UiElement` e uma instrucao potencial para o teste Playwright, nao uma afirmacao de que o crawler executou o controle.

Campos persistidos na transicao:

```text
observed_text
observed_element_id
observed_element_role
```

Esses campos representam um pequeno resultado que apareceu no estado posterior a acao. Nao constituem uma avaliacao de sucesso; apenas registram uma mudanca observada.

### Identidade E Deduplicacao

Um controle recebe uma identidade deterministica formada por:

```text
page_url + tag + primeiro atributo estavel + texto normalizado
```

O primeiro atributo estavel segue a ordem:

```text
data-testid, aria-label, id, name, placeholder, href, role+text, text
```

Ao consolidar estados com a mesma URL, seus controles sao unidos por essa identidade. Na selecao para o prompt, controles globais repetidos em URLs diferentes tambem podem ser tratados como equivalentes quando possuem o mesmo `tag`, `href`, rotulo normalizado e operacao. Essa deduplicacao reduz repeticao, mas nao recupera a sequencia perdida entre estados DOM de uma mesma URL.

## Extracao Do HTML

### Elementos Incluidos

Extrair dos DOMs visitados:

```css
a[href], button, input:not([type=hidden]), select, textarea,
[role=button], [role=link], [role=textbox], [role=alert],
[aria-label]
```

Tambem registrar `label[for]` como rotulo do controle correspondente e os atributos `action` e `method` do formulario ancestral.

### Elementos Excluidos

- controles desabilitados sem funcao observavel;
- scripts, estilos e nos sem identificacao textual ou atributo estavel;
- valores de senha, preservando os metadados do controle;
- tokens, cookies e valores ocultos;
- conteudo integral da pagina.

### Parser

Usar um parser HTML, preferencialmente Jsoup, no exportador Java. Expressoes regulares nao devem ser usadas para analisar a estrutura completa do DOM.

### Dados Sensiveis

Valores preenchidos pelo usuario nao sao persistidos. Para inputs textuais, conservar apenas atributos declarados no HTML. Um campo `password` e mantido como `text_input` com operacao sugerida `fill`, incluindo `id`, `name`, `label` e `placeholder` quando existirem; seu `value` e persistido como string vazia.

## Resultados Observaveis

Para cada transicao de link efetivamente executada, comparar o DOM do estado de origem com o DOM do estado de destino antes da consolidacao por URL. Manter somente novos textos visiveis associados a regioes identificaveis, como:

- `[role=alert]`;
- regioes com `aria-live`;
- elementos de notificacao com `id`;
- cabecalho principal da nova pagina;
- pequenos blocos textuais adicionados apos a acao.

Nao persistir o diff completo do DOM. Textos repetidos do cabecalho, rodape e navegacao global devem ser descartados. Se o Crawljax nao produzir um estado posterior observavel, a transicao permanece sem resultado.

Como botoes e formularios nao sao executados por esse perfil, notificacoes AJAX
de carrinho, wishlist, login e cadastro nao sao resultados observaveis do crawl.
Os respectivos controles ainda podem fundamentar a geracao porque sao extraidos
do HTML da pagina.

## Algoritmo De Associacao Por Etapa

### Entrada

- etapas preservadas pela segmentacao atual;
- controles `UiElement`;
- transicoes `NAVIGATES_TO`;
- resultados observados, quando disponiveis.

### Normalizacao

- converter para minusculas;
- remover acentos;
- condensar espacos;
- remover somente contadores finais dinamicos de rotulos conhecidos, por exemplo `Shopping cart(0)` para `Shopping cart`;
- nao traduzir palavras e nao aplicar sinonimos de dominio.

### Rotulos Comparaveis

Para cada controle, considerar os valores nao vazios de:

```text
text, aria_label, placeholder, value, title, label associado
```

Os identificadores `id` e `name` podem fornecer uma forma legivel adicional
quando representam palavras. `href` e `form_action` nao sao tratados como
rotulos da etapa. O primeiro apenas confirma o destino de um link ja
identificado; o segundo descreve a estrutura do formulario e pode desambiguar
uma acao explicita de submissao.

### Regra De Correspondencia

Para cada etapa, na ordem original:

1. iniciar pela interface ativa, determinada pelas etapas anteriores;
2. localizar nessa interface controles cujos rotulos aparecem na etapa ou cuja operacao corresponde a acao textual por regras morfologicas gerais e deterministicas;
3. para um `radio`, exigir a mencao literal de seu rotulo ou valor concreto; o nome generico do grupo nao seleciona uma opcao;
4. identificar paginas mencionadas por um `h1` ou `title` literal e univoco; ampliar a busca para essas paginas somente quando a etapa expressa entrada em uma pagina ou quando a interface ativa nao possui candidato;
5. se a entrada de pagina trouxer apenas parte do `h1` ou `title`, consultar somente a etapa seguinte e aceitar a pagina apenas quando o controle seguinte a desambiguar de forma univoca entre os artefatos observados;
6. descartar identidades equivalentes e manter ate quatro controles distintos, na ordem em que suas interacoes aparecem na etapa;
7. quando um botao de envio foi identificado e existe um unico campo textual no mesmo formulario, permitir esse campo como interacao estruturalmente relacionada, sempre dentro do limite de quatro;
8. associar um resultado observado somente a transicao executada pelo controle correspondente;
9. para uma verificacao, consumir evidencia passiva da pagina ativa, sem transformar um controle homonimo de outra pagina em acao; `user confirms/checks/verifies` e considerado verificacao principal quando introduz `that`, `whether` ou `if`, preservando a acao `confirms the password by typing it again` como preenchimento;
10. associar no maximo uma evidencia curta de pagina e remover a duplicacao quando ela for igual ao resultado observado;
11. atualizar a interface ativa somente quando houver `href`, transicao observada ou identificacao univoca da pagina pelas regras anteriores; `form_action` isolado nao altera o cursor;
12. se nada corresponder, registrar `sem contexto observado` para a etapa.

Nao ha fallback por menor caminho nem soma ponderada de palavras coincidentes.
Uma rota nao substitui os controles necessarios para cumprir uma acao dentro da
pagina. O resultado posterior permanece ligado causalmente a acao que o
produziu; o algoritmo nao tenta decidir semanticamente qual frase de verificacao
da especificacao ele satisfaz.

### Desempate

Quando mais de um controle possui o mesmo rotulo:

1. preferir a interface ativa;
2. depois, respeitar a ordem das paginas identificadas literalmente na etapa;
3. preferir o tipo de correspondencia e o seletor pela politica fixa documentada;
4. preferir o rotulo completo mais especifico;
5. por fim, usar URL e identidade do controle em ordem lexicografica para garantir determinismo.

Essas sao regras lexicograficas inspecionaveis, e nao scores ou pesos ajustados
por cenario. Elas expressam continuidade do fluxo e reprodutibilidade.

### Seletores

Enviar somente um seletor por controle. Manter a politica fixa atual, com duas correcoes:

- para texto com contador dinamico, preferir `id`, `data-testid` ou `aria-label`; em links sem esses atributos, usar o nome acessivel sem o contador com correspondencia exata, pois um `href` pode se repetir em cabecalho, menu e notificacao;
- nao recomendar texto quando o mesmo rotulo ocorre varias vezes na mesma pagina sem outro atributo de desambiguacao.

## Formato Do Contexto No Prompt

Exemplo ilustrativo para `suite_adicionar_carrinho`, limitado aos controles observados nas paginas visitadas:

```text
Contexto estruturado por etapa:

1. Pesquisar por Blue Jeans usando Search
   pagina=/
   controle_1=input, id=small-searchterms, name=q, value=Search store
   operacao_1=fill
   seletor_1=id:small-searchterms
   controle_2=input, input_type=submit, value=Search, form_action=/search
   operacao_2=click
   seletor_2=role:button|name=Search

2. Abrir Blue Jeans
   pagina=/search
   controle=a, text=Blue Jeans, href=/blue-jeans
   operacao=click
   seletor=text:Blue Jeans
   pagina_evidencia=/blue-jeans
   evidencia_pagina=h1:Blue Jeans

3. Adicionar ao carrinho
   pagina=/blue-jeans
   controle=input, id=add-to-cart-button-36, value=Add to cart
   operacao=click
   seletor=id:add-to-cart-button-36

4. Confirmar a adicao
   sem contexto observado

5. Acessar o carrinho
   controle=a, text=Shopping cart, href=/cart
   operacao=click
   seletor=href:/cart

6. Verificar o produto
   sem contexto observado
```

O valor `Blue Jeans` usado no preenchimento continua vindo da especificacao. O contexto informa quais controles participam da etapa; ele nao precisa interpretar nem repetir o dado de entrada. Sufixos numericos aparecem nos controles quando a etapa possui mais de uma interacao. Quando todas as interacoes usam a mesma interface, o prompt agrupa sua origem em um unico `pagina=`. `pagina_evidencia=` identifica separadamente a pagina cujo `h1` ou `title` fundamenta uma evidencia; ela nao substitui a pagina de origem dos controles.

O campo `destino` e exibido somente para links com `href`. Um `form_action`
permanece identificado dentro dos dados do controle, mas nao e apresentado como
destino navegacional, pois a extracao do HTML nao prova que a submissao ocorreu.

O prompt declara que esse contexto e um guia parcial, nao um roteiro executavel
completo nem a unica fonte da geracao. A LLM deve combina-lo com a especificacao
e com seu conhecimento de navegacao e automacao web para acessar as paginas,
localizar elementos visiveis e realizar as acoes ausentes. A falta de contexto
nao autoriza omitir uma etapa; apenas impede tratar uma rota, seletor ou evidencia
nao observada como fato fornecido pelo grafo. O prompt tambem exige um unico
bloco de codigo `typescript`, cujo conteudo seja um Playwright `.spec.ts`
completo e executavel sem edicao manual. Isso protege URLs e barras invertidas
da renderizacao Markdown. `page.goto` e `toHaveURL` usam URLs literais, e os
locators de acao devem ser unicos no modo estrito do Playwright. A LLM nao deve
derivar uma rota do texto de um link, produto ou titulo: `toHaveURL` so e usado
quando a URL exata foi fornecida pela base ou pelo contexto; caso contrario, a
pagina de destino e confirmada por elementos visiveis.

Se apenas o link do carrinho tiver sido observado, o prompt deve incluir somente esse elemento nas etapas correspondentes. Nao deve completar as demais etapas com links globais ou caminhos indiretos. Da mesma forma, uma busca executada inteiramente na pagina inicial pode usar seus campos e botoes sem exigir uma rota `/search` no grafo.

## Alteracoes Na Implementacao

### Crawljax

Arquivos principais:

- `crawljax_explorer/pom.xml`: adicionar parser HTML;
- `SemanticExportPlugin.java`: extrair, consolidar e persistir controles;
- `SemanticExportPlugin.java`: extrair resultados entre estados de links executados;
- manifesto: registrar a versao do esquema exportado.

Novas responsabilidades recomendadas, separadas do plugin:

```text
extraction/UiElementExtractor.java
extraction/ObservedResultExtractor.java
domain/ExtractedUiElement.java
```

O plugin coordena a exportacao; as classes de extracao permanecem testaveis sem executar um crawl completo.

### Neo4j

- criar restricao unica para `UiElement.id`;
- remover `UiElement` junto com os dados da execucao anterior;
- persistir `HAS_ELEMENT` em lote;
- manter `NAVIGATES_TO` para transicoes realmente observadas.

### Gerador Python

Arquivos principais:

- `domain/models.py`: adicionar `UiElement` e contexto associado a etapa;
- `neo4j_graph_repository.py`: carregar controles e resultados;
- `context_selection.py`: substituir ranking global por associacao literal por etapa;
- `selector_policy.py`: tratar textos dinamicos e ambiguidade;
- `prompt_builder.py`: renderizar `Contexto estruturado por etapa`;
- `config.py`: remover configuracoes de limite global e profundidade de caminho que deixarem de ter funcao.

Modelo de saida implementado:

```text
InteractionContext
- control: ContextElement
- observed_result: ObservedResult | None
```

```text
StepContext
- requirement_id
- interactions: tuple[InteractionContext, ...]  # zero a quatro
- page_evidence: PageEvidence | None
```

```text
StructuredContext
- steps: list[StepContext]
```

## Configuracao Da Exploracao

A configuracao final deve ser escolhida antes do experimento e aplicada a todas as especificacoes. Manter:

- ordem aleatoria desativada;
- prioridade `SHALLOW_FIRST`;
- execucao somente de links navegacionais;
- limites fixos de profundidade, estados, tempo e esperas;
- manifesto da execucao;
- uma unica exploracao compartilhada pelas duas condicoes experimentais.

O piloto fixou `clickOnce=true` e `randomOrder=false`. Esses valores reduzem
repeticoes, tornam a ordem deterministica e devem ser mantidos durante o
experimento. Eles nao devem ser alterados porque um cenario especifico recebeu
pouco contexto.

O subtree de interface `slider-wrapper` e ignorado tanto como origem de cliques
quanto na comparacao de estados. Trata-se de conteudo autonomo e temporizado: as
trocas do Nivo Slider nao representam acoes do usuario nem estados funcionais da
loja. Sem essa normalizacao, o reset da home pode ser confundido com um estado sem
caminho de retorno.

O subtree `block-recently-viewed-products` e ignorado na comparacao de estados.
Visitar um produto altera esse bloco na home como efeito colateral e, sem a
normalizacao, invalida caminhos anteriores. A regra e estrutural e independente
das especificacoes.

## Fases De Implementacao

### Fase 1. Controles E Contexto Por Etapa

- extrair controles dos DOMs visitados;
- persistir `UiElement` e `HAS_ELEMENT`;
- carregar controles no gerador;
- implementar correspondencia literal por etapa;
- deduplicar controles globais;
- alterar o formato do prompt;
- remover o menor caminho e o ranking por quantidade de termos.

Resultado esperado: eliminar `Notebooks` e as repeticoes de `Shopping cart`, além de recuperar campos, links e botoes presentes nas paginas visitadas.

### Fase 2. Resultados Observaveis

- comparar estados antes da consolidacao por URL;
- registrar notificacoes e pequenos textos adicionados;
- associar resultados as etapas de verificacao;
- evitar diff completo ou conteudo extenso.

Resultado esperado: fundamentar assercoes somente quando uma transicao de link produzir um texto novo identificavel. Resultados AJAX de controles nao executados ficam fora do alcance desse perfil.

### Fase 3. Piloto E Congelamento Do Protocolo

- executar um crawl piloto controlado;
- inspecionar manualmente uma amostra de contextos;
- escolher e registrar o perfil fixo de exploracao;
- congelar regras e configuracoes antes da coleta experimental;
- gerar novamente todos os prompts com o mesmo grafo.

O piloto valida coerencia tecnica, nao e uma rodada de ajuste ate a abordagem proposta superar o baseline.

## Testes Necessarios

### Extrator Java

- extrai input com `id`, `name`, placeholder e formulario;
- extrai link com texto e `href`;
- extrai botao com `value`;
- associa `label[for]` ao controle;
- extrai `password` sem valor e ignora `hidden`, script e style;
- une controles repetidos de estados com a mesma URL;
- normaliza contador dinamico sem alterar outros numeros relevantes.

### Selecao Python

- associa `Search store` somente a etapa que o menciona;
- associa `Blue Jeans` ao link exato, sem selecionar `TBlue Jeans`;
- associa uma unica ocorrencia de `Shopping cart`;
- associa campos distintos mencionados na mesma etapa, ate o limite de quatro;
- associa o campo textual unico ao botao de envio do mesmo formulario quando essa relacao for aplicavel;
- nao seleciona uma opcao `radio` quando a etapa menciona apenas o nome generico do grupo;
- mantem a pagina ativa depois de `fill`, `check` e clique local sem transicao;
- avanca a pagina quando houver `href` ou transicao observada;
- nao usa `form_action` isolado como prova de navegacao;
- usa `h1` ou `title` literal e univoco como evidencia curta de pagina;
- usa no maximo uma etapa seguinte para desambiguar uma pagina parcialmente nomeada por um controle observado;
- nao introduz `Notebooks`;
- retorna ausencia de contexto quando o elemento nao existe;
- produz a mesma saida para as mesmas entradas;
- seleciona somente um seletor por controle.

### Montagem Do Prompt

- preserva todas as etapas da especificacao;
- remove um titulo inline antes da primeira acao sem remover o texto da acao;
- agrupa contexto pela etapa correta;
- agrupa controles da mesma interface sob um unico `pagina=` e separa `pagina_evidencia=`;
- nao repete o texto original fora da lista de etapas;
- nao inclui JSON, scores, pesos ou o grafo completo;
- nao inclui controles sem correspondencia literal;
- registra quantidade de caracteres e itens enviados.

## Criterios De Aceitacao

Para a fixture de `suite_adicionar_carrinho` com todos os controles presentes:

1. o contexto contem `small-searchterms`, `/blue-jeans`, `add-to-cart-button-36` e `/cart`;
2. `Shopping cart` aparece uma unica vez como controle;
3. `Notebooks` nao aparece;
4. cada controle esta associado a uma etapa especifica;
5. nenhum controle de pagina alheia e usado como preenchimento;
6. a ausencia de uma notificacao observada nao gera texto inventado;
7. duas execucoes com o mesmo grafo e a mesma especificacao produzem prompts identicos;
8. o prompt continua valido quando apenas parte dos elementos foi observada;
9. o campo e o botao de busca podem fundamentar a mesma etapa na pagina inicial;
10. uma acao local nao exige nem inventa uma rota com o nome do objetivo;
11. nenhuma etapa possui mais de quatro interacoes.

Para resultados observados de uma transicao de link:

1. o texto observado e associado causalmente ao link executado;
2. o contexto informa um seletor identificavel para a regiao de feedback;
3. nenhum trecho extenso do DOM e enviado ao prompt.

## Riscos E Tratamento

| Risco | Tratamento |
|---|---|
| Pagina relevante nao visitada | registrar ausencia; nao executar crawl dirigido pela spec |
| Muitos controles globais | deduplicar por identidade funcional |
| Rotulo dinamico | normalizar apenas padroes documentados e preferir atributo estavel |
| Resultado AJAX nao vira estado | aceitar como ausencia deliberada no perfil que executa somente links |
| DOM possui dados sensiveis | excluir valores preenchidos, esvaziar `value` de password e ignorar hidden e tokens |
| Parser aumenta custo do crawl | extrair uma vez por estado e consolidar por URL |
| Estados DOM distintos compartilham a URL | unir controles, registrar a perda de ordem temporal e nao afirmar disponibilidade simultanea |
| Regras favorecem cenarios conhecidos | congelar regras antes do experimento e aplicar a suite completa |
| Contexto adicional nao melhora o teste | registrar como resultado experimental valido |

## Decisao Final

A unidade central deixa de ser uma transicao global considerada relevante e passa a ser a etapa na interface ativa. Controles da pagina fundamentam as interacoes; rotas, transicoes e evidencias de pagina ajudam a estabelecer continuidade quando realmente existem. A etapa determina quais evidencias podem ser enviadas. Quando nao existe evidencia, o gerador permanece silencioso ou registra explicitamente a ausencia, sem substituir o dado faltante por contexto generico.

Esse desenho aproxima o prompt do fluxo esperado sem reintroduzir a complexidade criticada: nao ha score, peso, dicionario, otimizacao adaptativa do Crawljax ou avaliacao de cobertura da especificacao.
