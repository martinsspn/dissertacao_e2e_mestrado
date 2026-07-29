import { test, expect, Page, Locator } from '@playwright/test';

const email = process.env.DEMO_WEB_SHOP_EMAIL;
const password = process.env.DEMO_WEB_SHOP_PASSWORD;

async function selectFirstAvailableOption(options: Locator): Promise<void> {
  const optionCount = await options.count();

  for (let index = 0; index < optionCount; index += 1) {
    const option = options.nth(index);

    if (await option.isEnabled()) {
      await option.check();
      return;
    }
  }

  throw new Error('Nenhuma opção disponível foi encontrada.');
}

async function continueCheckoutStep(
  page: Page,
  containerSelector: string,
): Promise<void> {
  const container = page.locator(containerSelector);
  await expect(container).toBeVisible();

  const continueButton = container.getByRole('button', {
    name: 'Continue',
    exact: true,
  });

  await expect(continueButton).toBeEnabled();
  await continueButton.click();
}

test.describe('Suite Checkout Blue Jeans', () => {
  test('finaliza a compra de Blue Jeans', async ({ page }) => {
    test.skip(
      !email || !password,
      'Defina DEMO_WEB_SHOP_EMAIL e DEMO_WEB_SHOP_PASSWORD com uma conta que possua endereços válidos.',
    );

    await page.goto('https://demowebshop.tricentis.com/');

    await page.getByRole('link', { name: 'Log in', exact: true }).click();
    await page.locator('#Email').fill(email!);
    await page.locator('#Password').fill(password!);
    await page.getByRole('button', { name: 'Log in', exact: true }).click();

    await expect(
      page.getByRole('link', { name: email!, exact: true }),
    ).toBeVisible();

    await page.locator('#small-searchterms').fill('Blue Jeans');
    await page.getByRole('button', { name: 'Search', exact: true }).click();

    const blueJeansResult = page
      .locator('.product-item')
      .filter({
        has: page.getByRole('link', {
          name: 'Blue Jeans',
          exact: true,
        }),
      });

    await expect(blueJeansResult).toBeVisible();

    const blueJeansResultLink = blueJeansResult.getByRole('link', {
      name: 'Blue Jeans',
      exact: true,
    });

    await expect(blueJeansResultLink).toBeVisible();
    await blueJeansResultLink.click();

    await expect(page).toHaveURL(
      'https://demowebshop.tricentis.com/blue-jeans',
    );
    await expect(
      page.getByRole('heading', { name: 'Blue Jeans', exact: true }),
    ).toBeVisible();

    await page.locator('#add-to-cart-button-36').click();

    const notification = page.locator('#bar-notification');
    await expect(notification).toBeVisible();
    await expect(notification).toContainText(
      'The product has been added to your shopping cart',
    );

    await page
      .getByRole('link', { name: 'Shopping cart', exact: true })
      .click();

    await expect(page).toHaveURL('https://demowebshop.tricentis.com/cart');
    await expect(
      page.getByRole('heading', { name: 'Shopping cart', exact: true }),
    ).toBeVisible();

    const blueJeansCartItem = page
      .locator('tr.cart-item-row')
      .filter({
        has: page.getByRole('link', {
          name: 'Blue Jeans',
          exact: true,
        }),
      });

    await expect(blueJeansCartItem).toBeVisible();
    await expect(
      blueJeansCartItem.getByRole('link', {
        name: 'Blue Jeans',
        exact: true,
      }),
    ).toBeVisible();

    await page.locator('#termsofservice').check();
    await expect(page.locator('#termsofservice')).toBeChecked();
    await page.locator('#checkout').click();

    const billingAddressSelect = page.locator('#billing-address-select');

    if (await billingAddressSelect.isVisible()) {
      const selectedBillingAddress =
        await billingAddressSelect.locator('option:checked').textContent();

      expect(selectedBillingAddress?.trim()).toBeTruthy();
    }

    await continueCheckoutStep(page, '#billing-buttons-container');

    const shippingAddressSelect = page.locator('#shipping-address-select');

    if (await shippingAddressSelect.isVisible()) {
      const selectedShippingAddress =
        await shippingAddressSelect.locator('option:checked').textContent();

      expect(selectedShippingAddress?.trim()).toBeTruthy();
    }

    await continueCheckoutStep(page, '#shipping-buttons-container');

    const shippingMethods = page.locator(
      '#checkout-shipping-method-load input[type="radio"]',
    );

    await expect(shippingMethods.first()).toBeVisible();
    await selectFirstAvailableOption(shippingMethods);
    await expect(shippingMethods.filter({ has: page.locator(':checked') })).toHaveCount(1);
    await continueCheckoutStep(page, '#shipping-method-buttons-container');

    const paymentMethods = page.locator(
      '#checkout-payment-method-load input[type="radio"]',
    );

    await expect(paymentMethods.first()).toBeVisible();
    await selectFirstAvailableOption(paymentMethods);
    await expect(paymentMethods.filter({ has: page.locator(':checked') })).toHaveCount(1);
    await continueCheckoutStep(page, '#payment-method-buttons-container');

    const paymentInformation = page.locator(
      '#checkout-payment-info-load',
    );

    await expect(paymentInformation).toBeVisible();
    await continueCheckoutStep(page, '#payment-info-buttons-container');

    const orderReview = page.locator('#checkout-confirm-order-load');
    await expect(orderReview).toBeVisible();
    await expect(
      orderReview.getByRole('link', {
        name: 'Blue Jeans',
        exact: true,
      }),
    ).toBeVisible();

    const confirmButton = page
      .locator('#confirm-order-buttons-container')
      .getByRole('button', { name: 'Confirm', exact: true });

    await expect(confirmButton).toBeEnabled();
    await confirmButton.click();

    await expect(
      page.getByRole('heading', {
        name: 'Thank you',
        exact: true,
      }),
    ).toBeVisible();

    await expect(
      page.getByText(
        'Your order has been successfully processed!',
        { exact: true },
      ),
    ).toBeVisible();
  });
});
