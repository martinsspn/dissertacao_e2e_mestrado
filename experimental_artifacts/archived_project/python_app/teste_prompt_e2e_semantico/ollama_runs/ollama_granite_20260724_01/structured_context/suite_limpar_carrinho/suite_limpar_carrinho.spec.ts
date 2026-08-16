import { test } from '@playwright/test';

describe('Suite Limpar Carrinho', () => {
  it('The user adds the product Blue Jeans to the cart to prepare the scenario.', async () => {
    await page.goto('https://demowebshop.tricentis.com/blue-jeans');

    const addToCartButton = await page.locator('#add-to-cart-button-36');
    await addToCartButton.click();

    const shoppingCartLink = await page.locator('.page-by-role/link[name="Shopping cart"]');
    await shoppingCartLink.click();
  });

  it('The user accesses Shopping cart.', async () => {
    await page.goto('https://demowebshop.tricentis.com/cart');

    const cartElement = await page.locator('.page-by-role/link[name="Shopping cart"]');
    expect(await cartElement).toBeInTheDocument();
  });

  it('The user marks Blue Jeans for removal.', async () => {
    const blueJeansButton = await page.locator('#blue-jeans-button');
    await blueJeansButton.click();

    const removeBlueJeansButton = await page.locator('.page-by-role/link[name="Remove from cart"]');
    await removeBlueJeansButton.click();
  });

  it('The user selects Update shopping cart.', async () => {
    await page.goto('https://demowebshop.tricentis.com/cart');

    const updateShoppingCartButton = await page.locator('.page-by-role/link[name="Update shopping cart"]');
    await updateShoppingCartButton.click();
  });

  it('The system displays the empty cart.', async () => {
    await page.goto('https://demowebshop.tricentis.com/cart');

    const cartElement = await page.locator('.page-by-role/link[name="Shopping cart"]');
    expect(await cartElement).toBeInTheDocument();
  });
});
