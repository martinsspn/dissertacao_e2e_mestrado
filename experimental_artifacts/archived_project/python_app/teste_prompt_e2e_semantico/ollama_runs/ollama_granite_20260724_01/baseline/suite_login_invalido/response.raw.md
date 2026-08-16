
1. First, install Playwright and TypeScript:
```bash
npm init -y
npm install --save-dev playwright typescript ts-node @types/playwright @types/node
npx tsc
npx playwright install
```

2. Create a new file `index.ts` and add the following code:

```typescript
import { chroot } from 'child_process';
import * as puppeteer from 'puppeteer';

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  // Navigate to the login page
  await page.goto('https://demo-web-shop.com/login');

  // Fill in the email and password fields with invalid values
  await page.fillIn('#email', 'invalid_email@example.com');
  await page.fillIn('#password', '');

  // Submit the login form
  await page.click('#login-button');

  // Wait for the login to complete
  await page.waitForNavigation();

  // Check if the user is unauthenticated
  const isAuthenticated = await page.evaluate(() => {
    return window.location.href === 'https://demo-web-shop.com/';
  });

  console.log('Login attempt with an invalid password:', isAuthenticated);
})();
```

3. Replace `'https://demo-web-shop.com/login'` with the actual login URL of your Demo Web Shop.

4. Run the script:
```bash
npx ts-node index.ts
```