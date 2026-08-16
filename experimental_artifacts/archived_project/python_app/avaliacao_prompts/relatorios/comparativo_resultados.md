# Comparação dos testes gerados: baseline × contexto estruturado

## Conclusão principal

As duas abordagens terminaram empatadas na execução: **7 de 12 testes passaram (58,3%) e 5 falharam (41,7%) em cada grupo**. Nenhum dos 24 arquivos apresentou erro de sintaxe ou de carregamento pelo Playwright.

O contexto estruturado alterou características diretamente mensuráveis do código gerado: aumentou a proporção de chamadas `getBy*` e a cobertura de textos encontrados no grafo. Essas medidas descrevem a geração e não comprovam maior robustez ou resiliência. Nesta execução inicial, a taxa de aprovação não mudou. As falhas observadas também mostram que chamadas `getBy*` podem ser ambíguas, estar excessivamente restritas a um contêiner ou usar um papel incorreto.

Este relatório corresponde à primeira etapa experimental: geração dos testes e execução contra a versão atual da aplicação. A resiliência somente poderá ser avaliada em uma segunda etapa, mediante mudanças controladas nas páginas e reexecução dos mesmos testes.

## Ambiente e método

- Playwright 1.61.1 com Chromium 149, em modo headless;
- execução isolada por arquivo, com um worker;
- timeout de teste de 20 segundos, ação de 10 segundos e expectativa de 7 segundos;
- aplicação: `https://demowebshop.tricentis.com/`;
- conta descartável criada pelo próprio teste de registro estruturado;
- dados pessoais e endereço fictícios;
- uma execução consolidada por cenário, sem repetição estatística.

Os testes que exigiam autenticação foram inicialmente executados sem configuração para observar o comportamento diante de pré-condições ausentes. Depois foram repetidos com credenciais válidas. Os resultados configurados prevalecem na tabela final.

## Comparação quantitativa

| Indicador | Baseline | Contexto estruturado | Leitura |
| --- | ---: | ---: | --- |
| Arquivos carregados sem erro de sintaxe | 12/12 (100%) | 12/12 (100%) | empate |
| Testes aprovados | 7/12 (58,3%) | 7/12 (58,3%) | empate |
| Testes reprovados | 5/12 (41,7%) | 5/12 (41,7%) | empate |
| Estrutura mínima e asserção | 12/12 (100%) | 12/12 (100%) | empate |
| Uso de `waitForTimeout` | 0/12 | 0/12 | nenhuma espera fixa |
| XPath | 0 | 0 | nenhuma ocorrência |
| Classificação heurística “baixo” | 6/12 (50,0%) | 11/12 (91,7%) | descrição da regra interna; não mede resiliência observada |
| Classificação heurística “médio” | 6/12 (50,0%) | 1/12 (8,3%) | descrição da regra interna; não mede resiliência observada |
| Cobertura média de URLs no grafo | 100,0% | 100,0% | empate |
| Cobertura média de textos no grafo | 88,2% | 96,5% | vantagem estruturada de 8,3 p.p. |
| Chamadas `getBy*` / total de locators | 81/164 (49,4%) | 115/158 (72,8%) | diferença descritiva do código gerado |
| Média de locators por teste | 13,67 | 13,17 | volumes semelhantes |
| Média de ações por teste | 8,33 | 6,92 | estruturado gerou fluxos um pouco mais compactos |
| Tamanho médio da entrada da LLM | 386 caracteres | 3.480 caracteres | contexto estruturado usa cerca de 9 vezes mais texto |

## Resultado por cenário

| Cenário | Baseline | Contexto estruturado | Diagnóstico principal |
| --- | --- | --- | --- |
| Adicionar ao carrinho | ❌ | ✅ | Baseline usa `input[value="Add to cart"]`, que encontra quatro botões. O estruturado usa o ID específico do produto. |
| Buscar Blue Jeans | ✅ | ✅ | Ambos localizaram, abriram e validaram o produto. |
| Checkout | ❌ | ❌ | Ambos assumem que a etapa de endereço de entrega está visível; no estado observado o contêiner estava oculto. |
| Configurar desktop | ❌ | ❌ | Baseline omite os acréscimos de preço nos labels; estruturado restringe `Desktops` a `.category-grid`, contêiner que não resolveu no DOM observado. |
| Detalhes de Fiction | ✅ | ✅ | Ambos abriram o produto e validaram preço visível. |
| Limpar carrinho | ✅ | ✅ | Ambos adicionaram, removeram e validaram o carrinho vazio. |
| Limpar wishlist | ❌ | ❌ | O botão “Add to wishlist” resolveu dois elementos; faltou escopo ou ID específico nas duas versões. |
| Login inválido | ✅ | ✅ | Ambos validaram a permanência do usuário não autenticado. |
| Login válido | ✅ | ✅ | Ambos autenticaram e validaram os links de sessão. |
| Logout | ✅ | ✅ | Ambos encerraram a sessão corretamente. |
| Registrar usuário | ✅ | ❌ | O estruturado concluiu o registro e autenticou o usuário, mas depois procurou “Continue” como link; a interface expõe um botão. É falha técnica posterior ao objetivo principal. |
| Adicionar à wishlist | ❌ | ❌ | Baseline não resolveu o campo de busca após login; estruturado adicionou e recebeu a notificação, mas não encontrou o item com o locator usado na página da wishlist. |

