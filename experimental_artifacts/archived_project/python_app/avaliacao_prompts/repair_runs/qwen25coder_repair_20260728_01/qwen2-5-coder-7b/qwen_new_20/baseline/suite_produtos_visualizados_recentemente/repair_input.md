Condição experimental: baseline

ESPECIFICAÇÃO ORIGINAL:
Viewing the product history: In a new browser context, the user opens the Fiction product page and then opens the Blue Jeans product page. The user selects Recently viewed products in the Customer service section. The system displays the Recently viewed products page containing both Blue Jeans and Fiction, with Blue Jeans presented before Fiction because it was viewed most recently.


ARQUIVO GERADO QUE DEVE SER REPARADO:
```typescript
import { test, expect } from '@playwright/test';

test.describe('Product History', () => {
  test('displays recently viewed products in the correct order', async ({ page }) => {
    // Open a new browser context
    const context = await page.context();
    const newPage = await context.newPage();

    // Navigate to Fiction product page
    await newPage.goto('https://example.com/fiction-product');

    // Navigate to Blue Jeans product page
    await newPage.goto('https://example.com/blue-jeans-product');

    // Select Recently viewed products in the Customer service section
    await newPage.click('text=Customer Service');
    await newPage.click('text=Recently Viewed Products');

    // Check if both products are displayed
    const recentlyViewedProducts = await newPage.textContent('.recently-viewed-products');
    expect(recentlyViewedProducts).toContain('Blue Jeans');
    expect(recentlyViewedProducts).toContain('Fiction');

    // Verify the order of products
    const productOrder = await newPage.textContent('.product-order');
    expect(productOrder).toBe('Blue Jeans, Fiction');
  });
});

```

EVIDÊNCIA DA FALHA DE EXECUÇÃO:
TimeoutError: page.click: Timeout 10000ms exceeded.
Call log:
  - waiting for locator('text=Customer Service')

DIAGNÓSTICO DA REVISÃO:
Representa a ordem pedida, mas usa outra aplicação e seletores inventados.

Faça uma única tentativa de reparo. Mantenha todas as verificações exigidas e devolva o arquivo TypeScript completo.