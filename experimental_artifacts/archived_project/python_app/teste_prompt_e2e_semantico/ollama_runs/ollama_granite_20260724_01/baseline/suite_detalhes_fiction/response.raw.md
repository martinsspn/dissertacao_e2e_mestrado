
1. First, install Playwright and TypeScript:
```bash
npm init -y
npm install --save-dev playwright typescript @types/playwright typescript-node
npx tsc && npm install playwright
```

2. Create a `tsconfig.json` file with the following content:
```json
{
  "compilerOptions": {
    "target": "es6",
    "module": "commonjs",
    "strict": true,
    "esModuleInterop": true,
    "outDir": "./dist"
  },
  "include": ["src/**/*.ts"],
  "exclude": ["node_modules"]
}
```

3. Create a `src` folder and an `index.ts` file inside it:
```typescript
import { createBrowser } from 'playwright';

const browser = createBrowser();

async function main() {
  const page = await browser.newPage();

  await page.goto('https://example.com/search?query=Fiction');

  await page.waitForSelector('.product-name', {
    name: 'Fiction'
  });

  await page.waitForSelector('.price', {
    name: 'Price'
  });

  console.log(await page.getText('#price'));
}

main().catch((error) => {
  console.error('Error:', error);
});
```

4. Replace `'https://example.com/search?query=Fiction'` with the actual URL of your search store.

5. Run the script:
```bash
npx ts-node src/index.ts
```