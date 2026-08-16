# Ampliacao candidata da suite do Demo Web Shop

Este documento registra a curadoria de novas especificacoes em linguagem natural para uma rodada adicional do experimento. Os arquivos foram mantidos em `python_app/teste_prompt_e2e_semantico/specs_candidates_20260727/`, separados das 14 especificacoes e dos artefatos das execucoes anteriores.

Data da consulta e da verificacao da interface: 27 de julho de 2026.

## Objetivo e isolamento

A ampliacao acrescenta 18 objetivos de teste candidatos, sem modificar a entrada, os prompts, os testes gerados ou os relatorios das rodadas ja concluidas. Na proxima rodada, cada especificacao deve voltar a ser processada nas duas condicoes experimentais:

1. baseline, contendo somente a especificacao em linguagem natural;
2. contexto estruturado, contendo a mesma especificacao e o contexto produzido pelo gerador.

Cada condicao deve possuir diretorios de prompts, respostas, testes e relatorios exclusivos. A saida de uma condicao nao pode ser fornecida ao modelo, ao gerador ou ao avaliador da outra condicao.

## Repositorios publicos consultados

| Projeto | Evidencias examinadas | Revisao consultada |
| --- | --- | --- |
| [VadymDrebot/DemoWebShop](https://github.com/VadymDrebot/DemoWebShop) | testes de cadastro, login, navegacao por categorias e carrinho | [`7871353`](https://github.com/VadymDrebot/DemoWebShop/commit/78713535d28f9038fbb3ae935b973b19d3406410) |
| [Arti-98/Tricentis_Demo_Web_Shop](https://github.com/Arti-98/Tricentis_Demo_Web_Shop) | cenarios BDD de navegacao, produtos e atualizacao do carrinho | [`22f6d45`](https://github.com/Arti-98/Tricentis_Demo_Web_Shop/commit/22f6d4504215387517de4e86de8805a664c32a49) |
| [Kaif955/-Automation-Testing-Project-Demo-Web-Shop-Tested-with-Cypress-](https://github.com/Kaif955/-Automation-Testing-Project-Demo-Web-Shop-Tested-with-Cypress-) | scripts Cypress de categorias, busca, perfil e links do rodape | [`de9d334`](https://github.com/Kaif955/-Automation-Testing-Project-Demo-Web-Shop-Tested-with-Cypress-/commit/de9d334b1ff457d08e2ae484c582dabc14e5a15b) |
| [TapashiRoy/UIDemoWebShopAutomation](https://github.com/TapashiRoy/UIDemoWebShopAutomation) | testes e page objects de catalogo, enquete, produtos e recuperacao de senha | [`c2f4ca4`](https://github.com/TapashiRoy/UIDemoWebShopAutomation/commit/c2f4ca43cc69b48d71d33494d493ca81c6eb3448) |
| [GThippeswamy/Demo-Web-Shop](https://github.com/GThippeswamy/Demo-Web-Shop) | casos de teste de cadastro, busca, carrinho, comparacao e produtos recentes | [`7f801e2`](https://github.com/GThippeswamy/Demo-Web-Shop/commit/7f801e222474bb0e273b8bcc05afe61f5d7f1d0f) |

Nenhum arquivo `LICENSE` ou `COPYING` foi encontrado nas revisoes consultadas. Por isso, nenhum codigo, seletor, dado de teste ou texto de cenario foi copiado. Os repositorios serviram apenas para identificar comportamentos observaveis, que foram reescritos com redacao propria e conferidos na aplicacao publica [Demo Web Shop](https://demowebshop.tricentis.com/).

## Criterios de curadoria

- Remover cenarios semanticamente equivalentes aos 14 arquivos da suite anterior.
- Manter um objetivo principal por arquivo.
- Especificar resultados observaveis, evitando prescrever seletores ou detalhes de implementacao.
- Usar produtos e textos que estavam visiveis na aplicacao durante a verificacao.
- Tornar explicitas as pre-condicoes de autenticacao e de novo contexto de navegador.
- Preparar e restaurar estado dentro do proprio cenario quando houver alteracao persistente.
- Evitar oraculos volateis, como numero de avaliacoes, total global de produtos e ano do rodape.

## Cobertura acrescentada

| Grupo | Especificacoes candidatas | Quantidade |
| --- | --- | ---: |
| Busca negativa | `suite_busca_sem_resultados.txt` | 1 |
| Validacao de cadastro | `suite_cadastro_campos_obrigatorios.txt`, `suite_cadastro_senha_curta.txt`, `suite_cadastro_confirmacao_senha.txt` | 3 |
| Catalogo de livros | `suite_navegar_categoria_livros.txt`, `suite_ordenar_livros_por_preco.txt`, `suite_exibir_quatro_livros.txt`, `suite_visualizacao_livros_em_lista.txt`, `suite_filtrar_livros_abaixo_25.txt` | 5 |
| Carrinho | `suite_atualizar_quantidade_carrinho.txt`, `suite_adicionar_dois_produtos_carrinho.txt`, `suite_persistencia_carrinho_apos_login.txt`, `suite_carrinho_inicialmente_vazio.txt` | 4 |
| Recursos de produto | `suite_comparar_produtos.txt`, `suite_produtos_visualizados_recentemente.txt` | 2 |
| Pagina inicial e navegacao | `suite_enquete_sem_resposta.txt`, `suite_navegar_sobre_nos.txt`, `suite_navegar_cartoes_presente.txt` | 3 |
| **Total adicional** |  | **18** |

Com os 14 arquivos usados na rodada mais recente, a uniao das duas colecoes possui 32 especificacoes. Esse total descreve a base planejada; ele nao deve ser apresentado como quantidade de testes gerados ou avaliados antes da execucao da nova rodada.

## Confirmacao na aplicacao

Foram confirmados diretamente na interface atual:

- a mensagem de busca sem resultados;
- as cinco mensagens de campo obrigatorio e a regra de senha com pelo menos seis caracteres;
- os controles `View as`, `Sort by` e `Display`, alem das tres faixas de filtro por preco em Books;
- os comandos de atualizacao do carrinho e de comparacao de produtos;
- a pagina e a ordem dos produtos visualizados recentemente;
- a enquete `Do you like nopCommerce?` e a mensagem exibida quando nenhuma resposta e selecionada;
- os links `About us`, `Recently viewed products` e `Compare products list`;
- as categorias Books e Gift Cards.

A verificacao manual confirma a existencia do comportamento, mas nao substitui a avaliacao posterior dos testes produzidos pelas LLMs.

## Cenarios encontrados e nao selecionados

| Comportamento encontrado | Motivo da exclusao nesta etapa |
| --- | --- |
| Aplicar cupom promocional | depende de um codigo valido externo e nao controlado |
| Cancelar pedido | a documentacao consultada nao demonstrou um fluxo publico e estavel de cancelamento |
| Validar produto esgotado | depende do estoque mutavel da aplicacao |
| Confirmar recebimento de email | depende de infraestrutura externa ao navegador |
| Validar alinhamento responsivo | exige um oraculo visual especifico, diferente das metricas atuais |
| Interagir com o carrossel | o componente e dinamico e nao acrescenta um fluxo de negocio relevante para esta rodada |
| Assinar newsletter | a resposta observavel nao se mostrou estavel durante a verificacao |

## Preparacao da proxima rodada

Antes da geracao, deve-se verificar se todos os estados e elementos requeridos pelos 18 arquivos aparecem no grafo navegacional usado pelo gerador. Se um comportamento confirmado na aplicacao nao estiver no grafo, isso deve ser registrado como lacuna de exploracao do crawler, e nao corrigido manualmente apenas no prompt estruturado. Depois dessa verificacao, as duas condicoes devem usar a mesma versao da aplicacao, o mesmo modelo, os mesmos parametros de inferencia e a mesma especificacao.
