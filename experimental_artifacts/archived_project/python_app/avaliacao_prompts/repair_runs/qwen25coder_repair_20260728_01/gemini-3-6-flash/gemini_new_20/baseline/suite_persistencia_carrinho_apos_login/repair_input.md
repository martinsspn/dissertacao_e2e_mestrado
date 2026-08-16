Condição experimental: baseline

ESPECIFICAÇÃO ORIGINAL:
Persistence of an authenticated user's cart: The user is authenticated with valid credentials provided by the testing environment. The user ensures that the cart does not contain Computing and Internet and then adds that product to the cart. The user logs out and logs in again with the same account. The user accesses Shopping cart. The system still displays Computing and Internet in the cart. At the end, the user removes the product to restore the account state.


ARQUIVO GERADO QUE DEVE SER REPARADO:
```typescript
import { test, expect } from '@playwright/test';

test.describe('Authenticated User Cart Persistence', () => {
  test('should persist Computing and Internet in cart across user sessions and clean up state', async ({ page }) => {
    const email = process.env.E2E_EMAIL;
    const password = process.env.E2E_PASSWORD;
    const baseUrl = process.env.BASE_URL || 'https://demowebshop.tricentis.com';

    expect(email, 'E2E_EMAIL environment variable must be set').toBeTruthy();
    expect(password, 'E2E_PASSWORD environment variable must be set').toBeTruthy();

    const productName = 'Computing and Internet';

    // Helper function to log in
    async function login() {
      await page.goto(baseUrl);
      const logoutLink = page.getByRole('link', { name: 'Log out' });
      if (await logoutLink.isVisible()) {
        return;
      }
      await page.getByRole('link', { name: 'Log in' }).click();
      await page.getByLabel(/Email/i).fill(email!);
      await page.getByLabel(/Password/i).fill(password!);
      await page.getByRole('button', { name: 'Log in' }).click();
      await expect(logoutLink).toBeVisible();
    }

    // Helper function to log out
    async function logout() {
      const logoutLink = page.getByRole('link', { name: 'Log out' });
      if (await logoutLink.isVisible()) {
        await logoutLink.click();
        await expect(page.getByRole('link', { name: 'Log in' })).toBeVisible();
      }
    }

    // Helper function to ensure product is removed from cart
    async function removeProductFromCart() {
      await page.getByRole('link', { name: /Shopping cart/i }).first().click();
      const productInCart = page.getByRole('link', { name: productName, exact: true });
      
      if (await productInCart.isVisible()) {
        const cartRow = page.locator('tr', { has: productInCart });
        const removeCheckbox = cartRow.getByRole('checkbox', { name: /remove/i }).or(cartRow.locator('input[name="removefromcart"]'));
        await removeCheckbox.check();
        await page.getByRole('button', { name: 'Update shopping cart' }).click();
        await expect(productInCart).not.toBeVisible();
      }
    }

    // Step 1: Authenticate
    await login();

    // Step 2: Ensure cart does not contain Computing and Internet
    await removeProductFromCart();

    try {
      // Step 3: Add Computing and Internet to the cart
      const searchInput = page.getByRole('textbox', { name: /Search store/i }).or(page.getByPlaceholder('Search store'));
      await searchInput.fill(productName);
      await page.getByRole('button', { name: 'Search' }).click();

      await page.getByRole('link', { name: productName, exact: true }).first().click();
      await page.getByRole('button', { name: 'Add to cart' }).first().click();

      // Confirm item added notification
      const notification = page.getByText(/The product has been added to your/i);
      await expect(notification).toBeVisible();

      // Step 4: Log out
      await logout();

      // Step 5: Log in again with the same account
      await login();

      // Step 6: Access Shopping cart
      await page.getByRole('link', { name: /Shopping cart/i }).first().click();

      // Step 7: Verify Computing and Internet is still in the cart
      const persistedItem = page.getByRole('link', { name: productName, exact: true });
      await expect(persistedItem).toBeVisible();
    } finally {
      // Step 8: Clean up / restore account state
      await removeProductFromCart();
    }
  });
});

```

EVIDÊNCIA DA FALHA DE EXECUÇÃO:
Error: E2E_EMAIL environment variable must be set

expect(received).toBeTruthy()

Received: undefined

DIAGNÓSTICO DA REVISÃO:
Usa credenciais do ambiente, limpa o estado, reloga, verifica persistência e restaura a conta em finally.

Faça uma única tentativa de reparo. Mantenha todas as verificações exigidas e devolva o arquivo TypeScript completo.