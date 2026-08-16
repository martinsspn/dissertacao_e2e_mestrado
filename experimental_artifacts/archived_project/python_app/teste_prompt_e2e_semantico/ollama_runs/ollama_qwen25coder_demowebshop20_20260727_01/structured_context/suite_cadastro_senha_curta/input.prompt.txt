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

Especificacao `Suite Cadastro Senha Curta` em etapas:
1. The user accesses the Register page.
2. The user fills in First name and Last name with valid data and Email with a unique address generated for this execution.
3. The user fills in Password and Confirm password with the same value containing fewer than six characters.
4. The user submits the form using the Register button.
5. The system does not register the user and informs that the password must contain at least six characters.

Contexto estruturado por etapa:
Etapa 1 (R1):
- pagina=https://demowebshop.tricentis.com/
- controle=tag=a, text=Register, href=/register
- operacao=click
- destino=https://demowebshop.tricentis.com/register
- locator_playwright=page.getByText("Register", { exact: true }).first()
- pagina_evidencia=https://demowebshop.tricentis.com/register
- evidencia_pagina=h1:Register
Etapa 2 (R2):
- pagina=https://demowebshop.tricentis.com/register
- controle_1=tag=input, label=First name:, id=FirstName, name=FirstName, input_type=text, form_action=/register, form_method=POST
- operacao_1=fill
- locator_playwright_1=page.getByLabel("First name:", { exact: true })
- controle_2=tag=input, label=Last name:, id=LastName, name=LastName, input_type=text, form_action=/register, form_method=POST
- operacao_2=fill
- locator_playwright_2=page.getByLabel("Last name:", { exact: true })
- controle_3=tag=input, label=Email:, id=Email, name=Email, input_type=text, form_action=/register, form_method=POST
- operacao_3=fill
- locator_playwright_3=page.getByLabel("Email:", { exact: true })
Etapa 3 (R3):
- pagina=https://demowebshop.tricentis.com/register
- controle_1=tag=input, label=Password:, id=Password, name=Password, input_type=password, form_action=/register, form_method=POST
- operacao_1=fill
- locator_playwright_1=page.getByLabel("Password:", { exact: true })
- controle_2=tag=input, label=Confirm password:, id=ConfirmPassword, name=ConfirmPassword, input_type=password, form_action=/register, form_method=POST
- operacao_2=fill
- locator_playwright_2=page.getByLabel("Confirm password:", { exact: true })
Etapa 4 (R4):
- pagina=https://demowebshop.tricentis.com/register
- controle=tag=input, id=register-button, name=register-button, input_type=submit, value=Register, form_action=/register, form_method=POST
- operacao=click
- locator_playwright=page.locator("[id=\"register-button\"]")
Etapas sem contexto observado: 5.

Use as informacoes observadas quando forem aplicaveis, sem limitar o teste a elas.
`pagina_evidencia` nao comprova uma transicao ate a pagina.
Sem contexto, siga a especificacao e interaja normalmente com a pagina; nao trate inferencias como fatos observados.
