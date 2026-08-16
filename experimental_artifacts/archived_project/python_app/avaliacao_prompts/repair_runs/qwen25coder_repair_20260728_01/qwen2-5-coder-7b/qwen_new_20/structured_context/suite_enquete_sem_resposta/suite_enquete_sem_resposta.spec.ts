import { test, expect } from '@playwright/test';

test.describe('Suite Enquete Sem Resposta', () => {
  test('The user accesses the Demo Web Shop home page in a new browser context and tries to vote without selecting an answer', async ({ page }) => {
    await page.goto('https://demowebshop.tricentis.com/');
    await expect(page).toHaveTitle('Demo Web Shop');

    const voteButton = page.locator("[id=\"vote-poll-1\"]");
    await voteButton.click();

    await expect(voteButton).toBeEnabled();
    await expect(page).toHaveText('Please select an answer before voting.');
  });
});
