import { test, expect } from '@playwright/test';

test.describe('Suite Navegar Categoria Livros', () => {
  test('Navegar para a categoria Livros e validar breadcrumb e produtos', async ({ page }) => {
    // Etapa 1: Acessar a página inicial
    await page.goto('https://demowebshop.tricentis.com/');
    await expect(page).toHaveTitle('Demo Web Shop');

    // Etapa 2: Selecionar Books no menu principal de categorias
    await page.getByText("Books", { exact: true }).first().click();

    // Etapa 3: Verificar exibição da página Books, breadcrumb e produtos
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/books');
    await expect(page.getByRole('heading', { name: 'Books', exact: true })).toBeVisible();

    // Validação do breadcrumb
    await expect(page.locator('.breadcrumb')).toContainText('Books');

    // Validação dos produtos disponíveis
    await expect(page.getByRole('link', { name: 'Computing and Internet', exact: true })).toBeVisible();
    await expect(page.getByRole('link', { name: 'Fiction', exact: true })).toBeVisible();
    await expect(page.getByRole('link', { name: 'Health Book', exact: true })).toBeVisible();
  });
});
