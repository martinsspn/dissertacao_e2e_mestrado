import { test, expect } from '@playwright/test';

test.describe('Suite Produtos Visualizados Recentemente', () => {
  test('deve exibir produtos visualizados recentemente na ordem correta', async ({ page }) => {
    // 1. Viewing the product history: Open Fiction product page, then Blue Jeans product page
    await page.goto('https://demowebshop.tricentis.com/');

    // Search and navigate to Fiction product page
    await page.locator('#small-searchterms').fill('Fiction');
    await page.getByRole('button', { name: 'Search' }).click();
    await page.getByRole('link', { name: 'Fiction' }).first().click();
    await expect(page.getByRole('heading', { name: 'Fiction' })).toBeVisible();

    // Search and navigate to Blue Jeans product page
    await page.locator('#small-searchterms').fill('Blue Jeans');
    await page.getByRole('button', { name: 'Search' }).click();
    await page.getByRole('link', { name: 'Blue Jeans' }).first().click();
    await expect(page.getByRole('heading', { name: 'Blue Jeans' })).toBeVisible();

    // 2. Select Recently viewed products in the Customer service section
    await page.getByText("Recently viewed products", { exact: true }).first().click();

    // 3. Verify Recently viewed products page and item order
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/recentlyviewedproducts');

    await expect(page.getByRole('link', { name: 'Blue Jeans' }).first()).toBeVisible();
    await expect(page.getByRole('link', { name: 'Fiction' }).first()).toBeVisible();

    const bodyText = await page.locator('body').innerText();
    const blueJeansIndex = bodyText.indexOf('Blue Jeans');
    const fictionIndex = bodyText.indexOf('Fiction');

    expect(blueJeansIndex).toBeGreaterThan(-1);
    expect(fictionIndex).toBeGreaterThan(-1);
    expect(blueJeansIndex).toBeLessThan(fictionIndex);
  });
});
