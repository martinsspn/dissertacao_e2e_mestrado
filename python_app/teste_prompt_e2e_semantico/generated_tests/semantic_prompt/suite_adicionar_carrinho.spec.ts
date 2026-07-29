import { test, expect } from '@playwright/test';

test.describe('Suite Adicionar Carrinho', () => {
test('adiciona Blue Jeans ao carrinho', async ({ page }) => {
await page.goto('https://demowebshop.tricentis.com/');

const searchField = page.locator('#small-searchterms');
await expect(searchField).toBeVisible();
await searchField.fill('Blue Jeans');
await page.getByRole('button', { name: 'Search' }).click();

const productLink = page.getByRole('link', { name: 'Blue Jeans', exact: true });
await expect(productLink).toBeVisible();
await productLink.click();

await expect(page).toHaveURL(/\/blue-jeans$/);
await expect(page.getByRole('heading', { name: 'Blue Jeans', exact: true })).toBeVisible();

await page.locator('#add-to-cart-button-36').click();

const notification = page.locator('#bar-notification');
await expect(notification).toBeVisible();
await expect(notification).toContainText('The product has been added to your shopping cart');

await page.getByRole('link', { name: 'Shopping cart', exact: true }).click();

await expect(page).toHaveURL(/\/cart$/);
await expect(page.getByRole('heading', { name: 'Shopping cart', exact: true })).toBeVisible();
await expect(page.getByRole('link', { name: 'Blue Jeans', exact: true })).toBeVisible();

});
});
