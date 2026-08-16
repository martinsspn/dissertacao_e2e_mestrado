```typescript
import { test, expect } from '@playwright/test';

test.describe('Suite Configurar Desktop', () => {
  test('configura um desktop e o adiciona ao carrinho', async ({ page }) => {
    await page.goto('https://demowebshop.tricentis.com/');

    await page
      .locator('.top-menu')
      .getByRole('link', { name: 'Computers' })
      .click();

    await expect(page).toHaveURL(
      'https://demowebshop.tricentis.com/computers',
    );
    await expect(
      page.getByRole('heading', { name: 'Computers' }),
    ).toBeVisible();

    await page
      .locator('.category-grid')
      .getByRole('link', { name: 'Desktops' })
      .click();

    await expect(page).toHaveURL(
      'https://demowebshop.tricentis.com/desktops',
    );
    await expect(
      page.getByRole('heading', { name: 'Desktops' }),
    ).toBeVisible();

    const desktopName = 'Build your own cheap computer';

    const configurableDesktop = page
      .locator('.product-item')
      .filter({
        has: page.getByRole('link', {
          name: desktopName,
        }),
      });

    await expect(configurableDesktop).toBeVisible();

    await configurableDesktop
      .getByRole('link', {
        name: desktopName,
      })
      .click();

    await expect(page).toHaveURL(
      'https://demowebshop.tricentis.com/build-your-cheap-own-computer',
    );
    await expect(
      page.getByRole('heading', {
        name: desktopName,
      }),
    ).toBeVisible();

    const fastProcessor = page.getByLabel('Fast [+100.00]');
    const fourGbMemory = page.getByLabel('4 GB [+20.00]');
    const fourHundredGbDisk = page.getByLabel('400 GB [+100.00]');
    const officeSuite = page.getByLabel('Office Suite [+100.00]');

    await fastProcessor.check();
    await fourGbMemory.check();
    await fourHundredGbDisk.check();
    await officeSuite.check();

    await expect(fastProcessor).toBeChecked();
    await expect(fourGbMemory).toBeChecked();
    await expect(fourHundredGbDisk).toBeChecked();
    await expect(officeSuite).toBeChecked();

    await page
      .getByRole('button', { name: 'Add to cart' })
      .click();

    const notification = page.locator('#bar-notification');

    await expect(notification).toBeVisible();
    await expect(notification).toContainText(
      'The product has been added to your shopping cart',
    );

    await page
      .getByRole('link', { name: 'Shopping cart' })
      .click();

    await expect(page).toHaveURL(
      'https://demowebshop.tricentis.com/cart',
    );
    await expect(
      page.getByRole('heading', {
        name: 'Shopping cart',
      }),
    ).toBeVisible();

    const configuredDesktopCartItem = page
      .locator('tr.cart-item-row')
      .filter({
        has: page.getByRole('link', {
          name: desktopName,
        }),
      });

    await expect(configuredDesktopCartItem).toBeVisible();
    await expect(
      configuredDesktopCartItem.getByRole('link', {
        name: desktopName,
      }),
    ).toBeVisible();

    const configuration = configuredDesktopCartItem.locator('.attributes');

    await expect(configuration).toContainText('Fast');
    await expect(configuration).toContainText('4 GB');
    await expect(configuration).toContainText('400 GB');
    await expect(configuration).toContainText('Office Suite');
  });
});
```