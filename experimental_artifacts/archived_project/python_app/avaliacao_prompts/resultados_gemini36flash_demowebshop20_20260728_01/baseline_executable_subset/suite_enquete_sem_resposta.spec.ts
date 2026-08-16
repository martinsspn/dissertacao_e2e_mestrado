import { test, expect } from '@playwright/test';

test.describe('Community Poll', () => {
  test('should inform user to select an answer when attempting to vote without selection', async ({ page }) => {
    const baseUrl = process.env.BASE_URL || 'https://demowebshop.tricentis.com/';
    await page.goto(baseUrl);

    // Verify the Community Poll header / question exists
    const pollTitle = page.getByText('Do you like nopCommerce?');
    await expect(pollTitle).toBeVisible();

    let dialogMessage = '';
    page.on('dialog', async (dialog) => {
      dialogMessage = dialog.message();
      await dialog.accept();
    });

    // Click the Vote button without selecting any radio option
    const voteButton = page.getByRole('button', { name: 'Vote' });
    await voteButton.click();

    // Verify user is informed to select an answer (via browser alert or inline notification element)
    const pollErrorElement = page.locator('#block-poll-vote-error-1');
    
    if (dialogMessage) {
      expect(dialogMessage.toLowerCase()).toContain('select an answer');
    } else {
      await expect(pollErrorElement).toBeVisible();
      await expect(pollErrorElement).toContainText(/select an answer/i);
    }
  });
});
