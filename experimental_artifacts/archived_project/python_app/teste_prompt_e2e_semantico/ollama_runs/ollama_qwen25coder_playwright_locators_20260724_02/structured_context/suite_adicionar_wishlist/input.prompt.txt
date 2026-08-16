# Geracao de teste E2E Playwright

Gere um teste TypeScript Playwright fiel a especificacao.

Regras:
- Retorne um unico bloco de codigo `typescript`, sem texto fora dele; o conteudo interno deve ser um arquivo Playwright `.spec.ts` completo e executavel por `npx playwright test`.
- Importe `test` e `expect` de `@playwright/test`.
- Inicie com `await page.goto('https://demowebshop.tricentis.com/')`; use URLs literais tambem em `toHaveURL`, sem regex ou links Markdown.
- Nao derive rotas do texto de links, produtos ou titulos. Use `toHaveURL` somente quando a URL exata estiver na base ou no contexto; sem URL observada, confirme a pagina por elementos visiveis.
- Use locators Playwright legiveis e unicos no modo estrito; evite XPath, indices e `waitForTimeout`.
- Cada valor `locator_playwright=...` e uma expressao TypeScript Playwright completa e executavel. Copie a expressao sem aspas adicionais e aplique a acao nela, por exemplo `await page.getByRole('button', { name: 'Search', exact: true }).click()` ou `await page.getByLabel('Email:', { exact: true }).fill(valor)`.
- Nunca passe uma expressao `page.getBy*` ou `page.locator` como argumento de `page.click`, `page.fill` ou `page.selectOption`; chame `.click()`, `.fill()` ou `.selectOption()` diretamente no locator.
- Nao use no codigo a notacao descritiva de `controle=...` nem invente engines como `role_name:`, `label:`, `id:`, `tag=` ou `text:`. Somente os valores de `locator_playwright=...` sao locators copiaveis.
- Quando o contexto fornecer `locator_playwright`, preserve esse locator; nao o substitua por um locator generico baseado apenas em papel e nome.
- Quando varios itens ou variantes compartilharem a mesma acao, relacione o controle escolhido ao nome visivel do item antes do clique e reutilize esse nome nas verificacoes posteriores; nao trate o titulo da pagina agrupadora como nome do item sem confirmar essa igualdade. Se o nome exato nao puder ser observado, verifique apenas a propriedade explicitada pela especificacao, sem inventar um rotulo.
- Inclua assercoes observaveis que comprovem o resultado esperado.
- O contexto é apenas um guia: combine-o com a especificacao e sua experiencia para navegar, localizar elementos e executar as acoes.
- Caso seja possível acessar a aplicação, entre nela e interaja validando o fluxo e os resultados e utilizando as informações obtidas nessa interação em conjunto do contexto e a especificacao e seu conhecimento de playwright para fazer o teste ts; caso contrario, use a especificacao, o contexto observado e seu conhecimento de Playwright sem afirmar que executou acoes.

Especificacao `Suite Adicionar Wishlist` em etapas:
1. The user is authenticated with valid credentials provided by the testing environment.
2. The user searches for Camera in the Search store field.
3. The user opens a Camera product presented in the results.
4. The user selects Add to wishlist on the product page.
5. The system informs that the product has been added to the wishlist.
6. The user accesses Wishlist.
7. The system displays the Camera product in the wishlist.

Contexto estruturado por etapa:
Etapa 2 (R2):
- pagina=https://demowebshop.tricentis.com/
- controle_1=tag=input, id=small-searchterms, name=q, input_type=text, value=Search store, form_action=/search, form_method=GET
- operacao_1=fill
- locator_playwright_1=page.locator("[id=\"small-searchterms\"]")
- controle_2=tag=input, input_type=submit, value=Search, form_action=/search, form_method=GET
- operacao_2=click
- locator_playwright_2=page.getByRole("button", { name: "Search", exact: true })
Etapa 3 (R3):
- pagina_evidencia=https://demowebshop.tricentis.com/digital-slr-camera
- evidencia_pagina=h1:Digital SLR Camera 12.2 Mpixel
Etapa 4 (R4):
- pagina=https://demowebshop.tricentis.com/digital-slr-camera
- controle=tag=input, id=add-to-wishlist-button-18, input_type=button, value=Add to wishlist, form_action=/digital-slr-camera, form_method=POST
- operacao=click
- locator_playwright=page.locator("[id=\"add-to-wishlist-button-18\"]")
Etapa 6 (R6):
- pagina=https://demowebshop.tricentis.com/digital-slr-camera
- controle=tag=a, text=Wishlist, href=/wishlist
- operacao=click
- destino=https://demowebshop.tricentis.com/wishlist
- locator_playwright=page.getByRole("link", { name: "Wishlist", exact: true })
- pagina_evidencia=https://demowebshop.tricentis.com/wishlist
- evidencia_pagina=h1:Wishlist
Etapas sem contexto observado: 1, 5, 7.

Use as informacoes observadas quando forem aplicaveis, sem limitar o teste a elas.
`pagina_evidencia` nao comprova uma transicao ate a pagina.
Sem contexto, siga a especificacao e interaja normalmente com a pagina; nao trate inferencias como fatos observados.
