import { test } from '@playwright/test';
import { expect } from '@playwright/test';

describe('Fiction Product', () => {
  it('should display the product Fiction in the search results', async () => {
    await page.goto('https://demowebshop.tricentis.com/');

    const control_1 = await page.locator('#small-searchterms');
    await control_1.fill('Search store');
    await control_1.click();

    const seletor_1 = await page.locator('#search');
    await seletor_1.click();

    const evidencia_pagina = await page.locator('#fiction');
    expect(await evidencia_pagina).toHaveText('Fiction');
  });

  it('should display the details page with the name Fiction', async () => {
    await page.goto('https://demowebshop.tricentis.com/fiction');

    const seletor_2 = await page.locator('#details');
    expect(await seletor_2).toHaveText('Fiction');
  });

  it('should display the available price information for the product', async () => {
    await page.goto('https://demowebshop.tricentis.com/fiction');

    const evidencia_pagina = await page.locator('#price');
    expect(await evidencia_pagina).toHaveText('Available Price: $100');
  });
});
