
```typescript
import { test } from '@playwright/test';
import { expect } from '@playwright/test';

describe('Suite Adicionar Carrinho', () => {
  it('Adicionar carrinho ao produto Blue Jeans', async () => {
    const page = await test.chromium.launch();
    const context = await page.context();

    // Etapa 1 (R1)
    const smallSearchTermsInput = await context.query('#small-searchterms');
    const searchStoreButton = await context.query('#search');
    const addToCartButton36 = await context.query('#add-to-cart-button-36');

    // Etapa 2 (R2)
    const blueJeansPage = await context.page.goto('https://demowebshop.tricentis.com/blue-jeans');
    expect(blueJeansPage).toHaveURL();

    // Etapa 3 (R3)
    const addToCartButton36Input = await context.query('#add-to-cart-button-36');
    expect(addToCartButton36Input).toHaveURL();

    // Etapa 5 (R5)
    const cartPage = await context.page.goto('https://demowebshop.tricentis.com/cart');
    expect(cartPage).toHaveURL();
  });
});
```