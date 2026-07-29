import { test, expect } from '@playwright/test';

test.describe('Suite Exibir Quatro Livros', () => {
  test('Deve exibir ate quatro livros na pagina da categoria Books', async ({ page }) => {
    // Etapa 1: Aceessar a categoria Books
    await page.goto('https://demowebshop.tricentis.com/');
    await page.getByText("Books", { exact: true }).first().click();
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/books');
    await expect(page.getByRole('heading', { name: 'Books' })).toBeVisible();

    // Etapa 2: Selecionar 4 no controle de exibição (Display)
    await page.locator('#products-pagesize').selectOption({ label: '4' });

    // Etapa 3: Confirmar categoria visivel e no maximo 4 produtos na pagina
    await expect(page.getByRole('heading', { name: 'Books' })).toBeVisible();

    const productItems = page.locator('.product-item');
    await expect(productItems.first()).toBeVisible();
    const count = await productItems.count();
    expect(count).toBeGreaterThan(0);
    expect(count).toBeLessThanOrEqual(4);
  });
});
