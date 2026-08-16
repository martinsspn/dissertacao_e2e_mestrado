# Resultado Do Seletor Orientado A Interface

## Objetivo

Este registro compara duas versoes do gerador usando exatamente o mesmo grafo da
exploracao controlada do Demo Web Shop:

- **anterior**: no maximo um controle por etapa e continuidade determinada
  principalmente pela pagina corrente;
- **orientada a interface**: ate quatro interacoes por etapa, controles locais
  preservados na mesma interface e rotas usadas somente como evidencia auxiliar.

O baseline experimental da dissertacao nao e nenhuma dessas versoes. Ele
continua sendo a especificacao original enviada diretamente a mesma LLM.
Tambem nao foi calculado score de cobertura da especificacao.

## Mudancas Avaliadas

- campo e submit do mesmo formulario podem aparecer juntos;
- etapas compostas podem conservar varios campos ou controles explicitos;
- `fill`, `check` e botoes sem navegacao observada nao alteram a pagina ativa;
- `form_action` relaciona controles do formulario, mas nao e apresentado como
  destino observado;
- uma pagina nomeada pode fornecer evidencia literal de `h1` ou `title`, sem que
  isso afirme a observacao do caminho ate ela;
- rotulos genericos que sao subconjuntos de outro rotulo sao descartados, como
  `book` diante de `Health Book`;
- uma referencia generica a um grupo `radio` nao escolhe uma opcao arbitraria;
- o titulo inline do cenario e removido antes da primeira etapa;
- controles da mesma pagina compartilham um unico campo `pagina=` no prompt.

## Resultado Nas 14 Especificacoes

| Medida descritiva | Anterior | Orientada a interface | Diferenca |
|---|---:|---:|---:|
| Etapas avaliadas | 93 | 93 | 0 |
| Etapas com algum contexto | 30 | 44 | +14 |
| Controles, resultados e evidencias | 41 | 71 | +30 |
| Caracteres nos 14 prompts | 23.659 | 34.500 | +10.841 |

Os 71 itens finais sao 48 controles, tres resultados observados e 20 evidencias
literais de pagina. Uma etapa com contexto e apenas uma etapa que recebeu pelo
menos um desses itens; essa contagem nao representa uma nota de qualidade.

O tamanho total cresceu aproximadamente 45,8%. Esse aumento deve ser considerado
na avaliacao com a LLM: a abordagem passou a contextualizar mais acoes, mas o
custo adicional so se justifica se houver ganho nos testes gerados. O total
inclui a instrucao fixa de que o contexto e apenas um guia e deve ser combinado
com a especificacao e com a experiencia de navegacao web da LLM, alem da
protecao para produzir um `.spec.ts` executavel dentro de um bloco de codigo,
manter `page.goto` e `toHaveURL` como URLs literais sem sintaxe Markdown e usar
locators unicos no modo estrito.

| Cenario | Etapas com contexto antes | Depois | Etapas adicionadas | Etapas removidas |
|---|---:|---:|---|---|
| `fluxo_computadores_desktops` | 1 | 1 | - | - |
| `suite_adicionar_carrinho` | 2 | 4 | R2, R3 | - |
| `suite_adicionar_wishlist` | 2 | 2 | - | - |
| `suite_busca_blue_jeans` | 1 | 3 | R3, R4 | - |
| `suite_checkout_blue_jeans` | 1 | 3 | R2, R3 | - |
| `suite_configurar_desktop` | 2 | 2 | - | - |
| `suite_detalhes_fiction` | 1 | 3 | R2, R3 | - |
| `suite_limpar_carrinho` | 1 | 2 | R1 | - |
| `suite_limpar_wishlist` | 1 | 1 | - | - |
| `suite_login_invalido` | 2 | 3 | R3 | - |
| `suite_login_valido` | 2 | 3 | R3 | - |
| `suite_logout` | 0 | 0 | - | - |
| `suite_registro_usuario` | 6 | 5 | - | R2 |
| `user_registration_book_purchase` | 8 | 12 | R1, R4, R5, R6 | - |

A remocao de R2 em `suite_registro_usuario` e intencional: a especificacao pede
apenas uma opcao de genero, mas nao determina `Male` ou `Female`. O gerador nao
deve inserir essa escolha na entrada da LLM.

## Exemplos De Ganho

- uma busca recebe `#small-searchterms` e o submit `Search` da mesma pagina, sem
  exigir que `/search` exista no grafo;
- `Email and Password`, `First name and Last name` e `Password and Confirm
  password` preservam os dois campos;
- referencias como `email field` e `password field` sao reconhecidas sem
  depender de maiusculas, e `confirms the password by typing it again` e tratado
  como preenchimento, nao como verificacao passiva;
- a etapa seguinte a busca por Blue Jeans pode usar
  `#add-to-cart-button-36`, pois a pagina e identificada literalmente por
  `h1:Blue Jeans`;
- o formulario de login usa o submit `Log in`, e nao o submit global `Search`;
- a submissao do cadastro usa somente `#register-button`, sem o link homonimo
  `Register`;
- `Digital downloads` nao recebe tambem o link generico `digital`, e `Health
  Book` nao recebe a tag `book`.

## Interpretacao E Limites

O resultado mostra que o contexto deixou de depender de uma rota para representar
acoes realizadas dentro da pagina. Ao mesmo tempo, ele nao elimina a informacao
navegacional: um `href` ainda identifica o destino de um link, e uma transicao
executada ainda pode fornecer um resultado observado.

Uma evidencia `pagina_evidencia=/blue-jeans` com `h1:Blue Jeans` comprova que
essa interface existe no artefato e ajuda a desambiguar seus controles. Ela nao
comprova que o crawler submeteu a busca nem observou todo o caminho ate o
produto. Essa diferenca deve ser mantida na analise experimental.

O exportador ainda consolida DOMs diferentes que possuem a mesma URL. Portanto,
estados AJAX podem ter seus controles unidos sem preservar a ordem temporal.
Essa limitacao deve ser registrada, mas sua correcao exigiria um novo modelo de
estado e nao faz parte deste refinamento.

Nenhum novo crawl foi necessario para esta comparacao. A mudanca usa o mesmo
inventario de paginas e controles, permitindo atribuir a diferenca observada ao
seletor e ao formato do prompt. O passo seguinte continua sendo gerar testes nas
duas condicoes experimentais e medir compilacao, execucao, aderencia e deteccao
de defeitos.
