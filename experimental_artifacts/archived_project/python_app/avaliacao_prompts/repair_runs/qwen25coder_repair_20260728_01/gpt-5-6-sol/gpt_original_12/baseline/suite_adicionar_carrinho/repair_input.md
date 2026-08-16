Condição experimental: baseline

ESPECIFICAÇÃO ORIGINAL:
Adding a product to the cart: The user searches for the product Blue Jeans in the Search store field. The user opens the product Blue Jeans in the search results. The user selects Add to cart on the product page. The system informs that the product has been added to the cart. The user accesses Shopping cart. The system displays Blue Jeans among the items in the cart.


ARQUIVO GERADO QUE DEVE SER REPARADO:
```typescript
import { test, expect } from '@playwright/test';

test('Adding Blue Jeans to the shopping cart', async ({ page }) => {
  await page.goto('https://demowebshop.tricentis.com/');

  const searchField = page.locator('#small-searchterms');
  await expect(searchField).toBeVisible();
  await searchField.fill('Blue Jeans');

  await page.locator('input.search-box-button').click();

  const blueJeansProduct = page
    .locator('.product-item')
    .filter({ has: page.getByRole('link', { name: 'Blue Jeans', exact: true }) });

  await expect(blueJeansProduct).toBeVisible();
  await blueJeansProduct
    .getByRole('link', { name: 'Blue Jeans', exact: true })
    .click();

  await expect(
    page.getByRole('heading', { name: 'Blue Jeans', exact: true }),
  ).toBeVisible();

  await page.locator('input[value="Add to cart"]').click();

  const successNotification = page.locator('#bar-notification');
  await expect(successNotification).toBeVisible();
  await expect(successNotification).toContainText(
    'The product has been added to your shopping cart',
  );

  await page.locator('#topcartlink').getByRole('link').click();

  await expect(
    page.locator('.cart-item-row').filter({
      has: page.getByRole('link', { name: 'Blue Jeans', exact: true }),
    }),
  ).toBeVisible();
});

```

EVIDÊNCIA DA FALHA DE EXECUÇÃO:
Falha registrada sem mensagem detalhada.

DIAGNÓSTICO DA REVISÃO:
Fluxo e oráculo completos; o botão genérico Add to cart é ambíguo na página do produto.

Faça uma única tentativa de reparo. Mantenha todas as verificações exigidas e devolva o arquivo TypeScript completo.