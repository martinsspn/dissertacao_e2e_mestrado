import { test, expect } from '@playwright/test';

test.describe('Suite Produtos Visualizados Recentemente', () => {
  test('Viewing the product history and verifying recently viewed products', async ({ page }) => {
    // Etapa 1: Viewing the product history
    await page.goto('https://demowebshop.tricentis.com/blue-jeans');
    expect(page).toHaveURL('https://demowebshop.tricentis.com/blue-jeans');

    // Etapa 2: The user selects Recently viewed products in the Customer service section
    await page.getByText("Recently viewed products", { exact: true }).first().click();
    expect(page).toHaveURL('https://demowebshop.tricentis.com/recentlyviewedproducts');

    // Verifying that Blue Jeans is presented before Fiction because it was viewed most recently
    const productItems = await page.locator('.product-item').allInnerTexts();
    expect(productItems[0]).toContain('Blue Jeans');
    expect(productItems[1]).toContain('Fiction');
  });
});
