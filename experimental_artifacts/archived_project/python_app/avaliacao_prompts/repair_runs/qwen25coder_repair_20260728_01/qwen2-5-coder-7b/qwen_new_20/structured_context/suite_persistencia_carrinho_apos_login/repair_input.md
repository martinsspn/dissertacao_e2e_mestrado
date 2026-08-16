Condição experimental: structured_context

ESPECIFICAÇÃO ORIGINAL:
Persistence of an authenticated user's cart: The user is authenticated with valid credentials provided by the testing environment. The user ensures that the cart does not contain Computing and Internet and then adds that product to the cart. The user logs out and logs in again with the same account. The user accesses Shopping cart. The system still displays Computing and Internet in the cart. At the end, the user removes the product to restore the account state.


ARQUIVO GERADO QUE DEVE SER REPARADO:
```typescript
import { test, expect } from '@playwright/test';

test.describe('Suite Persistencia Carrinho Apos Login', () => {
  test('should persist cart items after login', async ({ page }) => {
    // Etapa 1: Autenticação com credenciais válidas
    await page.goto('https://demowebshop.tricentis.com/');
    await page.getByText("Log in", { exact: true }).first().click();
    await page.fill('input[name="Email"]', process.env.TEST_EMAIL);
    await page.fill('input[name="Password"]', process.env.TEST_PASSWORD);
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/');

    // Etapa 2: Adicionar produto ao carrinho
    await page.goto('https://demowebshop.tricentis.com/');
    await page.getByRole('link', { name: 'Computing and Internet' }).click();
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/cart');

    // Etapa 3: Logout e login novamente
    await page.goto('https://demowebshop.tricentis.com/');
    await page.getByText("Log in", { exact: true }).first().click();
    await page.fill('input[name="Email"]', process.env.TEST_EMAIL);
    await page.fill('input[name="Password"]', process.env.TEST_PASSWORD);
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/');

    // Etapa 4: Acessar carrinho
    await page.goto('https://demowebshop.tricentis.com/');
    await page.getByRole('link', { name: 'Shopping cart' }).click();
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/cart');

    // Etapa 5: Verificar persistência do carrinho
    await expect(page.getByText('Computing and Internet')).toBeVisible();

    // Etapa 6: Remover produto para restaurar o estado da conta
    await page.click('button[name="removefromcart"]');
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/cart');
    await expect(page.getByText('Computing and Internet')).not.toBeVisible();
  });
});

```

EVIDÊNCIA DA FALHA DE EXECUÇÃO:
Error: page.fill: value: expected string, got undefined

DIAGNÓSTICO DA REVISÃO:
Não limpa o estado inicial nem faz logout; tenta abrir Log in enquanto a sessão continua autenticada.

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

Especificacao `Suite Persistencia Carrinho Apos Login` em etapas:
1. The user is authenticated with valid credentials provided by the testing environment.
2. The user ensures that the cart does not contain Computing and Internet and then adds that product to the cart.
3. The user logs out and logs in again with the same account.
4. The user accesses Shopping cart.
5. The system still displays Computing and Internet in the cart.
6. At the end, the user removes the product to restore the account state.

Contexto estruturado por etapa:
Etapa 3 (R3):
- pagina=https://demowebshop.tricentis.com/
- controle=tag=a, text=Log in, href=/login
- operacao=click
- destino=https://demowebshop.tricentis.com/login
- locator_playwright=page.getByText("Log in", { exact: true }).first()
- resultado_observado=Welcome, Please Sign In!
Etapa 4 (R4):
- pagina=https://demowebshop.tricentis.com/login
- controle=tag=a, text=Shopping cart, href=/cart
- operacao=click
- destino=https://demowebshop.tricentis.com/cart
- locator_playwright=page.getByRole("link", { name: "Shopping cart", exact: true })
- pagina_evidencia=https://demowebshop.tricentis.com/cart
- evidencia_pagina=h1:Shopping cart
Etapas sem contexto observado: 1, 2, 5, 6.

Use as informacoes observadas quando forem aplicaveis, sem limitar o teste a elas.
`pagina_evidencia` nao comprova uma transicao ate a pagina.
Sem contexto, siga a especificacao e interaja normalmente com a pagina; nao trate inferencias como fatos observados.


Faça uma única tentativa de reparo. Mantenha todas as verificações exigidas e devolva o arquivo TypeScript completo.