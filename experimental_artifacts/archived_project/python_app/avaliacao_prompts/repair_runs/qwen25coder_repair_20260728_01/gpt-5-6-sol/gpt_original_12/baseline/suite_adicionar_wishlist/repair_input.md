Condição experimental: baseline

ESPECIFICAÇÃO ORIGINAL:
Adding a product to the wishlist: The user is authenticated with valid credentials provided by the testing environment. The user searches for Camera in the Search store field. The user opens a Camera product presented in the results. The user selects Add to wishlist on the product page. The system informs that the product has been added to the wishlist. The user accesses Wishlist. The system displays the Camera product in the wishlist.


ARQUIVO GERADO QUE DEVE SER REPARADO:
```typescript
import { test, expect } from '@playwright/test';

test('adding a Camera product to the wishlist', async ({ page }) => {
  const email = process.env.DEMO_WEB_SHOP_EMAIL;
  const password = process.env.DEMO_WEB_SHOP_PASSWORD;

  if (!email || !password) {
    throw new Error(
      'Define DEMO_WEB_SHOP_EMAIL and DEMO_WEB_SHOP_PASSWORD in the testing environment.',
    );
  }

  await page.goto('https://demowebshop.tricentis.com/');

  await page.getByRole('link', { name: 'Log in' }).click();

  await page.locator('#Email').fill(email);
  await page.locator('#Password').fill(password);
  await page.getByRole('button', { name: 'Log in' }).click();

  await expect(page.getByRole('link', { name: email })).toBeVisible();

  const searchField = page.getByRole('textbox', { name: 'Search store' });
  await searchField.fill('Camera');
  await page.getByRole('button', { name: 'Search' }).click();

  const cameraProduct = page
    .locator('.product-item')
    .filter({
      has: page.locator('.product-title a', { hasText: 'Camera' }),
    })
    .first();

  await expect(cameraProduct).toBeVisible();

  const productName = (
    await cameraProduct.locator('.product-title a').innerText()
  ).trim();

  await cameraProduct.locator('.product-title a').click();

  await expect(page.getByRole('heading', { name: productName })).toBeVisible();

  await page.getByRole('button', { name: 'Add to wishlist' }).click();

  await expect(page.locator('#bar-notification')).toContainText(
    'The product has been added to your wishlist',
  );

  await page.getByRole('link', { name: /Wishlist/ }).click();

  await expect(
    page.locator('.wishlist-content .product-name', {
      hasText: productName,
    }),
  ).toBeVisible();
});

```

EVIDÊNCIA DA FALHA DE EXECUÇÃO:
Falha registrada sem mensagem detalhada.

DIAGNÓSTICO DA REVISÃO:
Representa autenticação, busca, inclusão e verificação; falha ao localizar a busca após login.

Faça uma única tentativa de reparo. Mantenha todas as verificações exigidas e devolva o arquivo TypeScript completo.