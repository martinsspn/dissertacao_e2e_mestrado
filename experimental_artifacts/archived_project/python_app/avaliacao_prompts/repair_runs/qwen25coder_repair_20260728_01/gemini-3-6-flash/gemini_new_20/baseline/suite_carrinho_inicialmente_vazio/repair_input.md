Condição experimental: baseline

ESPECIFICAÇÃO ORIGINAL:
Viewing an empty shopping cart: In a new browser context, the user accesses Shopping cart without adding any product. The system displays the Shopping cart page, shows a zero item count, and informs that the shopping cart is empty.


ARQUIVO GERADO QUE DEVE SER REPARADO:
```typescript
import { test, expect } from '@playwright/test';

test.describe('Shopping Cart - Empty State', () => {
  test('displays empty cart message and zero item count when accessed without adding products', async ({ page }) => {
    const baseUrl = process.env.BASE_URL || 'https://demo.ecomstore.com';

    // Access the shopping cart directly in a fresh context
    await page.goto(`${baseUrl}/cart`);

    // Verify Shopping Cart page is displayed
    const cartHeading = page.getByRole('heading', { name: /shopping cart|your cart/i });
    await expect(cartHeading).toBeVisible();

    // Verify notice informing that the shopping cart is empty
    const emptyCartNotice = page.getByText(/shopping cart is empty|your cart is empty|you have no items/i);
    await expect(emptyCartNotice).toBeVisible();

    // Verify item count indicates 0 items
    const itemCount = page.getByText(/0 items|0 products|items \(0\)/i);
    await expect(itemCount.first()).toBeVisible();
  });
});

```

EVIDÊNCIA DA FALHA DE EXECUÇÃO:
Error: expect(locator).toBeVisible() failed

Locator: getByRole('heading', { name: /shopping cart|your cart/i })
Expected: visible
Timeout: 7000ms
Error: element(s) not found

Call log:
  - Expect "toBeVisible" with timeout 7000ms
  - waiting for getByRole('heading', { name: /shopping cart|your cart/i })

DIAGNÓSTICO DA REVISÃO:
Oráculo completo, porém executa por padrão contra um domínio de comércio inventado.

Faça uma única tentativa de reparo. Mantenha todas as verificações exigidas e devolva o arquivo TypeScript completo.