
1. First, make sure you have Node.js and npm installed on your machine. If not, download and install them from https://nodejs.org/.

2. Create a new directory for your project and navigate to it in your terminal or command prompt.

3. Run the following command to create a new TypeScript project:
```
npx tsc --init
```
4. Install Playwright as a development dependency:
```
npm install playwright
```
5. Create a new file called `main.ts` and add the following code:
```typescript
import { chromium } from 'playwright';

(async () => {
  const browser = await chromium.launch();

  await browser.goto('https://demo-web-shop.com/login');

  await browser.fillInForm({
    email: 'test@example.com',
    password: 'password123',
  });

  await browser.click('login');

  const account = await browser.waitForSelector('.account-link');
  console.log(`Account link: ${account.innerText}`);

  await browser.close();
})();
```
6. Replace `'https://demo-web-shop.com/login'` with the actual URL of your login page.

7. Run the following command to start Playwright and open the demo web shop in a new tab:
```
npx playwright --headless
```
8. Open another terminal or command prompt window and navigate to the directory containing `main.ts`.

9. Run the following command to build and run your TypeScript project:
```
npm run build && npm start
```
This will create a production-ready TypeScript application that can be used to test the login functionality of your demo web shop.