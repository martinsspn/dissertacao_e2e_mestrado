```typescript
import { test, expect } from '@playwright/test';

test.describe('Suite Navegar Categoria Livros', () => {
  test('The user accesses the Demo Web Shop home page and navigates to the Books category', async ({ page }) => {
    // Etapa 1: Acessa a página inicial do Demo Web Shop
    await page.goto('https://demowebshop.tricentis.com/');
    expect(page).toHaveTitle('Demo Web Shop');

    // Etapa 2: Seleciona a categoria "Books" no menu principal
    const booksLink = page.getByText("Books", { exact: true }).first();
    await booksLink.click();

    // Verifica se foi redirecionado para a página de categorias de livros
    expect(page).toHaveURL('https://demowebshop.tricentis.com/books');
    expect(page.locator('h1')).toHaveText('Books');

    // Etapa 3: Confirma que os subcategorias estão disponíveis
    const subcategories = ['Computing and Internet', 'Fiction', 'Health Book'];
    for (const category of subcategories) {
      expect(page.getByText(category)).toBeVisible();
    }
  });
});
```