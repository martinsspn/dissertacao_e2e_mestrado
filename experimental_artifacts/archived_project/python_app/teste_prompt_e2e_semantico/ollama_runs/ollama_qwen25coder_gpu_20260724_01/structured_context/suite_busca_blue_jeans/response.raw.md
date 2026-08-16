```typescript
import { test, expect } from '@playwright/test';

test.describe('Suite Busca Blue Jeans', () => {
  test('should search for Blue Jeans and open its details page', async ({ page }) => {
    await page.goto('https://demowebshop.tricentis.com/');

    // Etapa 1: Pesquisa por Blue Jeans
    const searchInput = page.locator('#small-searchterms');
    await searchInput.fill('Blue Jeans');
    const searchButton = page.locator('role=Search');
    await searchButton.click();

    // Verifica se a URL contém o termo de pesquisa
    await expect(page).toHaveURL(/blue-jeans/);

    // Etapa 3: Abre a página dos detalhes do Blue Jeans
    const blueJeansLink = page.locator('a', { hasText: 'Blue Jeans' });
    await blueJeansLink.click();

    // Verifica se a página de detalhes do Blue Jeans foi aberta corretamente
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/blue-jeans');
    await expect(page.locator('h1')).toHaveText('Blue Jeans');
  });
});
```