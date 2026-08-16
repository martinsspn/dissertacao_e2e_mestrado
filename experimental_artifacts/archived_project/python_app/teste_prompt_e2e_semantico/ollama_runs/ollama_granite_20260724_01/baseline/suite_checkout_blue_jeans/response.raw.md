
1. First, install Playwright and TypeScript:
```bash
npm init -y
npm install --save-dev playwright typescript ts-node @types/playwright @types/node
npx tsc
npx playwright
```

2. Create a new file `index.ts` and add the following code:

```typescript
import { chroot } from 'playwright';
import { createBrowserContext } from '@playwright/shared-context';
import { getPage, waitFor } from 'playwright';

const context = createBrowserContext({
  headless: true,
  networkTimeout: 10000,
});

async function main() {
  const browser = await chroot(context);

  // Navigate to the product page
  await browser.goto('https://example.com/blue-jeans');

  // Add Blue Jeans to the cart
  await waitFor(browser, 1000, () => {
    const cartItem = await browser.querySelector('.cart-item');
    if (cartItem) {
      cartItem.click();
    }
  });

  // Access Shopping cart and confirm product presence
  await waitFor(browser, 2000, () => {
    const shoppingCart = await browser.querySelector('.shopping-cart');
    if (shoppingCart) {
      shoppingCart.click();
    }
  });

  // Accept Terms of service and select Checkout
  await waitFor(browser, 3000, () => {
    const termsOfService = await browser.querySelector('.terms-of-service');
    if (termsOfService) {
      termsOfService.click();
    }

    const checkoutButton = await browser.querySelector('.checkout-button');
    if (checkoutButton) {
      checkoutButton.click();
    }
  });

  // Provide valid Billing and Shipping address data
  await waitFor(browser, 4000, () => {
    const billingAddressInput = await browser.querySelector('#billing-address');
    if (billingAddressInput) {
      billingAddressInput.value = '123 Main St';
    }

    const shippingAddressInput = await browser.querySelector('#shipping-address');
    if (shippingAddressInput) {
      shippingAddressInput.value = '456 Elm St';
    }
  });

  // Select an available Shipping method option and Payment method option
  await waitFor(browser, 5000, () => {
    const shippingMethodInput = await browser.querySelector('#shipping-method');
    if (shippingMethodInput) {
      shippingMethodInput.value = 'Standard';
    }

    const paymentMethodInput = await browser.querySelector('#payment-method');
    if (paymentMethodInput) {
      paymentMethodInput.value = 'Credit Card';
    }
  });

  // Review Payment information and proceed
  await waitFor(browser, 6000, () => {
    const paymentInfoInput = await browser.querySelector('#payment-info');
    if (paymentInfoInput) {
      paymentInfoInput.focus();
    }

    const confirmButton = await browser.querySelector('.confirm-button');
    if (confirmButton) {
      confirmButton.click();
    }
  });

  // Review the order and select Confirm
  await waitFor(browser, 7000, () => {
    const orderSummaryInput = await browser.querySelector('#order-summary');
    if (orderSummaryInput) {
      orderSummaryInput.focus();
    }

    const confirmButton = await browser.querySelector('.confirm-button');
    if (confirmButton) {
      confirmButton.click();
    }
  });

  // System informs that the order was processed successfully
  await waitFor(browser, 8000, () => {
    console.log('Order processed successfully.');
  });
}

main().catch((error) => {
  console.error('Error:', error);
});
```

3. Replace `'https://example.com/blue-jeans'` with the actual URL of the product page.

4. Run the script:
```bash
npx ts-node index.ts
```