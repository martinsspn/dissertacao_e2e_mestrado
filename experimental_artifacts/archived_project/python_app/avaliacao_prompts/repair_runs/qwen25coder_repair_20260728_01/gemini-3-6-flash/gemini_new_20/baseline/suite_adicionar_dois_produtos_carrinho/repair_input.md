Condição experimental: baseline

ESPECIFICAÇÃO ORIGINAL:
Adding two different products to the cart: The user adds Computing and Internet to the cart. The user then adds Fiction to the cart. The user accesses Shopping cart. The system displays both Computing and Internet and Fiction as separate cart items, each with its quantity and price.


ARQUIVO GERADO QUE DEVE SER REPARADO:
```typescript
import { test, expect } from '@playwright/test';

test.describe('Shopping Cart - Add Multiple Products', () => {
  test('should display both Computing and Internet and Fiction in cart with quantity and price', async ({ page }) => {
    const baseUrl = process.env.BASE_URL || 'https://demowebshop.tricentis.com';

    // Navigate to the e-commerce store
    await page.goto(baseUrl);

    // 1. Navigate to Books category and add "Computing and Internet"
    await page.getByRole('link', { name: 'Books' }).first().click();
    await expect(page).toHaveURL(/.*\/books/);

    await page.getByRole('link', { name: 'Computing and Internet' }).first().click();
    await expect(page.getByRole('heading', { name: 'Computing and Internet' })).toBeVisible();

    // Click 'Add to cart' and wait for notification
    await page.getByRole('button', { name: 'Add to cart' }).click();
    const notification = page.locator('#bar-notification');
    await expect(notification).toBeVisible();
    await expect(notification).toContainText('The product has been added to your');

    // 2. Navigate back to Books category and add "Fiction"
    await page.getByRole('link', { name: 'Books' }).first().click();
    await page.getByRole('link', { name: 'Fiction', exact: true }).first().click();
    await expect(page.getByRole('heading', { name: 'Fiction' })).toBeVisible();

    // Click 'Add to cart' and wait for notification
    await page.getByRole('button', { name: 'Add to cart' }).click();
    await expect(notification).toBeVisible();
    await expect(notification).toContainText('The product has been added to your');

    // 3. Access Shopping cart
    await page.getByRole('link', { name: 'Shopping cart' }).first().click();
    await expect(page).toHaveURL(/.*\/cart/);
    await expect(page.getByRole('heading', { name: 'Shopping cart' })).toBeVisible();

    // 4. Verify Computing and Internet item in cart table
    const computingRow = page.locator('tr.cart-item-row').filter({ hasText: 'Computing and Internet' });
    await expect(computingRow).toBeVisible();
    await expect(computingRow.locator('input.qty-input')).toBeVisible();
    await expect(computingRow.locator('.product-unit-price')).toBeVisible();
    await expect(computingRow.locator('.product-subtotal')).toBeVisible();

    // 5. Verify Fiction item in cart table
    const fictionRow = page.locator('tr.cart-item-row').filter({ hasText: 'Fiction' });
    await expect(fictionRow).toBeVisible();
    await expect(fictionRow.locator('input.qty-input')).toBeVisible();
    await expect(fictionRow.locator('.product-unit-price')).toBeVisible();
    await expect(fictionRow.locator('.product-subtotal')).toBeVisible();
  });
});

```

EVIDÊNCIA DA FALHA DE EXECUÇÃO:
Error: locator.click: Error: strict mode violation: getByRole('button', { name: 'Add to cart' }) resolved to 6 elements:
    1) <input type="button" value="Add to cart" data-productid="13" id="add-to-cart-button-13" class="button-1 add-to-cart-button" onclick="AjaxCart.addproducttocart_details('/addproducttocart/details/13/1', '#product-details-form');return false;"/> aka locator('#add-to-cart-button-13')
    2) <input type="button" value="Add to cart" class="button-2 product-box-add-to-cart-button" onclick="AjaxCart.addproducttocart_catalog('/addproducttocart/catalog/75/1/1    ');return false;"/> aka getByRole('button', { name: 'Add to cart' }).nth(1)
    3) <input type="button" value="Add to cart" class="button-2 product-box-add-to-cart-button" onclick="AjaxCart.addproducttocart_catalog('/addproducttocart/catalog/74/1/1    ');return false;"/> aka getByRole('button', { name: 'Add to cart' }).nth(2)
    4) <input type="button" value="Add to cart" class="button-2 product-box-add-to-cart-button" onclick="AjaxCart.addproducttocart_catalog('/addproducttocart/catalog/36/1/1    ');return false;"/> aka getByRole('button', { name: 'Add to cart' }).nth(3)
    5) <input type="button" value="Add to cart" class="button-2 product-box-add-to-cart-button" onclick="AjaxCart.addproducttocart_catalog('/addproducttocart/catalog/22/1/1    ');return false;"/> aka getByRole('button', { name: 'Add to cart' }).nth(4)
    6) <input type="button" value="Add to cart" class="button-2 product-box-add-to-cart-button" onclick="AjaxCart.addproducttocart_catalog('/addproducttocart/catalog/45/1/1    ');return false;"/> aka getByRole('button', { name: 'Add to cart' }).nth(5)

Call log:
  - waiting for getByRole('button', { name: 'Add to cart' })

DIAGNÓSTICO DA REVISÃO:
Adiciona os dois livros no mesmo teste e valida linhas, quantidade e preços.

Faça uma única tentativa de reparo. Mantenha todas as verificações exigidas e devolva o arquivo TypeScript completo.