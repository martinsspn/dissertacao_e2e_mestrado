```typescript
import { test, expect } from '@playwright/test';

test.describe('Suite Busca Blue Jeans', () => {
  test('should search for Blue Jeans and open its details page', async ({ page }) => {
    // Etapa 1: Navegar para a página inicial e realizar a busca
    await page.goto('https://demowebshop.tricentis.com/');
    await page.locator("[id=\"small-searchterms\"]").fill('Blue Jeans');
    await page.getByRole("button", { name: "Search", exact: true }).click();

    // Etapa 3: Verificar que os resultados da busca contêm Blue Jeans
    const searchResults = page.locator('.product-list-item-name');
    await expect(searchResults).toContainText('Blue Jeans');

    // Etapa 4: Abrir a página de detalhes do produto Blue Jeans
    await searchResults.first().click();
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/blue-jeans');

    // Verificar que a página de detalhes exibe o nome Blue Jeans
    const productName = page.locator('.product-name');
    await expect(productName).toContainText('Blue Jeans');
  });
});
```