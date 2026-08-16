
1. First, install Playwright and TypeScript globally using npm:
```
npm install -g playwright typescript-node
```
2. Create a new directory for your project and navigate to it:
```
mkdir teste-e2e-typescript
cd teste-e2e-typescript
```
3. Initialize a new TypeScript project using `tsc`:
```
npx tsc --init
```
4. Install Playwright as a development dependency:
```
npm install playwright
```
5. Create a new file named `main.ts` and add the following code:
```typescript
import { chromium } from 'playwright';

async function main() {
  const browser = await chromium.launch();

  // Navigate to the login page
  await browser.goto('https://example.com/login');

  // Enter valid credentials
  await browser.fillInForm({
    username: 'valid_username',
    password: 'valid_password',
  });

  // Click the Log in button
  await browser.click(document.querySelector('#login-button'));

  // Wait for the page to load
  await browser.waitForNavigation();

  // Display the Log in link again
  await browser.goto('https://example.com/login');
}

main().catch((error) => {
  console.error('Error:', error);
});
```
6. Replace `'https://example.com/login'` with the actual login page URL of your application.
7. Run the script using `npx playwright main.ts`:
```
npx playwright main.ts
```