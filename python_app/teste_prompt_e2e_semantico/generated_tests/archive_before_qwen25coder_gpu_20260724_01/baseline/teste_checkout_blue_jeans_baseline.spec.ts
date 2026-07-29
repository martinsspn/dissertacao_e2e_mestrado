import { test, expect, Page } from '@playwright/test';

function requireEnvironmentVariable(name: string): string {
  const value = process.env[name];

  if (!value) {
    throw new Error(`The environment variable ${name} is required.`);
  }

  return value;
}

async function completeAddressForm(
  page: Page,
  prefix: 'BillingNewAddress' | 'ShippingNewAddress',
): Promise<void> {
  const firstNameField = page.locator(`#${prefix}_FirstName`);

  if (!(await firstNameField.isVisible())) {
    return;
  }

  await firstNameField.fill(
    requireEnvironmentVariable('DEMO_WEB_SHOP_FIRST_NAME'),
  );
  await page
    .locator(`#${prefix}_LastName`)
    .fill(requireEnvironmentVariable('DEMO_WEB_SHOP_LAST_NAME'));
  await page
    .locator(`#${prefix}_Email`)
    .fill(requireEnvironmentVariable('DEMO_WEB_SHOP_EMAIL'));

  const countrySelect = page.locator(`#${prefix}_CountryId`);
  await countrySelect.selectOption({
    label: requireEnvironmentVariable('DEMO_WEB_SHOP_COUNTRY'),
  });

  const stateSelect = page.locator(`#${prefix}_StateProvinceId`);

  if (await stateSelect.isVisible()) {
    const state = process.env.DEMO_WEB_SHOP_STATE;

    if (state) {
      await stateSelect.selectOption({ label: state });
    } else {
      const availableState = stateSelect.locator(
        'option:not([value="0"]):not([value=""])',
      );

      if ((await availableState.count()) > 0) {
        await stateSelect.selectOption(
          await availableState.first().getAttribute('value'),
        );
      }
    }
  }

  await page
    .locator(`#${prefix}_City`)
    .fill(requireEnvironmentVariable('DEMO_WEB_SHOP_CITY'));
  await page
    .locator(`#${prefix}_Address1`)
    .fill(requireEnvironmentVariable('DEMO_WEB_SHOP_ADDRESS'));
  await page
    .locator(`#${prefix}_ZipPostalCode`)
    .fill(requireEnvironmentVariable('DEMO_WEB_SHOP_ZIP_CODE'));
  await page
    .locator(`#${prefix}_PhoneNumber`)
    .fill(requireEnvironmentVariable('DEMO_WEB_SHOP_PHONE'));
}

test('Complete purchase of the product Blue Jeans', async ({ page }) => {
  const email = requireEnvironmentVariable('DEMO_WEB_SHOP_EMAIL');
  const password = requireEnvironmentVariable('DEMO_WEB_SHOP_PASSWORD');

  await page.goto('https://demowebshop.tricentis.com/');

  await page.getByRole('link', { name: 'Log in', exact: true }).click();

  await page.locator('#Email').fill(email);
  await page.locator('#Password').fill(password);
  await page.locator('input.login-button').click();

  await expect(
    page.getByRole('link', { name: email, exact: true }),
  ).toBeVisible();

  const searchField = page.locator('#small-searchterms');
  await searchField.fill('Blue Jeans');
  await page.locator('input.search-box-button').click();

  const blueJeansProduct = page.locator('.product-item').filter({
    has: page.getByRole('link', {
      name: 'Blue Jeans',
      exact: true,
    }),
  });

  await expect(blueJeansProduct).toBeVisible();

  await blueJeansProduct
    .getByRole('link', {
      name: 'Blue Jeans',
      exact: true,
    })
    .click();

  await expect(
    page.getByRole('heading', {
      name: 'Blue Jeans',
      exact: true,
    }),
  ).toBeVisible();

  await page.locator('input[value="Add to cart"]').click();

  const successNotification = page.locator('#bar-notification');
  await expect(successNotification).toBeVisible();
  await expect(successNotification).toContainText(
    'The product has been added to your shopping cart',
  );

  await page.locator('#topcartlink').getByRole('link').click();

  const blueJeansCartItem = page.locator('.cart-item-row').filter({
    has: page.getByRole('link', {
      name: 'Blue Jeans',
      exact: true,
    }),
  });

  await expect(blueJeansCartItem).toBeVisible();

  await page.locator('#termsofservice').check();
  await page.locator('#checkout').click();

  const billingAddressSelect = page.locator('#billing-address-select');

  if (await billingAddressSelect.isVisible()) {
    const existingBillingAddress = billingAddressSelect.locator(
      'option:not([value=""])',
    );

    if ((await existingBillingAddress.count()) > 0) {
      await billingAddressSelect.selectOption({
        index: 0,
      });
    }
  }

  await completeAddressForm(page, 'BillingNewAddress');
  await page.locator('#billing-buttons-container input').click();

  const shippingAddressSelect = page.locator('#shipping-address-select');

  if (await shippingAddressSelect.isVisible()) {
    const existingShippingAddress = shippingAddressSelect.locator(
      'option:not([value=""])',
    );

    if ((await existingShippingAddress.count()) > 0) {
      await shippingAddressSelect.selectOption({
        index: 0,
      });
    }
  }

  await completeAddressForm(page, 'ShippingNewAddress');
  await page.locator('#shipping-buttons-container input').click();

  const shippingMethods = page.locator(
    '#checkout-shipping-method-load input[type="radio"]',
  );

  await expect(shippingMethods.first()).toBeVisible();
  await shippingMethods.first().check();
  await page.locator('#shipping-method-buttons-container input').click();

  const paymentMethods = page.locator(
    '#checkout-payment-method-load input[type="radio"]',
  );

  await expect(paymentMethods.first()).toBeVisible();
  await paymentMethods.first().check();
  await page.locator('#payment-method-buttons-container input').click();

  await expect(page.locator('#checkout-payment-info-load')).toBeVisible();
  await page.locator('#payment-info-buttons-container input').click();

  const orderSummary = page.locator('#checkout-confirm-order-load');
  await expect(orderSummary).toBeVisible();
  await expect(
    orderSummary.getByRole('link', {
      name: 'Blue Jeans',
      exact: true,
    }),
  ).toBeVisible();

  await page.locator('#confirm-order-buttons-container input').click();

  await expect(
    page.getByText('Your order has been successfully processed!', {
      exact: true,
    }),
  ).toBeVisible();
});
