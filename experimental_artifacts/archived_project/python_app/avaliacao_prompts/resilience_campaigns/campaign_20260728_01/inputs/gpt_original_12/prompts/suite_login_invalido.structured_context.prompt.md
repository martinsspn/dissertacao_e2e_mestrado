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

Especificacao `Suite Login Invalido` em etapas:
1. The user accesses the Log in page of the Demo Web Shop.
2. The user fills in Email with the email of an existing account and Password with an invalid password provided by the testing environment.
3. The user submits the login form.
4. The system keeps the user unauthenticated and informs that the login was not completed.

Contexto estruturado por etapa:
Etapa 1 (R1):
- pagina=https://demowebshop.tricentis.com/
- controle=tag=a, text=Log in, href=/login
- operacao=click
- destino=https://demowebshop.tricentis.com/login
- seletor=text:Log in
- resultado_observado=Welcome, Please Sign In!
Etapa 2 (R2):
- pagina=https://demowebshop.tricentis.com/login
- controle_1=tag=input, label=Email:, id=Email, name=Email, input_type=text, form_action=/login, form_method=POST
- operacao_1=fill
- seletor_1=label:Email:
- controle_2=tag=input, label=Password:, id=Password, name=Password, input_type=password, form_action=/login, form_method=POST
- operacao_2=fill
- seletor_2=label:Password:
Etapa 3 (R3):
- pagina=https://demowebshop.tricentis.com/login
- controle=tag=input, input_type=submit, value=Log in, form_action=/login, form_method=POST
- operacao=click
- seletor=role_name:Log in
Etapas sem contexto observado: 4.

Use as informacoes observadas quando forem aplicaveis, sem limitar o teste a elas.
`pagina_evidencia` nao comprova uma transicao ate a pagina.
Sem contexto, siga a especificacao e interaja normalmente com a pagina; nao trate inferencias como fatos observados.
