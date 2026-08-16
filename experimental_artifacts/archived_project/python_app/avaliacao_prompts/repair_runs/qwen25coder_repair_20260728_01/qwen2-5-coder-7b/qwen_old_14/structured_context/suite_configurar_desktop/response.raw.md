```typescript
import { test, expect } from '@playwright/test';

test.describe('Suite Configurar Desktop', () => {
  test('should configure and add desktop to cart', async ({ page }) => {
    // Step 1: Access Computers and open the Desktops category
    await page.goto('https://demowebshop.tricentis.com/');
    await page.getByText("Computers", { exact: true }).first().click();
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/computers');

    // Step 2: Open a desktop that allows choosing its configuration
    await page.getByText("Desktops", { exact: true }).first().click();
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/desktops');
    
    // Step 3: Select options for Fast processor, 4 GB memory, 400 GB disk, and Office Suite software
    await page.getByText("Fast", { exact: true }).click();
    await page.getByText("4GB [+$25.00]", { exact: true }).click();
    await page.getByText("400GB [+$10.00]", { exact: true }).click();
    await page.getByText("Microsoft Office Suite [+$79.00]", { exact: true }).click();

    // Step 4: Select Add to cart
    await page.getByRole('button', { name: 'Add to cart', exact: true }).click();

    // Step 5: System informs that the product has been added to the cart
    await expect(page.locator('.content')).toContainText('The product has been added to your shopping cart');

    // Step 6: Access Shopping cart
    await page.getByRole("link", { name: "Shopping cart", exact: true }).click();
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/cart');

    // Step 7: System displays the configured desktop among the items in the cart
    await expect(page.locator('.cart-item-name')).toContainText('Desktop');
  });
});
```