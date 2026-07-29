import { test, expect } from '@playwright/test';

test.describe('Suite Atualizar Quantidade Carrinho', () => {
  test('Atualizar quantidade do produto Computing and Internet no carrinho', async ({ page }) => {
    // Inicia na pagina principal
    await page.goto('https://demowebshop.tricentis.com/');

    // Etapa 1: Navegar ate o produto Computing and Internet e adicionar ao carrinho
    await page.goto('https://demowebshop.tricentis.com/computing-and-internet');
    await page.locator("[id=\"add-to-cart-button-13\"]").click();

    // Etapa 2: Acessar o carrinho de compras
    await page.getByRole("link", { name: "Shopping cart", exact: true }).click();
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/cart');

    // Alterar a quantidade do produto de 1 para 2
    const qtyInput = page.locator('input.qty-input').first();
    await qtyInput.fill('2');

    // Etapa 3: Selecionar Atualizar carrinho de compras
    await page.getByRole('button', { name: 'Update shopping cart' }).click();

    // Etapa 4: Validar a permanencia do produto, quantidade e consistencia do subtotal
    await expect(qtyInput).toHaveValue('2');
    await expect(page.locator('.shopping-cart-page')).toContainText('Computing and Internet');

    const unitPriceText = await page.locator('.product-unit-price').first().innerText();
    const subtotalText = await page.locator('.product-subtotal').first().innerText();

    const unitPrice = parseFloat(unitPriceText.replace(/[^0-9.]/g, ''));
    const subtotal = parseFloat(subtotalText.replace(/[^0-9.]/g, ''));

    expect(subtotal).toBeCloseTo(unitPrice * 2, 2);
  });
});
