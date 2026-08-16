# Suite de especificacoes em linguagem natural

Esta suite reescreve, em linguagem natural e com redacao propria, comportamentos encontrados em tres projetos publicos de testes do Demo Web Shop. Ela serve como conjunto de entrada para o experimento de geracao de testes, nao como implementacao de referencia.

Data da consulta: 13 de julho de 2026.

## Fontes consultadas

| Projeto | Tecnologia | Revisao consultada |
| --- | --- | --- |
| [DemowebshopPlaywrightFramework](https://github.com/vanik642/DemowebshopPlaywrightFramework) | Playwright e TypeScript | [`90a73be`](https://github.com/vanik642/DemowebshopPlaywrightFramework/commit/90a73beb4061f1ae5095ffcaab9cf42d10d7dc2a) |
| [DemoWebShop-Selenium-Java-BDD](https://github.com/gian-aguilar/DemoWebShop-Selenium-Java-BDD) | Selenium, Java e Cucumber | [`c48f594`](https://github.com/gian-aguilar/DemoWebShop-Selenium-Java-BDD/commit/c48f5944a1aa87e4532d54b237191facfde7988e) |
| [DemoWebShop](https://github.com/KrisDeluca/DemoWebShop) | Selenium, Java, Cucumber e TestNG | [`ff150d7`](https://github.com/KrisDeluca/DemoWebShop/commit/ff150d7fd1e67628d6929f6ba843402b49e59349) |

Nenhum arquivo de licenca foi encontrado nas revisoes consultadas. Por isso, nenhum codigo, seletor, credencial ou texto de cenario foi copiado. Somente os comportamentos observaveis foram usados como referencia para uma nova redacao.

## Criterios de curadoria

- Um arquivo representa um objetivo de teste independente.
- Cada linha descreve uma acao do usuario, uma pre-condicao ou um resultado observavel.
- Os nomes visiveis da interface permanecem em ingles para permitir correspondencia literal com o contexto extraido do HTML.
- Credenciais, enderecos e senhas devem vir do ambiente de execucao e nunca da especificacao.
- Cadastro usa email unico por execucao para evitar colisao de estado.
- Carrinho e wishlist sao preparados dentro do proprio cenario, evitando dependencia da ordem de execucao.
- Contagens exatas de resultados e valores de preco foram omitidos por serem oraculos volateis e nao essenciais ao comportamento avaliado.

## Cenários selecionados

| Grupo | Especificacoes | Origem comportamental principal |
| --- | --- | --- |
| Autenticacao | `suite_login_valido.txt`, `suite_login_invalido.txt`, `suite_logout.txt` | Selenium BDD e Playwright |
| Cadastro | `suite_registro_usuario.txt` | Cucumber/TestNG |
| Busca e produto | `suite_busca_blue_jeans.txt`, `suite_detalhes_fiction.txt` | Selenium BDD e Playwright |
| Carrinho | `suite_adicionar_carrinho.txt`, `suite_limpar_carrinho.txt` | As tres suites |
| Wishlist | `suite_adicionar_wishlist.txt`, `suite_limpar_wishlist.txt` | Cucumber/TestNG |
| Produto configuravel | `suite_configurar_desktop.txt` | Cucumber/TestNG |
| Compra completa | `suite_checkout_blue_jeans.txt` | Selenium BDD |

## Uso no experimento

Cada arquivo deve ser tratado como uma unidade experimental. No baseline, seu texto e enviado sem modificacao para a LLM. Na abordagem proposta, o mesmo texto e usado para selecionar o contexto estruturado e compor o prompt. As implementacoes originais nao devem ser fornecidas a LLM, pois isso introduziria uma resposta de referencia apenas durante a geracao.

Os cenarios de login, wishlist, logout e checkout exigem uma conta de teste controlada. O checkout tambem exige dados validos de endereco. Essas dependencias devem ser registradas na configuracao da execucao. O cenario de cadastro exige isolamento ou limpeza posterior da conta criada.
