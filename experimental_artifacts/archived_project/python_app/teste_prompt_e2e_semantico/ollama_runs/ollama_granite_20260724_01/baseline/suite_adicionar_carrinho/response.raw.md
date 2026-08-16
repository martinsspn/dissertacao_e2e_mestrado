
1. First, install Playwright and TypeScript:
```bash
npm init -y
npm install playwright typescript @types/playwright typescript-node
```

2. Create a new file `index.ts` and add the following code:

```typescript
import { chromium } from 'playwright';
import { createBrowserContext } from '@types/playwright';
import { getPage, waitFor } from 'playwright';

const browser = await createBrowserContext({ headless: true });
const page = await browser.newPage();

async function addProductToCart() {
  const searchStoreField = document.querySelector('#search-store');
  const blueJeansProduct = document.querySelector('.product-blue-jeans');

  // Search for Blue Jeans in the search store field
  await searchStoreField.focus();
  await searchStoreField.sendKeys('Blue Jeans');
  await waitFor(page, 100);

  // Open the product page and add it to the cart
  const blueJeansProductPage = document.querySelector('.product-blue-jeans-page');
  await blueJeansProductPage.focus();
  await blueJeansProductPage.clickOn('Add to Cart');
}

async function accessShoppingCart() {
  // Navigate to the shopping cart page
  const shoppingCartPage = await browser.goto('/shopping-cart');

  // Display Blue Jeans among the items in the cart
  await waitFor(page, 100);
  await blueJeansProductPage.focus();
  await blueJeansProductPage.clickOn('View Cart');
}

addProductToCart().catch((error) => {
  console.error('Error adding product to cart:', error);
});

accessShoppingCart().catch((error) => {
  console.error('Error accessing shopping cart:', error);
});
```

3. Run the script:
```bash
npx playwright run index.ts
```