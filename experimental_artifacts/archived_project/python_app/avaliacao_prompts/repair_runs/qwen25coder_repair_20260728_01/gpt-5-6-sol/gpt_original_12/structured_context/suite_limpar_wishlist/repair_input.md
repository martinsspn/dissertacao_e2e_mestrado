Condição experimental: structured_context

ESPECIFICAÇÃO ORIGINAL:
Removal of all products from the wishlist: The user is authenticated with valid credentials provided by the testing environment. The user adds a Camera product to the wishlist to prepare the scenario. The user accesses Wishlist. The user marks the Camera product for removal. The user selects Update wishlist. The system displays the empty wishlist.


ARQUIVO GERADO QUE DEVE SER REPARADO:
```typescript
import { test, expect } from '@playwright/test';

const email = process.env.DEMO_WEB_SHOP_EMAIL;
const password = process.env.DEMO_WEB_SHOP_PASSWORD;

test.describe('Suite Limpar Wishlist', () => {
  test('remove o produto Camera e exibe a wishlist vazia', async ({ page }) => {
    test.skip(
      !email || !password,
      'Defina DEMO_WEB_SHOP_EMAIL e DEMO_WEB_SHOP_PASSWORD com credenciais válidas.',
    );

    await page.goto('https://demowebshop.tricentis.com/');

    await page.getByRole('link', { name: 'Log in', exact: true }).click();
    await page.locator('#Email').fill(email!);
    await page.locator('#Password').fill(password!);
    await page.getByRole('button', { name: 'Log in', exact: true }).click();

    await expect(
      page.getByRole('link', { name: email!, exact: true }),
    ).toBeVisible();

    await page.locator('#small-searchterms').fill('Camera');
    await page.getByRole('button', { name: 'Search', exact: true }).click();

    const cameraProductLink = page
      .locator('h2.product-title')
      .getByRole('link')
      .filter({ hasText: 'Camera' });

    await expect(cameraProductLink).toHaveCount(1);
    await expect(cameraProductLink).toBeVisible();

    const cameraProductName = (
      await cameraProductLink.textContent()
    )?.trim();

    expect(cameraProductName).toBeTruthy();

    await cameraProductLink.click();

    await expect(
      page.getByRole('heading', {
        name: cameraProductName!,
        exact: true,
      }),
    ).toBeVisible();

    await page
      .getByRole('button', { name: 'Add to wishlist', exact: true })
      .click();

    const notification = page.locator('#bar-notification');

    await expect(notification).toBeVisible();
    await expect(notification).toContainText(
      'The product has been added to your wishlist',
    );

    await page
      .getByRole('link', { name: 'Wishlist', exact: true })
      .click();

    await expect(page).toHaveURL(
      'https://demowebshop.tricentis.com/wishlist',
    );
    await expect(
      page.getByRole('heading', { name: 'Wishlist', exact: true }),
    ).toBeVisible();

    const cameraWishlistItem = page
      .locator('tr.cart-item-row')
      .filter({
        has: page.getByRole('link', {
          name: cameraProductName!,
          exact: true,
        }),
      });

    await expect(cameraWishlistItem).toBeVisible();

    const removeCheckbox = cameraWishlistItem.locator(
      'input[type="checkbox"][name="removefromcart"]',
    );

    await removeCheckbox.check();
    await expect(removeCheckbox).toBeChecked();

    await page
      .getByRole('button', {
        name: 'Update wishlist',
        exact: true,
      })
      .click();

    await expect(
      page.getByText('The wishlist is empty!', { exact: true }),
    ).toBeVisible();

    await expect(cameraWishlistItem).toHaveCount(0);
  });
});

```

EVIDÊNCIA DA FALHA DE EXECUÇÃO:
Falha registrada sem mensagem detalhada.

DIAGNÓSTICO DA REVISÃO:
Cobre autenticação, preparação, remoção e estado vazio; Add to wishlist permanece ambíguo.

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


Faça uma única tentativa de reparo. Mantenha todas as verificações exigidas e devolva o arquivo TypeScript completo.