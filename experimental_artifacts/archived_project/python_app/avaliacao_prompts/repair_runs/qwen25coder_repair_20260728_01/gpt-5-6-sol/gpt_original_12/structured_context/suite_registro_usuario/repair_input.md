Condição experimental: structured_context

ESPECIFICAÇÃO ORIGINAL:
Registration of a new user: The user accesses the Register page of the Demo Web Shop. The user selects a Gender option. The user fills in First name and Last name with valid data. The user fills in Email with a unique address generated for this execution. The user fills in Password and Confirm password with the same valid password. The user submits the form using the Register button. The system confirms that the registration has been completed. The user selects Continue and returns to the store authenticated.


ARQUIVO GERADO QUE DEVE SER REPARADO:
```typescript
import { test, expect } from '@playwright/test';

test.describe('Suite Registro Usuario', () => {
  test('registra um novo usuario e retorna autenticado para a loja', async ({
    page,
  }) => {
    const uniqueEmail = `playwright.${Date.now()}@example.com`;
    const password = 'ValidPassword123!';

    await page.goto('https://demowebshop.tricentis.com/');

    await page.getByRole('link', { name: 'Register', exact: true }).click();

    await expect(page).toHaveURL(
      'https://demowebshop.tricentis.com/register',
    );
    await expect(
      page.getByRole('heading', { name: 'Register', exact: true }),
    ).toBeVisible();

    const genderOption = page.locator('#gender-male');
    await genderOption.check();
    await expect(genderOption).toBeChecked();

    await page.getByLabel('First name:').fill('Playwright');
    await page.getByLabel('Last name:').fill('User');
    await page.getByLabel('Email:').fill(uniqueEmail);
    await page.getByLabel('Password:', { exact: true }).fill(password);
    await page.getByLabel('Confirm password:').fill(password);

    await page.locator('#register-button').click();

    await expect(
      page.getByText('Your registration completed', { exact: true }),
    ).toBeVisible();

    await expect(
      page.getByRole('link', { name: uniqueEmail, exact: true }),
    ).toBeVisible();
    await expect(
      page.getByRole('link', { name: 'Log out', exact: true }),
    ).toBeVisible();

    await page.getByRole('link', { name: 'Continue', exact: true }).click();

    await expect(
      page.getByRole('link', { name: uniqueEmail, exact: true }),
    ).toBeVisible();
    await expect(
      page.getByRole('link', { name: 'Log out', exact: true }),
    ).toBeVisible();
    await expect(
      page.getByRole('link', { name: 'Log in', exact: true }),
    ).toHaveCount(0);
  });
});

```

EVIDÊNCIA DA FALHA DE EXECUÇÃO:
Falha registrada sem mensagem detalhada.

DIAGNÓSTICO DA REVISÃO:
Conclui e confirma o cadastro, mas trata Continue como link em vez de botão.

PROMPT ESTRUTURADO ORIGINAL DESTA CONDIÇÃO:
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

Especificacao `Suite Registro Usuario` em etapas:
1. The user accesses the Register page of the Demo Web Shop.
2. The user selects a Gender option.
3. The user fills in First name and Last name with valid data.
4. The user fills in Email with a unique address generated for this execution.
5. The user fills in Password and Confirm password with the same valid password.
6. The user submits the form using the Register button.
7. The system confirms that the registration has been completed.
8. The user selects Continue and returns to the store authenticated.

Contexto estruturado por etapa:
Etapa 1 (R1):
- pagina=https://demowebshop.tricentis.com/
- controle=tag=a, text=Register, href=/register
- operacao=click
- destino=https://demowebshop.tricentis.com/register
- seletor=text:Register
- pagina_evidencia=https://demowebshop.tricentis.com/register
- evidencia_pagina=h1:Register
Etapa 3 (R3):
- pagina=https://demowebshop.tricentis.com/register
- controle_1=tag=input, label=First name:, id=FirstName, name=FirstName, input_type=text, form_action=/register, form_method=POST
- operacao_1=fill
- seletor_1=label:First name:
- controle_2=tag=input, label=Last name:, id=LastName, name=LastName, input_type=text, form_action=/register, form_method=POST
- operacao_2=fill
- seletor_2=label:Last name:
Etapa 4 (R4):
- pagina=https://demowebshop.tricentis.com/register
- controle=tag=input, label=Email:, id=Email, name=Email, input_type=text, form_action=/register, form_method=POST
- operacao=fill
- seletor=label:Email:
Etapa 5 (R5):
- pagina=https://demowebshop.tricentis.com/register
- controle_1=tag=input, label=Password:, id=Password, name=Password, input_type=password, form_action=/register, form_method=POST
- operacao_1=fill
- seletor_1=label:Password:
- controle_2=tag=input, label=Confirm password:, id=ConfirmPassword, name=ConfirmPassword, input_type=password, form_action=/register, form_method=POST
- operacao_2=fill
- seletor_2=label:Confirm password:
Etapa 6 (R6):
- pagina=https://demowebshop.tricentis.com/register
- controle=tag=input, id=register-button, name=register-button, input_type=submit, value=Register, form_action=/register, form_method=POST
- operacao=click
- seletor=id:register-button
Etapas sem contexto observado: 2, 7, 8.

Use as informacoes observadas quando forem aplicaveis, sem limitar o teste a elas.
`pagina_evidencia` nao comprova uma transicao ate a pagina.
Sem contexto, siga a especificacao e interaja normalmente com a pagina; nao trate inferencias como fatos observados.


Faça uma única tentativa de reparo. Mantenha todas as verificações exigidas e devolva o arquivo TypeScript completo.