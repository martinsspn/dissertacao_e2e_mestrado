
```typescript
import { test } from '@playwright/test';
import { expect } from '@playwright/test';

describe('Fluxo Computadores Desktops', () => {
  beforeEach(() => {
    await page.goto('https://demowebshop.tricentis.com/');
  });

  it('verifica que a página Digital downloads é exibida', async () => {
    const control = await page.locator('.tag-a, .text-digital-downloads, .href/digital-downloads');
    expect(await control).toBeVisible();

    // Use the 'page_evidencia' variable to verify that the digital downloads page is visible
  });
});
```