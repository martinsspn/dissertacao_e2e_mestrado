import { test, expect } from '@playwright/test';

test.describe('Suite Filtrar Livros Abaixo 25', () => {
  test('Filtrar livros com preco abaixo de 25.00', async ({ page }) => {
    // 1. The user accesses the Books category.
    await page.goto('https://demowebshop.tricentis.com/');
    await page.getByText("Books", { exact: true }).first().click();

    await expect(page).toHaveURL('https://demowebshop.tricentis.com/books');
    await expect(page.getByRole('heading', { name: 'Books', exact: true })).toBeVisible();

    // 2. The user selects the Under 25.00 price filter.
    await page.getByText("Under 25.00", { exact: true }).first().click();

    // 3. The system keeps the Books category visible and displays only products whose current sale price is below 25.00.
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/books?price=-25');
    await expect(page.getByRole('heading', { name: 'Books', exact: true })).toBeVisible();

    const priceElements = page.locator('.actual-price');
    await expect(priceElements.first()).toBeVisible();

    const count = await priceElements.count();
    expect(count).toBeGreaterThan(0);

    for (let i = 0; i < count; i++) {
      const priceText = await priceElements.nth(i).innerText();
      const priceValue = parseFloat(priceText.replace(/[^0-9.]/g, ''));
      expect(priceValue).toBeLessThan(25.00);
    }
  });
});
