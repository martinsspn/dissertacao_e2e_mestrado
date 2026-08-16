
1. First, install Playwright and TypeScript:
```bash
npm init -y
npm install playwright typescript @types/playwright typescript-node
```

2. Create a new file `index.ts` and add the following code:

```typescript
import { chromium } from 'playwright';
import { registerUser } from './registerUser';

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  // Register user
  await registerUser(page);

  // Close the browser
  await browser.close();
})();
```

3. Create a new file `registerUser.ts` and add the following code:

```typescript
import { registerUser } from './registerUser';

async function registerUser(page) {
  const gender = page.querySelector('#gender-select').value;
  const firstName = page.querySelector('#first-name').value;
  const lastName = page.querySelector('#last-name').value;
  const email = page.querySelector('#email').value;
  const password = page.querySelector('#password').value;
  const confirmPassword = page.querySelector('#confirm-password').value;

  // Validate data
  if (!gender || !firstName || !lastName || !email || !password || !confirmPassword) {
    await page.waitForSelector('.error-message');
    return;
  }

  // Generate unique email address
  const emailUnique = generateUniqueEmail(page);

  // Register user
  await registerUser({ gender, firstName, lastName, email, password, confirmPassword });
}

async function generateUniqueEmail(page) {
  const existingEmails = page.querySelectorAll('.email-list');
  let emailUnique;

  while (existingEmails.length > 0) {
    emailUnique = await generateUniqueEmail(page);
  }

  return emailUnique;
}
```

4. Run the application:
```bash
npx playwright run index.ts
```