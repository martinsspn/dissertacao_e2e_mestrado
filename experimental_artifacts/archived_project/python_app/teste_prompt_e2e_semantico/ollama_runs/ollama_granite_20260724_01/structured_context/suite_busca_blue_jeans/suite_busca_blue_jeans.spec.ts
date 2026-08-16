import { test } from '@playwright/test';
import { expect } from '@playwright/test';

describe('Suite Busca Blue Jeans', () => {
  it('Busca e seleciona o campo de busca', async () => {
    const page = await playwright.chromium.launch();
    const context = await page.context();

    // Step 1: The user searches for the product Blue Jeans in the Search store field.
    const searchTerm = await context.query('#small-searchterms');
    expect(await searchTerm).toHaveURL('https://demowebshop.tricentis.com/search');

    // Step 2: The system displays the results related to the search.
    const searchResults = await context.query('#search');
    expect(await searchResults).toHaveURL('https://demowebshop.tricentis.com/results');

    // Step 3: The user opens the product Blue Jeans from the results.
    const blueJeansLink = await context.query('#blue-jeans');
    expect(await blueJeansLink).toHaveURL('https://demowebshop.tricentis.com/blue-jeans');

    // Step 4: The system displays the details page with the name Blue Jeans.
    const blueJeansDetails = await context.query('#details');
    expect(await blueJeansDetails).toHaveURL('https://demowebshop.tricentis.com/details');
  });
});
