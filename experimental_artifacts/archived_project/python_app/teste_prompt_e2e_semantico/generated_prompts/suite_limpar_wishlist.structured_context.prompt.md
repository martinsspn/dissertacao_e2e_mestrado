# Geracao de teste E2E Playwright

Gere um teste TypeScript Playwright fiel a especificacao.

Regras:
- Retorne um unico bloco de codigo `typescript`, sem texto fora dele; o conteudo interno deve ser um arquivo Playwright `.spec.ts` completo e executavel por `npx playwright test`.
- Importe `test` e `expect` de `@playwright/test`.
- Inicie com `await page.goto('https://demowebshop.tricentis.com/')`; use URLs literais tambem em `toHaveURL`, sem regex ou links Markdown.
- Nao derive rotas do texto de links, produtos ou titulos. Use `toHaveURL` somente quando a URL exata estiver na base ou no contexto; sem URL observada, confirme a pagina por elementos visiveis.
- Use locators Playwright legiveis e unicos no modo estrito; evite XPath, indices e `waitForTimeout`.
- Quando o contexto fornecer `id`, `data-testid` ou um locator Playwright exato, preserve esse seletor; nao o substitua por um locator generico baseado apenas em papel e nome.
- Quando varios itens ou variantes compartilharem a mesma acao, relacione o controle escolhido ao nome visivel do item antes do clique e reutilize esse nome nas verificacoes posteriores; nao trate o titulo da pagina agrupadora como nome do item sem confirmar essa igualdade. Se o nome exato nao puder ser observado, verifique apenas a propriedade explicitada pela especificacao, sem inventar um rotulo.
- Inclua assercoes observaveis que comprovem o resultado esperado.
- O contexto é apenas um guia: combine-o com a especificacao e sua experiencia para navegar, localizar elementos e executar as acoes.
- Caso seja possível acessar a aplicação, entre nela e interaja validando o fluxo e os resultados e utilizando as informações obtidas nessa interação em conjunto do contexto e a especificacao e seu conhecimento de playwright para fazer o teste ts; caso contrario, use a especificacao, o contexto observado e seu conhecimento de Playwright sem afirmar que executou acoes.

Especificacao `Suite Limpar Wishlist` em etapas:
1. The user is authenticated with valid credentials provided by the testing environment.
2. The user adds a Camera product to the wishlist to prepare the scenario.
3. The user accesses Wishlist.
4. The user marks the Camera product for removal.
5. The user selects Update wishlist.
6. The system displays the empty wishlist.

Contexto estruturado por etapa:
Etapa 3 (R3):
- pagina=https://demowebshop.tricentis.com/
- controle=tag=a, text=Wishlist, href=/wishlist
- operacao=click
- destino=https://demowebshop.tricentis.com/wishlist
- seletor=page.getByRole('link', { name: 'Wishlist', exact: true })
- pagina_evidencia=https://demowebshop.tricentis.com/wishlist
- evidencia_pagina=h1:Wishlist
Etapas sem contexto observado: 1, 2, 4, 5, 6.

Use as informacoes observadas quando forem aplicaveis, sem limitar o teste a elas.
`pagina_evidencia` nao comprova uma transicao ate a pagina.
Sem contexto, siga a especificacao e interaja normalmente com a pagina; nao trate inferencias como fatos observados.
