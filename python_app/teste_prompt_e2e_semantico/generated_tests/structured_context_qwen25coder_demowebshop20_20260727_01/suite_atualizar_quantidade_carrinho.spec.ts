import { test, expect } from '@playwright/test';

test.describe('Suite Atualizar Quantidade Carrinho', () => {
  test('should update quantity in cart and keep product with updated subtotal', async ({ page }) => {
    // Etapa 1: Adicionar produto ao carrinho
    await page.goto('https://demowebshop.tricentis.com/computing-and-internet');
    await page.locator("[id=\"add-to-cart-button-13\"]").click();
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/cart');

    // Etapa 2: Acessar carrinho e alterar quantidade
    await page.getByRole("link", { name: "Shopping cart", exact: true }).click();
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/cart');
    await page.locator("[name=\"cart_quantity_13\"]").fill('2');
    await page.locator("[id=\"update_cart_button\"]").click();

    // Verificar se a quantidade foi atualizada e o subtotal está correto
    await expect(page.locator("[name=\"cart_quantity_13\"]")).toHaveValue('2');
    const unitPrice = await page.locator("[class=\"product-unit-price\"]").textContent();
    const expectedSubtotal = parseFloat(unitPrice) * 2;
    const displayedSubtotal = await page.locator("[class=\"order-total-value\"]").textContent();
    expect(parseFloat(displayedSubtotal)).toBe(expectedSubtotal);
  });
});
