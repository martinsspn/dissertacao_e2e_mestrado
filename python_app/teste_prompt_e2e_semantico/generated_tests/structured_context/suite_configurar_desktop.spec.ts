import { test, expect } from '@playwright/test';

test.describe('Suite Configurar Desktop', () => {
  test('should configure and add desktop to cart', async ({ page }) => {
    await page.goto('https://demowebshop.tricentis.com/');

    // Etapa 1
    await page.click('text=Computers');
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/computers');
    await page.click('text=Desktops');
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/desktops');

    // Etapa 2
    const desktopLink = page.locator('a', { hasText: 'Build your own computer' });
    await desktopLink.click();
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/build-your-own-computer');

    // Etapa 3
    await page.selectOption('#product_attribute_1', 'Fast');
    await page.fill('#product_attribute_2', '4');
    await page.selectOption('#product_attribute_3', '400 GB');
    await page.click('text=Office Suite');
    await expect(page.locator('#product_attribute_5')).toBeChecked();

    // Etapa 4
    await page.click('text=Add to cart');

    // Etapa 5
    const alert = page.locator('.content-wrapper > .message-success');
    await expect(alert).toContainText('The product has been added to your shopping cart');

    // Etapa 6
    await page.click(page.getByRole('link', { name: 'Shopping cart', exact: true }));
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/cart');

    // Etapa 7
    const configuredDesktop = page.locator('.cart-item');
    await expect(configuredDesktop).toContainText('Build your own computer');
  });
});
