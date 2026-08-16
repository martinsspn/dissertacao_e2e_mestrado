import { chromium } from 'playwright';
import { randomUUID } from 'node:crypto';

const suffix = randomUUID().replaceAll('-', '').slice(0, 16);
const email = `repair-${suffix}@example.com`;
const password = `Repair-${suffix}!A1`;
const firstName = 'Repair';
const lastName = 'Evaluation';

const browser = await chromium.launch({ channel: 'chromium', headless: true });
try {
  const context = await browser.newContext();
  const page = await context.newPage();
  await page.goto('https://demowebshop.tricentis.com/register');
  await page.locator('#gender-male').check();
  await page.locator('#FirstName').fill(firstName);
  await page.locator('#LastName').fill(lastName);
  await page.locator('#Email').fill(email);
  await page.locator('#Password').fill(password);
  await page.locator('#ConfirmPassword').fill(password);
  await page.locator('#register-button').click();
  await page.getByText('Your registration completed', { exact: false }).waitFor();
  process.stdout.write(JSON.stringify({ email, password, firstName, lastName }));
} finally {
  await browser.close();
}

