import { test } from '@playwright/test';
import { expect } from '@playwright/test';

describe('Logout', () => {
  it('should log out the user and display the login link again', async () => {
    // Step 1: The user is authenticated with valid credentials provided by the testing environment.
    await page.goto('https://demowebshop.tricentis.com/');

    // Step 2: The user selects Log out.
    const logoutButton = await page.locator('#logout-button');
    await logoutButton.click();

    // Step 3: The system terminates the session.
    await page.waitForSelector('.login-link');

    // Step 4: The system displays the Log in link again.
    await page.waitForSelector('.login-link');
  });
});
