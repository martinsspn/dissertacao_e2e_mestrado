```typescript
import { test, expect } from '@playwright/test';

test.describe('Suite Comparar Produtos', () => {
  test('should compare products and clear the list', async ({ page }) => {
    // Etapa 1: Acessa a página de produtos Computing and Internet e adiciona ao comparador
    await page.goto('https://demowebshop.tricentis.com/computing-and-internet');
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/computing-and-internet');
    await page.getByRole('button', { name: 'Add to compare list' }).click();

    // Etapa 2: Acessa a página de produtos Fiction e adiciona ao comparador
    await page.goto('https://demowebshop.tricentis.com/fiction');
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/fiction');
    await page.getByRole('link', { name: 'Fiction' }).click();

    // Etapa 3: Verifica se os produtos estão sendo comparados
    await expect(page.locator('.compare-products-page')).toBeVisible();
    await expect(page.locator('.product-name', { hasText: 'Computing and Internet' })).toBeVisible();
    await expect(page.locator('.product-name', { hasText: 'Fiction' })).toBeVisible();

    // Etapa 4: Limpa a lista de comparação
    await page.getByRole('button', { name: 'Clear list' }).click();
    await expect(page.locator('.compare-products-page')).not.toBeVisible();
  });
});
```