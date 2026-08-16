import { test, expect } from '@playwright/test';

test.describe('Suite Detalhes Fiction', () => {
  test('The user searches for the product Fiction in the Search store field and opens its details page', async ({ page }) => {
    await page.goto('https://demowebshop.tricentis.com/');

    // Etapa 1: The user searches for the product Fiction in the Search store field.
    const searchInput = page.locator("[id=\"small-searchterms\"]");
    await searchInput.fill('Fiction');
    const searchButton = page.getByRole("button", { name: "Search", exact: true });
    await searchButton.click();

    // Etapa 2: The user opens the product Fiction in the search results.
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/fiction');

    // Etapa 3: The system displays the details page with the name Fiction.
    const fictionTitle = page.locator("h1", { hasText: "Fiction" });
    await expect(fictionTitle).toBeVisible();

    // Etapa 4: The system presents the available price information for the product.
    // Assuming there is a price element, e.g., <span class="price">$29.99</span>
    const priceElement = page.locator("span.price");
    await expect(priceElement).toBeVisible();
  });
});
