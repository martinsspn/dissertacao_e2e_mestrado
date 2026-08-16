Condição experimental: baseline

ESPECIFICAÇÃO ORIGINAL:
Updating a product quantity in the cart: The user adds Computing and Internet to the cart to prepare the scenario. The user accesses Shopping cart and changes the quantity of Computing and Internet from one to two. The user selects Update shopping cart. The system keeps the product in the cart with quantity two and updates its subtotal consistently with the displayed unit price.


ARQUIVO GERADO QUE DEVE SER REPARADO:
```typescript
import { test, expect } from '@playwright/test';

test.describe('Shopping Cart Quantity Update', () => {
  test('should update product quantity in cart and reflect correct subtotal', async ({ page }) => {
    const baseUrl = process.env.BASE_URL || 'https://demo.nopcommerce.com';

    // Navigate to the store
    await page.goto(baseUrl);

    // Search for "Computing and Internet"
    const searchInput = page.getByPlaceholder('Search store');
    await searchInput.fill('Computing and Internet');
    await page.getByRole('button', { name: 'Search' }).click();

    // Open the product page
    await page.getByRole('link', { name: 'Computing and Internet', exact: false }).first().click();

    // Add product to cart to prepare scenario
    const addToCartButton = page.getByRole('button', { name: 'Add to cart' }).first();
    await addToCartButton.click();

    // Wait for the notification bar confirming addition
    const notification = page.locator('.bar-notification.success');
    await expect(notification).toBeVisible();

    // Access Shopping cart
    await page.getByRole('link', { name: 'Shopping cart', exact: false }).first().click();
    await expect(page).toHaveURL(/.*cart/);

    // Locate the row for "Computing and Internet"
    const cartRow = page.locator('tr').filter({ hasText: 'Computing and Internet' });
    await expect(cartRow).toBeVisible();

    // Change the quantity from one to two
    const qtyInput = cartRow.locator('input.qty-input, input[name^="itemquantity"]').first();
    await qtyInput.fill('2');

    // Select "Update shopping cart"
    const updateCartBtn = page.getByRole('button', { name: 'Update shopping cart' })
      .or(page.getByRole('button', { name: 'Update cart' }));
    await updateCartBtn.first().click();

    // Verify product quantity remains two
    await expect(qtyInput).toHaveValue('2');

    // Read unit price and subtotal elements to assert mathematical consistency
    const unitPriceElement = cartRow.locator('.product-unit-price, .unit-price').first();
    const subtotalElement = cartRow.locator('.product-subtotal, .subtotal').first();

    await expect(unitPriceElement).toBeVisible();
    await expect(subtotalElement).toBeVisible();

    const unitPriceText = await unitPriceElement.innerText();
    const subtotalText = await subtotalElement.innerText();

    const parsePrice = (priceStr: string) => {
      const match = priceStr.replace(/[^0-9.]/g, '');
      return parseFloat(match);
    };

    const unitPrice = parsePrice(unitPriceText);
    const subtotal = parsePrice(subtotalText);

    expect(unitPrice).toBeGreaterThan(0);
    expect(subtotal).toBeCloseTo(unitPrice * 2, 2);
  });
});

```

EVIDÊNCIA DA FALHA DE EXECUÇÃO:
TimeoutError: locator.fill: Timeout 10000ms exceeded.
Call log:
  - waiting for getByPlaceholder('Search store')

DIAGNÓSTICO DA REVISÃO:
Fluxo e cálculo completos; o domínio padrão é outra instalação nopCommerce.

Faça uma única tentativa de reparo. Mantenha todas as verificações exigidas e devolva o arquivo TypeScript completo.