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

Especificacao `Suite Checkout Blue Jeans` em etapas:
1. The user is authenticated in an account with a valid billing and shipping address, using data provided by the testing environment.
2. The user searches for Blue Jeans and opens the product page.
3. The user adds Blue Jeans to the cart.
4. The user accesses Shopping cart and confirms that the product is present.
5. The user accepts the Terms of service and selects Checkout.
6. The user confirms or provides valid Billing address data.
7. The user confirms or provides valid Shipping address data.
8. The user selects an available Shipping method option.
9. The user selects an available Payment method option.
10. The user reviews Payment information and proceeds.
11. The user reviews the order and selects Confirm.
12. The system informs that the order was processed successfully.

Contexto estruturado por etapa:
Etapa 2 (R2):
- pagina=https://demowebshop.tricentis.com/
- controle_1=tag=input, id=small-searchterms, name=q, input_type=text, value=Search store, form_action=/search, form_method=GET
- operacao_1=fill
- seletor_1=id:small-searchterms
- controle_2=tag=input, input_type=submit, value=Search, form_action=/search, form_method=GET
- operacao_2=click
- seletor_2=role_name:Search
- pagina_evidencia=https://demowebshop.tricentis.com/blue-jeans
- evidencia_pagina=h1:Blue Jeans
Etapa 3 (R3):
- pagina=https://demowebshop.tricentis.com/blue-jeans
- controle=tag=input, id=add-to-cart-button-36, input_type=button, value=Add to cart, form_action=/blue-jeans, form_method=POST
- operacao=click
- seletor=id:add-to-cart-button-36
Etapa 4 (R4):
- pagina=https://demowebshop.tricentis.com/blue-jeans
- controle=tag=a, text=Shopping cart, href=/cart
- operacao=click
- destino=https://demowebshop.tricentis.com/cart
- seletor=page.getByRole('link', { name: 'Shopping cart', exact: true })
- pagina_evidencia=https://demowebshop.tricentis.com/cart
- evidencia_pagina=h1:Shopping cart
Etapas sem contexto observado: 1, 5, 6, 7, 8, 9, 10, 11, 12.

Use as informacoes observadas quando forem aplicaveis, sem limitar o teste a elas.
`pagina_evidencia` nao comprova uma transicao ate a pagina.
Sem contexto, siga a especificacao e interaja normalmente com a pagina; nao trate inferencias como fatos observados.
