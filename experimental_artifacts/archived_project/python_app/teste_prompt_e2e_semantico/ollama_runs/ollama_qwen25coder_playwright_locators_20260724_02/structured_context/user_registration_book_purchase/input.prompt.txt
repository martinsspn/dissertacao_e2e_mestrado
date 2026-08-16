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

Especificacao `User Registration Book Purchase` em etapas:
1. The user accesses the Demo Web Shop website.
2. The user clicks on the Register link to access the registration page.
3. The system displays the registration form.
4. The user fills in the email field with a valid email.
5. The user fills in the password field with a secure password.
6. The user confirms the password by typing it again.
7. The user fills in the First Name field with their first name.
8. The user fills in the Last Name field with their last name.
9. The user clicks on the Register button to complete the registration.
10. The system validates the data and registers the user automatically.
11. The user remains logged in after registration.
12. The user is redirected to the home page.
13. The user clicks on the Books menu or link to access the book list.
14. The system displays the catalog page of available books.
15. The user locates and clicks on the book Health Book to open its details page.
16. The system displays the product page with description, price, and purchase options.
17. The user clicks on the Add to cart button to add the book to the cart.
18. The system confirms that the product has been added to the cart (success notification).
19. The user navigates to the shopping cart to check the added item.
20. The system displays the cart containing the book Health Book with quantity and price.
21. The user verifies that the book was successfully added to the cart.

Contexto estruturado por etapa:
Etapa 1 (R1):
- pagina_evidencia=https://demowebshop.tricentis.com/
- evidencia_pagina=title:Demo Web Shop
Etapa 2 (R2):
- pagina=https://demowebshop.tricentis.com/
- controle=tag=a, text=Register, href=/register
- operacao=click
- destino=https://demowebshop.tricentis.com/register
- locator_playwright=page.getByText("Register", { exact: true }).first()
- pagina_evidencia=https://demowebshop.tricentis.com/register
- evidencia_pagina=h1:Register
Etapa 4 (R4):
- pagina=https://demowebshop.tricentis.com/register
- controle=tag=input, label=Email:, id=Email, name=Email, input_type=text, form_action=/register, form_method=POST
- operacao=fill
- locator_playwright=page.getByLabel("Email:", { exact: true })
Etapa 5 (R5):
- pagina=https://demowebshop.tricentis.com/register
- controle=tag=input, label=Password:, id=Password, name=Password, input_type=password, form_action=/register, form_method=POST
- operacao=fill
- locator_playwright=page.getByLabel("Password:", { exact: true })
Etapa 6 (R6):
- pagina=https://demowebshop.tricentis.com/register
- controle=tag=input, label=Confirm password:, id=ConfirmPassword, name=ConfirmPassword, input_type=password, form_action=/register, form_method=POST
- operacao=fill
- locator_playwright=page.getByLabel("Confirm password:", { exact: true })
Etapa 7 (R7):
- pagina=https://demowebshop.tricentis.com/register
- controle=tag=input, label=First name:, id=FirstName, name=FirstName, input_type=text, form_action=/register, form_method=POST
- operacao=fill
- locator_playwright=page.getByLabel("First name:", { exact: true })
Etapa 8 (R8):
- pagina=https://demowebshop.tricentis.com/register
- controle=tag=input, label=Last name:, id=LastName, name=LastName, input_type=text, form_action=/register, form_method=POST
- operacao=fill
- locator_playwright=page.getByLabel("Last name:", { exact: true })
Etapa 9 (R9):
- pagina=https://demowebshop.tricentis.com/register
- controle=tag=input, id=register-button, name=register-button, input_type=submit, value=Register, form_action=/register, form_method=POST
- operacao=click
- locator_playwright=page.locator("[id=\"register-button\"]")
Etapa 13 (R13):
- pagina=https://demowebshop.tricentis.com/register
- controle=tag=a, text=Books, href=/books
- operacao=click
- destino=https://demowebshop.tricentis.com/books
- locator_playwright=page.getByText("Books", { exact: true }).first()
- pagina_evidencia=https://demowebshop.tricentis.com/books
- evidencia_pagina=h1:Books
Etapa 15 (R15):
- pagina=https://demowebshop.tricentis.com/books
- controle=tag=a, text=Health Book, href=/health
- operacao=click
- destino=https://demowebshop.tricentis.com/health
- locator_playwright=page.getByText("Health Book", { exact: true }).first()
- pagina_evidencia=https://demowebshop.tricentis.com/health
- evidencia_pagina=h1:Health Book
Etapa 17 (R17):
- pagina=https://demowebshop.tricentis.com/health
- controle=tag=input, id=add-to-cart-button-22, input_type=button, value=Add to cart, form_action=/health, form_method=POST
- operacao=click
- locator_playwright=page.locator("[id=\"add-to-cart-button-22\"]")
Etapa 19 (R19):
- pagina=https://demowebshop.tricentis.com/health
- controle=tag=a, text=Shopping cart, href=/cart
- operacao=click
- destino=https://demowebshop.tricentis.com/cart
- locator_playwright=page.getByRole("link", { name: "Shopping cart", exact: true })
- pagina_evidencia=https://demowebshop.tricentis.com/cart
- evidencia_pagina=h1:Shopping cart
Etapas sem contexto observado: 3, 10, 11, 12, 14, 16, 18, 20, 21.

Use as informacoes observadas quando forem aplicaveis, sem limitar o teste a elas.
`pagina_evidencia` nao comprova uma transicao ate a pagina.
Sem contexto, siga a especificacao e interaja normalmente com a pagina; nao trate inferencias como fatos observados.