## Avaliação das falhas

### Baseline

- **Ambiguidade de seletor:** adicionar ao carrinho e limpar wishlist.
- **Timeout de locator/estado:** checkout, configurar desktop e adicionar à wishlist.
- **Falhas de sintaxe:** nenhuma.
- **Falhas de ambiente após fornecer credenciais:** nenhuma.

### Contexto estruturado

- **Ambiguidade de seletor:** limpar wishlist.
- **Timeout ou asserção sobre estado/locator:** checkout, configurar desktop, registro e adicionar à wishlist.
- **Falhas de sintaxe:** nenhuma.
- **Falhas de ambiente após fornecer credenciais:** nenhuma.

## Interpretação

Os resultados mostram que o contexto estruturado aumentou duas medidas estáticas específicas: a proporção de chamadas `getBy*` e a cobertura de textos no grafo. Não se atribui a essas diferenças, nesta etapa, melhoria de qualidade, robustez ou resiliência. A executabilidade observada ficou igual nas duas condições.

Há dois efeitos opostos nos cenários divergentes. Em “adicionar ao carrinho”, o ID específico fornecido pelo contexto evitou a ambiguidade presente no baseline. Em “registrar usuário”, o baseline foi mais simples e passou, enquanto o estruturado adicionou um passo posterior desnecessário e usou o papel `link` em vez de `button`.

As métricas estáticas não funcionam como oráculo de robustez. O teste estruturado de configuração de desktop recebeu a classificação heurística “baixo” e possui alta proporção de chamadas `getBy*`, mas falhou porque o escopo `.category-grid` não correspondia ao contêiner real. Da mesma forma, a cobertura de URL de 100% não impediu falhas dentro das páginas corretas.

## Próxima etapa: avaliação de resiliência

Para medir resiliência, serão produzidas versões controladamente modificadas das páginas. As categorias de mutação, o elemento-alvo e o comportamento funcional preservado deverão ser definidos antes da execução. Os mesmos testes das duas condições serão então reexecutados, permitindo medir, sem inferência a partir de métricas estáticas:

- quantidade e proporção de locators que continuam identificando o elemento correto;
- testes que permanecem executáveis após cada tipo de mudança;
- quebras, falsos positivos e esforço necessário de manutenção;
- estabilidade em execuções repetidas.

## Fundamentação da etapa de resiliência

- Hammoudi, M.; Rothermel, G.; Tonella, P. *Why Do Record/Replay Tests of Web Applications Break?* ICST, 2016. DOI: [10.1109/ICST.2016.16](https://doi.org/10.1109/ICST.2016.16).
- Leotta, M.; Stocco, A.; Ricca, F.; Tonella, P. *Using Multi-Locators to Increase the Robustness of Web Test Cases.* ICST, 2015. DOI: [10.1109/ICST.2015.7102611](https://doi.org/10.1109/ICST.2015.7102611).
- Leotta, M.; Stocco, A.; Ricca, F.; Tonella, P. *Robula+: an algorithm for generating robust XPath locators for web testing.* Journal of Software: Evolution and Process, 2016. DOI: [10.1002/smr.1771](https://doi.org/10.1002/smr.1771).
- Playwright. *Locators* e *Best Practices*. Documentação oficial: [locators](https://playwright.dev/docs/locators) e [best practices](https://playwright.dev/docs/best-practices). A documentação sustenta a recomendação técnica da ferramenta, mas não substitui a validação empírica desta pesquisa.

## Limitações

- Cada caso foi executado uma vez; não foi medida flakiness.
- O Demo Web Shop é público e mutável, portanto estado e conteúdo podem variar.
- Os cenários de checkout dependem do estado de endereço da conta e do fluxo AJAX da aplicação.
- A conta e os dados usados são descartáveis; não representam um ambiente controlado dedicado.
- “Passou” comprova somente o comportamento observado nesta execução, não a correção semântica completa em relação à especificação original.
- A regra interna que classifica risco pelo percentual de chamadas `getBy*`, ausência de XPath e ausência de `waitForTimeout` é heurística e não foi validada como medida de resiliência.
- Nenhuma página foi modificada nesta etapa; portanto, não houve observação de comportamento dos testes diante da evolução da interface.
