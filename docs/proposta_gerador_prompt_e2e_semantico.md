# Proposta Do Projeto: Gerador De Prompts E2E Semanticos

## Escolha Do Projeto

O projeto principal passa a ser o gerador de prompts estruturados para testes E2E Playwright, localizado em `python_app/teste_prompt_e2e_semantico/`.

A geracao totalmente autonoma de testes fica como extensao experimental, nao como promessa central da dissertacao. Essa decisao reduz risco, melhora a reprodutibilidade e preserva o diferencial tecnico ja implementado: usar um grafo de navegacao enriquecido semanticamente para orientar uma LLM.

## Problema

LLMs conseguem gerar testes E2E a partir de descricoes em linguagem natural, mas tendem a:

- inventar rotas, textos e seletores;
- escolher fluxos que nao existem na aplicacao;
- usar seletores frageis;
- gerar testes que parecem plausiveis, mas nao refletem a estrutura real da interface;
- depender fortemente da qualidade manual do prompt escrito pelo usuario.

O problema investigado e como fornecer contexto estruturado, extraido automaticamente da aplicacao, para reduzir essas falhas na geracao de testes E2E.

## Proposta

Construir um pipeline que:

1. Explora a aplicacao com Crawljax a partir da URL alvo.
2. Persiste no Neo4j um grafo com paginas, transicoes, atributos dos elementos, seletores e metadados textuais.
3. Recebe uma especificacao de teste em linguagem natural.
4. Seleciona paginas, transicoes e caminhos candidatos por relevancia textual e qualidade de seletores.
5. Estima a cobertura da especificacao pelo grafo, indicando requisitos suportados, parciais e ausentes.
6. Gera um prompt estruturado para uma LLM produzir um teste Playwright.

A contribuicao nao e apenas "chamar uma LLM", mas transformar a aplicacao explorada em contexto semantico curado, auditavel e reutilizavel.

O Crawljax e tratado como mecanismo automatico de exploracao. O usuario informa a URL da aplicacao e o sistema aplica uma politica padrao com limites internos de profundidade, estados e tempo para manter o grafo finito e reprodutivel.

## Perguntas De Pesquisa

RQ1. Prompts enriquecidos com grafo semantico reduzem alucinacoes de rotas, seletores e elementos em testes E2E gerados por LLM?

RQ2. O ranking de paginas, transicoes e caminhos aumenta a aderencia do teste gerado ao fluxo especificado em linguagem natural?

RQ3. A politica de seletores baseada nos metadados do grafo favorece testes mais robustos e legiveis?

RQ4. Qual o custo pratico da abordagem em termos de tamanho do prompt, tempo de geracao e necessidade de intervencao manual?

## Hipotese

Testes gerados com especificacao em linguagem natural mais contexto semantico do grafo devem apresentar maior aderencia conceitual ao fluxo esperado, menor alucinacao de rotas/seletores e maior robustez tecnica do que testes gerados apenas com a especificacao textual.

O sucesso da execucao nao e usado isoladamente como indicador de qualidade. Um teste pode falhar porque detectou corretamente um comportamento ausente na aplicacao. Por isso, a avaliacao separa qualidade do teste gerado, resultado observado e causa provavel da falha.

## Metodo De Avaliacao

Comparar pelo menos duas abordagens:

- Baseline: prompt contendo apenas a especificacao em linguagem natural e regras gerais de Playwright.
- Proposta: prompt contendo especificacao, paginas relevantes, transicoes relevantes, caminhos candidatos, seletores recomendados e avisos de qualidade do contexto.

Para cada especificacao, gerar testes com a mesma LLM e avaliar:

- Avaliacao automatica: compilacao, estrutura do teste, uso de `expect`, uso de rotas/seletores presentes no grafo, risco dos seletores e resultado de execucao.
- Avaliacao humana: aderencia do fluxo a especificacao em linguagem natural, corretude dos elementos escolhidos, qualidade das assercoes e utilidade pratica do teste.
- Classificacao de falha: quando um teste falhar, separar `application_failure`, `generated_test_failure`, `environment_failure` e `inconclusive`.

A avaliacao detalhada esta descrita em `docs/protocolo_avaliacao_hibrida.md`.

A camada `specification_coverage`, usada para estimar o grau de fundamentacao da especificacao no grafo antes da geracao do teste, esta documentada em `docs/specification_coverage.md`.

## Artefatos Esperados

- Grafo Neo4j gerado pelo Crawljax.
- Especificacoes em linguagem natural.
- Prompts baseline.
- Prompts enriquecidos pela abordagem proposta.
- Testes Playwright gerados.
- Planilha ou JSON de avaliacao manual/semiautomatica.
- Relatorios automaticos de analise estatica, conformidade com o grafo e execucao.
- Analise comparativa dos resultados.
- Modulo web opcional para apoiar a execucao e visualizacao do pipeline experimental.

## Relevancia Cientifica

O trabalho contribui para a area de teste de software e engenharia de software baseada em IA ao investigar uma forma de grounding para LLMs: em vez de depender apenas do conhecimento geral do modelo, a geracao e condicionada por evidencias extraidas da aplicacao real.

Tambem dialoga com temas atuais:

- test generation with large language models;
- web crawling e modelagem de estados;
- recuperacao de contexto para geracao aumentada por informacao;
- robustez de seletores em testes E2E;
- avaliacao empirica de codigo gerado por IA.

## Relevancia Para O Mercado

Na pratica profissional, times gastam muito tempo escrevendo e mantendo testes E2E. A abordagem pode apoiar:

- criacao inicial de suites de regressao;
- onboarding em sistemas web desconhecidos;
- documentacao executavel de fluxos de negocio;
- reducao de seletores frageis;
- revisao assistida de fluxos descobertos automaticamente;
- uso de LLMs com menos alucinacao e mais contexto do sistema real.

O valor de mercado nao esta em substituir totalmente o testador, mas em acelerar a criacao de testes com uma camada de contexto verificavel.

## Escopo Para Finalizar

O escopo recomendado para entrega e:

1. Consolidar o gerador de prompts como modulo principal.
2. Corrigir ruidos do ranking, especialmente transicoes `reload` e seletores fracos.
3. Produzir prompts compactos e auditaveis.
4. Criar um conjunto pequeno de especificacoes representativas.
5. Gerar testes por baseline e pela proposta.
6. Avaliar os testes com criterios objetivos.
7. Relatar ameacas a validade, incluindo limitacoes do crawler, do site escolhido e da LLM usada.

## Fora Do Escopo Principal

- Prometer geracao totalmente autonoma de testes de alta qualidade.
- Avaliar muitos sites diferentes.
- Treinar ou ajustar um modelo de linguagem.
- Resolver todos os problemas de exploracao dinamica do Crawljax.
- Garantir que qualquer fluxo complexo, com autenticacao ou dados dinamicos, seja gerado sem intervencao humana.
- Tratar a interface web como contribuicao cientifica principal; ela e uma ferramenta de apoio experimental.
