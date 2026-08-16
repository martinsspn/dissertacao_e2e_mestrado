Condição experimental: structured_context

ESPECIFICAÇÃO ORIGINAL:
Login with valid credentials: The user accesses the Log in page of the Demo Web Shop. The user fills in Email and Password with the valid credentials provided by the testing environment. The user submits the login form. The system authenticates the user and displays the account and Log out links.


ARQUIVO GERADO QUE DEVE SER REPARADO:
```typescript
import { test, expect } from '@playwright/test';

test.describe('Suite Login Valido', () => {
  test('should log in with valid credentials and display account links', async ({ page }) => {
    // Etapa 1: Acessar a página de login
    await page.goto('https://demowebshop.tricentis.com/');
    await page.getByText("Log in", { exact: true }).first().click();
    expect(page).toHaveURL('https://demowebshop.tricentis.com/login');
    expect(await page.textContent('.title')).toBe('Welcome, Please Sign In!');

    // Etapa 2: Preencher os campos de email e senha
    await page.getByLabel("Email:", { exact: true }).fill(process.env.EMAIL || 'test@example.com');
    await page.getByLabel("Password:", { exact: true }).fill(process.env.PASSWORD || 'password123');

    // Etapa 3: Submeter o formulário de login
    await page.getByRole("button", { name: "Log in", exact: true }).click();
    expect(page).toHaveURL('https://demowebshop.tricentis.com/');

    // Verificar se os links da conta e logout estão presentes
    expect(await page.isVisible('.account')).toBe(true);
    expect(await page.isVisible('a[href="/logout"]')).toBe(true);
  });
});

```

EVIDÊNCIA DA FALHA DE EXECUÇÃO:
Error: expect(received).toBe(expected) // Object.is equality

- Expected  - 1
+ Received  + 3

- Welcome, Please Sign In!
+
+             Categories
+

DIAGNÓSTICO DA REVISÃO:
Locators e credenciais são adequados; uma asserção inventada sobre .title interrompe o fluxo.

PROMPT ESTRUTURADO ORIGINAL DESTA CONDIÇÃO:
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

Especificacao `Suite Login Valido` em etapas:
1. The user accesses the Log in page of the Demo Web Shop.
2. The user fills in Email and Password with the valid credentials provided by the testing environment.
3. The user submits the login form.
4. The system authenticates the user and displays the account and Log out links.

Contexto estruturado por etapa:
Etapa 1 (R1):
- pagina=https://demowebshop.tricentis.com/
- controle=tag=a, text=Log in, href=/login
- operacao=click
- destino=https://demowebshop.tricentis.com/login
- locator_playwright=page.getByText("Log in", { exact: true }).first()
- resultado_observado=Welcome, Please Sign In!
Etapa 2 (R2):
- pagina=https://demowebshop.tricentis.com/login
- controle_1=tag=input, label=Email:, id=Email, name=Email, input_type=text, form_action=/login, form_method=POST
- operacao_1=fill
- locator_playwright_1=page.getByLabel("Email:", { exact: true })
- controle_2=tag=input, label=Password:, id=Password, name=Password, input_type=password, form_action=/login, form_method=POST
- operacao_2=fill
- locator_playwright_2=page.getByLabel("Password:", { exact: true })
Etapa 3 (R3):
- pagina=https://demowebshop.tricentis.com/login
- controle=tag=input, input_type=submit, value=Log in, form_action=/login, form_method=POST
- operacao=click
- locator_playwright=page.getByRole("button", { name: "Log in", exact: true })
Etapas sem contexto observado: 4.

Use as informacoes observadas quando forem aplicaveis, sem limitar o teste a elas.
`pagina_evidencia` nao comprova uma transicao ate a pagina.
Sem contexto, siga a especificacao e interaja normalmente com a pagina; nao trate inferencias como fatos observados.


Faça uma única tentativa de reparo. Mantenha todas as verificações exigidas e devolva o arquivo TypeScript completo.