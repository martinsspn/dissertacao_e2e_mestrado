# Proposta Do Projeto: Contexto Estruturado Para Geracao De Testes E2E

## Problema De Pesquisa

LLMs conseguem gerar testes E2E a partir de especificacoes em linguagem natural, mas podem inventar rotas, elementos e seletores ou escolher fluxos que nao existem na aplicacao. O projeto investiga se um conjunto pequeno de dados estruturados extraidos da interface melhora essa geracao e se o eventual ganho justifica o custo adicional do prompt.

## Comparacao Experimental

Para cada especificacao sao comparadas duas entradas para a LLM:

- `baseline`: especificacao original enviada diretamente, sem passar pelo gerador;
- `structured_context`: prompt produzido pelo gerador com etapas textuais, controles e resultados observados extraidos do grafo.

O gerador produz somente o artefato `structured_context`. A mesma LLM e os mesmos parametros de geracao devem ser usados nos dois grupos. A diferenca de formatacao entre a especificacao pura e o prompt estruturado deve ser registrada no desenho experimental.

## Fluxo E Artefatos

| Atividade | Consome | Produz |
|---|---|---|
| Exploracao controlada | URL e parametros do Crawljax | paginas, controles, transicoes, resultados observados e manifesto |
| Segmentacao textual | especificacao em linguagem natural | lista ordenada de etapas |
| Selecao de contexto | paginas, controles, transicoes e etapas | ate quatro interacoes, resultados e evidencia de pagina associados por etapa |
| Preparacao do baseline | especificacao original | entrada direta para a LLM, sem arquivo gerado |
| Montagem do prompt estruturado | etapas da especificacao e contexto | prompt com contexto estruturado |
| Geracao pela LLM | um prompt | teste Playwright |
| Avaliacao | especificacao, prompt, teste e logs | relatorio comparativo |

## Segmentacao Textual

A segmentacao nao interpreta semanticamente a especificacao e nao utiliza LLM. Cada linha nao vazia e tratada como uma etapa. Quando existe apenas um paragrafo, o texto e dividido somente nos limites de sentencas. Titulos em linha propria terminados em dois-pontos, repeticoes exatas e um prefixo descritivo antes da primeira acao, como `Cenario: The user searches...`, sao removidos. A ordem e o texto original das acoes sao preservados.

## Selecao De Contexto

Os rotulos presentes em cada etapa sao comparados com controles extraidos do HTML. Nao existe dicionario de termos de dominio nem traducao automatica. Por isso, as especificacoes do experimento preservam em ingles os rotulos visiveis da interface; a generalizacao multilingue e uma ameaca a validade externa.

Uma referencia apenas ao nome de um grupo `radio` nao determina uma opcao. Por exemplo, `Gender option` permanece sem controle associado, enquanto `Female Gender option` pode fundamentar o `radio` rotulado como `Female`. Essa regra evita introduzir no prompt uma escolha que nao consta na especificacao.

A selecao e orientada a interface: procura primeiro controles na pagina ativa e pode associar ate quatro interacoes distintas quando elas sao explicitamente mencionadas ou estruturalmente relacionadas. Um exemplo e o par formado por um campo textual e o unico botao de envio de seu formulario. Nao existe ranking global, expansao por menor caminho ou envio do grafo completo. Quando nao existe correspondencia defensavel, a etapa permanece sem contexto observado.

Rotas sao evidencias auxiliares. Preencher um campo, marcar uma opcao ou clicar em um controle local nao muda a pagina presumida. Somente um `href`, uma transicao executada pelo crawler ou uma pagina identificada de forma literal e univoca por `h1` ou `title` pode orientar a mudanca de contexto. `form_action` ajuda a relacionar os controles de um formulario, mas nao prova que uma navegacao ocorreu.

Apenas um seletor e enviado por elemento. A prioridade fixa e: atributo de teste, `aria-label`/label, `id`, `name`, placeholder, texto, `href`, role e CSS. XPath, indices e seletores posicionais sao descartados. Essa ordem nao produz score e pode ser inspecionada diretamente no codigo.

## Fundamentacao De Locators E Resiliencia

A politica de seletores adota como orientacao tecnica a documentacao oficial do
Playwright, que recomenda priorizar atributos percebidos pelo usuario e contratos
explicitos e evitar cadeias CSS ou XPath dependentes da estrutura do DOM. Essa
recomendacao da ferramenta nao e tratada como prova de superioridade da politica
implementada.

A literatura cientifica fundamenta somente afirmacoes com o mesmo escopo dos
experimentos publicados:

