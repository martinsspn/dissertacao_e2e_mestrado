import { test, expect } from '../../../playwright_resilience/fixture.ts';

test.describe('Suite Configurar Desktop', () => {
  test('configura um desktop e o adiciona ao carrinho', async ({ page }) => {
    await page.goto('https://demowebshop.tricentis.com/');

    await page
      .locator('.top-menu')
      .getByRole('link', { name: 'Computers', exact: true })
      .click();

    await expect(page).toHaveURL(
      'https://demowebshop.tricentis.com/computers',
    );
    await expect(
      page.getByRole('heading', { name: 'Computers', exact: true }),
    ).toBeVisible();

    await page
      .locator('.category-grid')
      .getByRole('link', { name: 'Desktops', exact: true })
      .click();

    await expect(page).toHaveURL(
      'https://demowebshop.tricentis.com/desktops',
    );
    await expect(
      page.getByRole('heading', { name: 'Desktops', exact: true }),
    ).toBeVisible();

    const desktopName = 'Build your own cheap computer';

    const configurableDesktop = page
      .locator('.product-item')
      .filter({
        has: page.getByRole('link', {
          name: desktopName,
          exact: true,
        }),
      });

    await expect(configurableDesktop).toBeVisible();

    await configurableDesktop
      .getByRole('link', {
        name: desktopName,
        exact: true,
      })
      .click();

    await expect(page).toHaveURL(
      'https://demowebshop.tricentis.com/build-your-cheap-own-computer',
    );
    await expect(
      page.getByRole('heading', {
        name: desktopName,
        exact: true,
      }),
    ).toBeVisible();

    const fastProcessor = page.getByLabel('Fast [+100.00]', {
      exact: true,
    });
    const fourGbMemory = page.getByLabel('4 GB [+20.00]', {
      exact: true,
    });
    const fourHundredGbDisk = page.getByLabel('400 GB [+100.00]', {
      exact: true,
    });
    const officeSuite = page.getByLabel('Office Suite [+100.00]', {
      exact: true,
    });

    await fastProcessor.check();
    await fourGbMemory.check();
    await fourHundredGbDisk.check();
    await officeSuite.check();

    await expect(fastProcessor).toBeChecked();
    await expect(fourGbMemory).toBeChecked();
    await expect(fourHundredGbDisk).toBeChecked();
    await expect(officeSuite).toBeChecked();

    await page
      .getByRole('button', { name: 'Add to cart', exact: true })
      .click();

    const notification = page.locator('#bar-notification');

    await expect(notification).toBeVisible();
    await expect(notification).toContainText(
      'The product has been added to your shopping cart',
    );

    await page
      .getByRole('link', { name: 'Shopping cart', exact: true })
      .click();

    await expect(page).toHaveURL(
      'https://demowebshop.tricentis.com/cart',
    );
    await expect(
      page.getByRole('heading', {
        name: 'Shopping cart',
        exact: true,
      }),
    ).toBeVisible();

    const configuredDesktopCartItem = page
      .locator('tr.cart-item-row')
      .filter({
        has: page.getByRole('link', {
          name: desktopName,
          exact: true,
        }),
      });

    await expect(configuredDesktopCartItem).toBeVisible();
    await expect(
      configuredDesktopCartItem.getByRole('link', {
        name: desktopName,
        exact: true,
      }),
    ).toBeVisible();

    const configuration = configuredDesktopCartItem.locator('.attributes');

    await expect(configuration).toContainText('Fast');
    await expect(configuration).toContainText('4 GB');
    await expect(configuration).toContainText('400 GB');
    await expect(configuration).toContainText('Office Suite');
  });
});
