import { test, expect } from '@playwright/test';

test.describe('Suite Busca Sem Resultados', () => {
  test('should display no products matched message when searching for a non-existent term', async ({ page }) => {
    await page.goto('https://demowebshop.tricentis.com/');

    // Etapa 1
    const searchInputLocator = page.locator("[id=\"small-searchterms\"]");
    await searchInputLocator.fill('NonExistentTerm');
    
    const searchButtonLocator = page.getByRole("button", { name: "Search", exact: true });
    await searchButtonLocator.click();

    // Verificação de que a página de busca foi carregada
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/search?q=NonExistentTerm');

    // Verificação de que não há produtos correspondentes
    const noResultsMessage = page.getByText('No products were found that matched your criteria!');
    await expect(noResultsMessage).toBeVisible();
  });
});
