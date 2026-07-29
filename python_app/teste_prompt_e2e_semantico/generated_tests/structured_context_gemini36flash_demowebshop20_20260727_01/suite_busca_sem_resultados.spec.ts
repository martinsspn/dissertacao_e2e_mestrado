import { test, expect } from '@playwright/test';

test.describe('Suite Busca Sem Resultados', () => {
  test('Deve exibir mensagem informando que nenhum produto foi encontrado ao buscar termo inexistente', async ({ page }) => {
    await page.goto('https://demowebshop.tricentis.com/');

    const nonExistentTerm = 'XYZ987654321NoProduct';

    await page.locator("[id=\"small-searchterms\"]").fill(nonExistentTerm);
    await page.getByRole("button", { name: "Search", exact: true }).click();

    await expect(page.getByText('No products were found that matched your criteria.')).toBeVisible();
  });
});