- Hammoudi, Rothermel e Tonella caracterizam causas de quebra de testes
  record/replay a partir da evolucao de aplicacoes web (ICST 2016,
  [DOI 10.1109/ICST.2016.16](https://doi.org/10.1109/ICST.2016.16));
- Leotta, Stocco, Ricca e Tonella comparam multi-locators em seis aplicacoes e
  relatam cerca de 30% menos locators quebrados que o melhor tipo individual
  comparado (ICST 2015,
  [DOI 10.1109/ICST.2015.7102611](https://doi.org/10.1109/ICST.2015.7102611));
- Leotta, Stocco, Ricca e Tonella avaliam o Robula+ e relatam, no benchmark do
  estudo, reducao media de fragilidade de 90% frente a locators absolutos e de
  63% frente aos locators do Selenium IDE (Journal of Software: Evolution and
  Process, 2016,
  [DOI 10.1002/smr.1771](https://doi.org/10.1002/smr.1771)).

Esses estudos demonstram que a estrategia de localizacao pode influenciar as
quebras observadas durante a evolucao da interface. Eles nao demonstram que uma
chamada `getByRole`, `getByLabel`, CSS ou XPath seja universalmente superior.
Nesta pesquisa, resiliência sera uma medida experimental obtida pela reexecucao
dos mesmos testes em paginas modificadas, e nao uma conclusao derivada do tipo
de locator presente no codigo.

Documentacao tecnica utilizada na politica: [Playwright Locators](https://playwright.dev/docs/locators)
e [Playwright Best Practices](https://playwright.dev/docs/best-practices).

Nenhum score, peso, faceta, nivel de confianca ou indicador de cobertura e enviado a LLM.

O desenho implementado substitui o ranking global de transicoes pelo contexto associado diretamente a cada etapa e usa um inventario compacto de controles extraidos das paginas visitadas. Seus detalhes estao em [`projeto_contexto_estruturado_por_etapa.md`](projeto_contexto_estruturado_por_etapa.md).

## Prompt Compacto

O prompt produzido pelo gerador contem somente:

- instrucoes Playwright;
- especificacao em linguagem natural organizada em etapas, sem repetir o texto original;
- na abordagem proposta, interacoes, evidencias de pagina e resultados observados diretamente associados as etapas.

O resumo de geracao registra quantidade de caracteres e itens de contexto para apoiar a analise de eficiencia.

Para evitar repeticao, controles de uma mesma interface compartilham um unico
campo `pagina=`. Quando uma evidencia literal de `h1` ou `title` pertence a
outra pagina, sua origem aparece separadamente em `pagina_evidencia=`.

## Crawljax E Reprodutibilidade

A exploracao usa limites fixos de profundidade, estados, tempo e esperas. A ordem aleatoria fica desativada por padrao. Cada execucao grava `output_crawljax/crawl_run_manifest.json` com a URL e os parametros usados.

O crawler nao e reexecutado automaticamente quando o grafo parece insuficiente. Limitacoes da exploracao devem ser registradas e consideradas na interpretacao dos resultados.

No esquema atual, DOMs diferentes observados na mesma URL sao consolidados em um unico `PageState`. Os controles desses estados podem ser unidos, mas o gerador nao recebe a ordem temporal das mudancas AJAX. Essa perda de sequencia e uma limitacao do artefato de exploracao, nao uma evidencia de que todos os controles estavam disponiveis simultaneamente.

## Avaliacao

A especificacao pura e o prompt estruturado sao avaliados pelos mesmos criterios:

- aderencia a especificacao;
- rotas, elementos e seletores inventados;
- executabilidade e resultado da execucao;
- presenca e qualidade das assercoes;
- tipos de locator e dependencia estrutural observados no codigo gerado;
- tamanho do prompt, tempo e custo de geracao;
- utilidade pratica segundo avaliacao humana.

Nao se pressupoe que a abordagem proposta seja superior. O resultado pode indicar ganho, piora, ausencia de diferenca ou custo desproporcional.

## Escopo Futuro

Modificar controladamente a estrutura e os atributos das paginas, preservando o
comportamento funcional esperado, e reexecutar os mesmos testes permitira medir
quebras e resiliência dos locators. Separadamente, executar os testes contra uma
versao correta e versoes com defeitos funcionais propositalmente inseridos pode
medir a capacidade de deteccao de falhas. A avaliacao de resiliência nao deve ser
substituida por uma classificacao estatica baseada no tipo de locator.
