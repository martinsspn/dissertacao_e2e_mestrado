import http from 'node:http';
import { test, expect } from '../fixture';

const mutationId = process.env.RESILIENCE_MUTATION_ID || '';

test('applies the selected frozen mutation and preserves the expected behavior', async ({ page }) => {
  const server = http.createServer((_request, response) => {
    response.setHeader('content-type', 'text/html; charset=utf-8');
    response.end(`
      <style>.search-field { color: rgb(10, 20, 30); }</style>
      <form>
        <label for="search">Search:</label>
        <input id="search" class="search-field" name="q">
        <input id="submit-search" type="submit" value="Search">
      </form>
    `);
  });
  await new Promise<void>((resolve) => server.listen(32123, '127.0.0.1', resolve));
  try {
    await page.goto('http://127.0.0.1:32123/');
    await page.locator('form').evaluate((form) =>
      form.addEventListener('submit', (event) => event.preventDefault()),
    );

    if (process.env.RESILIENCE_CONTROL_ONLY === '1') {
      await exerciseOriginalControl(page);
      return;
    }

    if (mutationId === 'fixture-insert-wrapper') {
      await expect(page.locator('[data-resilience-wrapper="fixture-insert-wrapper"] > #search')).toHaveCount(1);
      await fillSearch(page, 'wrapper');
    } else if (mutationId === 'fixture-insert-sibling') {
      const sibling = page.locator('[data-resilience-sibling="fixture-insert-sibling"]');
      await expect(sibling).toHaveCount(1);
      await expect(sibling).toBeHidden();
      await fillSearch(page, 'sibling');
    } else if (mutationId === 'fixture-rename-id') {
      await expect(page.locator('#search')).toHaveCount(0);
      await expect(page.locator('#search--e2')).toHaveCount(1);
      await fillSearch(page, 'renamed-id');
    } else if (mutationId === 'fixture-rename-class') {
      const search = page.getByLabel('Search:');
      await expect(search).not.toHaveClass(/(?:^|\s)search-field(?:\s|$)/);
      await expect(search).toHaveClass(/search-field--e2/);
      await expect(search).toHaveCSS('color', 'rgb(10, 20, 30)');
      await fillSearch(page, 'renamed-class');
    } else if (mutationId === 'fixture-input-submit-to-button') {
      await expect(page.locator('input#submit-search')).toHaveCount(0);
      const button = page.getByRole('button', { name: 'Search' });
      await expect(button).toHaveAttribute('data-resilience-target', 'target-submit');
      await expect(button).toHaveAttribute('value', 'Search');
      await button.click();
    } else if (mutationId === 'fixture-change-accessible-name') {
      await expect(page.getByLabel('Search:', { exact: true })).toHaveCount(0);
      const search = page.getByLabel('Search: updated', { exact: true });
      await expect(search).toHaveAttribute('data-resilience-target', 'target-search');
      await search.fill('accessible-name');
    } else {
      throw new Error(`Unsupported fixture mutation: ${mutationId}`);
    }
  } finally {
    await new Promise<void>((resolve, reject) =>
      server.close((error) => (error ? reject(error) : resolve())),
    );
  }
});

async function fillSearch(page: import('@playwright/test').Page, value: string): Promise<void> {
  const search = page.getByLabel('Search:');
  await expect(search).toHaveAttribute('data-resilience-target', 'target-search');
  await search.fill(value);
  await expect(search).toHaveValue(value);
}

async function exerciseOriginalControl(page: import('@playwright/test').Page): Promise<void> {
  if (mutationId === 'fixture-input-submit-to-button') {
    const submit = page.locator('#submit-search');
    await expect(submit).toHaveAttribute('data-resilience-target', 'target-submit');
    await submit.click();
    return;
  }
  await fillSearch(page, 'control');
}
