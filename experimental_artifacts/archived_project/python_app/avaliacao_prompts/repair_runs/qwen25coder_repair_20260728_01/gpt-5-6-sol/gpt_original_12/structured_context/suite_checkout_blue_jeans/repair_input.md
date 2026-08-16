Condição experimental: structured_context

ESPECIFICAÇÃO ORIGINAL:
Complete purchase of the product Blue Jeans: The user is authenticated in an account with a valid billing and shipping address, using data provided by the testing environment. The user searches for Blue Jeans and opens the product page. The user adds Blue Jeans to the cart. The user accesses Shopping cart and confirms that the product is present. The user accepts the Terms of service and selects Checkout. The user confirms or provides valid Billing address data. The user confirms or provides valid Shipping address data. The user selects an available Shipping method option. The user selects an available Payment method option. The user reviews Payment information and proceeds. The user reviews the order and selects Confirm. The system informs that the order was processed successfully.


ARQUIVO GERADO QUE DEVE SER REPARADO:
```typescript
import { test, expect, Page, Locator } from '@playwright/test';

const email = process.env.DEMO_WEB_SHOP_EMAIL;
const password = process.env.DEMO_WEB_SHOP_PASSWORD;

async function selectFirstAvailableOption(options: Locator): Promise<void> {
  const optionCount = await options.count();

  for (let index = 0; index < optionCount; index += 1) {
    const option = options.nth(index);

    if (await option.isEnabled()) {
      await option.check();
      return;
    }
  }

  throw new Error('Nenhuma opção disponível foi encontrada.');
}

async function continueCheckoutStep(
  page: Page,
  containerSelector: string,
): Promise<void> {
  const container = page.locator(containerSelector);
  await expect(container).toBeVisible();

  const continueButton = container.getByRole('button', {
    name: 'Continue',
    exact: true,
  });

  await expect(continueButton).toBeEnabled();
  await continueButton.click();
}

test.describe('Suite Checkout Blue Jeans', () => {
  test('finaliza a compra de Blue Jeans', async ({ page }) => {
    test.skip(
      !email || !password,
      'Defina DEMO_WEB_SHOP_EMAIL e DEMO_WEB_SHOP_PASSWORD com uma conta que possua endereços válidos.',
    );

    await page.goto('https://demowebshop.tricentis.com/');

    await page.getByRole('link', { name: 'Log in', exact: true }).click();
    await page.locator('#Email').fill(email!);
    await page.locator('#Password').fill(password!);
    await page.getByRole('button', { name: 'Log in', exact: true }).click();

    await expect(
      page.getByRole('link', { name: email!, exact: true }),
    ).toBeVisible();

    await page.locator('#small-searchterms').fill('Blue Jeans');
    await page.getByRole('button', { name: 'Search', exact: true }).click();

    const blueJeansResult = page
      .locator('.product-item')
      .filter({
        has: page.getByRole('link', {
          name: 'Blue Jeans',
          exact: true,
        }),
      });

    await expect(blueJeansResult).toBeVisible();

    const blueJeansResultLink = blueJeansResult.getByRole('link', {
      name: 'Blue Jeans',
      exact: true,
    });

    await expect(blueJeansResultLink).toBeVisible();
    await blueJeansResultLink.click();

    await expect(page).toHaveURL(
      'https://demowebshop.tricentis.com/blue-jeans',
    );
    await expect(
      page.getByRole('heading', { name: 'Blue Jeans', exact: true }),
    ).toBeVisible();

    await page.locator('#add-to-cart-button-36').click();

    const notification = page.locator('#bar-notification');
    await expect(notification).toBeVisible();
    await expect(notification).toContainText(
      'The product has been added to your shopping cart',
    );

    await page
      .getByRole('link', { name: 'Shopping cart', exact: true })
      .click();

    await expect(page).toHaveURL('https://demowebshop.tricentis.com/cart');
    await expect(
      page.getByRole('heading', { name: 'Shopping cart', exact: true }),
    ).toBeVisible();

    const blueJeansCartItem = page
      .locator('tr.cart-item-row')
      .filter({
        has: page.getByRole('link', {
          name: 'Blue Jeans',
          exact: true,
        }),
      });

    await expect(blueJeansCartItem).toBeVisible();
    await expect(
      blueJeansCartItem.getByRole('link', {
        name: 'Blue Jeans',
        exact: true,
      }),
    ).toBeVisible();

    await page.locator('#termsofservice').check();
    await expect(page.locator('#termsofservice')).toBeChecked();
    await page.locator('#checkout').click();

    const billingAddressSelect = page.locator('#billing-address-select');

    if (await billingAddressSelect.isVisible()) {
      const selectedBillingAddress =
        await billingAddressSelect.locator('option:checked').textContent();

      expect(selectedBillingAddress?.trim()).toBeTruthy();
    }

    await continueCheckoutStep(page, '#billing-buttons-container');

    const shippingAddressSelect = page.locator('#shipping-address-select');

    if (await shippingAddressSelect.isVisible()) {
      const selectedShippingAddress =
        await shippingAddressSelect.locator('option:checked').textContent();

      expect(selectedShippingAddress?.trim()).toBeTruthy();
    }

    await continueCheckoutStep(page, '#shipping-buttons-container');

    const shippingMethods = page.locator(
      '#checkout-shipping-method-load input[type="radio"]',
    );

    await expect(shippingMethods.first()).toBeVisible();
    await selectFirstAvailableOption(shippingMethods);
    await expect(shippingMethods.filter({ has: page.locator(':checked') })).toHaveCount(1);
    await continueCheckoutStep(page, '#shipping-method-buttons-container');

    const paymentMethods = page.locator(
      '#checkout-payment-method-load input[type="radio"]',
    );

    await expect(paymentMethods.first()).toBeVisible();
    await selectFirstAvailableOption(paymentMethods);
    await expect(paymentMethods.filter({ has: page.locator(':checked') })).toHaveCount(1);
    await continueCheckoutStep(page, '#payment-method-buttons-container');

    const paymentInformation = page.locator(
      '#checkout-payment-info-load',
    );

    await expect(paymentInformation).toBeVisible();
    await continueCheckoutStep(page, '#payment-info-buttons-container');

    const orderReview = page.locator('#checkout-confirm-order-load');
    await expect(orderReview).toBeVisible();
    await expect(
      orderReview.getByRole('link', {
        name: 'Blue Jeans',
        exact: true,
      }),
    ).toBeVisible();

    const confirmButton = page
      .locator('#confirm-order-buttons-container')
      .getByRole('button', { name: 'Confirm', exact: true });

    await expect(confirmButton).toBeEnabled();
    await confirmButton.click();

    await expect(
      page.getByRole('heading', {
        name: 'Thank you',
        exact: true,
      }),
    ).toBeVisible();

    await expect(
      page.getByText(
        'Your order has been successfully processed!',
        { exact: true },
      ),
    ).toBeVisible();
  });
});

```

EVIDÊNCIA DA FALHA DE EXECUÇÃO:
Falha registrada sem mensagem detalhada.

DIAGNÓSTICO DA REVISÃO:
Cobre o checkout completo, mas presume visibilidade imediata dos contêineres de endereço.

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


Faça uma única tentativa de reparo. Mantenha todas as verificações exigidas e devolva o arquivo TypeScript completo.