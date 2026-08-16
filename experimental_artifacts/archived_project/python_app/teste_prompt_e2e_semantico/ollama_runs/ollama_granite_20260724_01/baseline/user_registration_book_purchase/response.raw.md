
1. First, install Playwright and TypeScript:
```bash
npm init -y
npm install --save-dev playwright typescript @types/playwright typescript-node
npx tsc && npx playwright
```

2. Create a new file `src/index.ts` and add the following code:

```typescript
import { chroot } from 'playwright';
import { registerUser, getCart } from './lib';

(async () => {
  const browser = await chroot('http://localhost:3000');

  // Register user
  await registerUser({
    email: 'user@example.com',
    password: 'secure_password',
    firstName: 'John',
    lastName: 'Doe',
  });

  // Navigate to the book list page
  await browser.goto('http://localhost:3000/books');

  // Add a book to the cart
  const bookHealthBook = await getCart().then((cart) => {
    return cart.find((book) => book.id === 'Health Book');
  });

  if (bookHealthBook) {
    await bookHealthBook.addToCart();

    // Display success notification
    console.log('Book added to the cart successfully.');
  }
})();
```

3. Create a new file `src/lib` and add the following code:

```typescript
export async function registerUser(userData: { email: string, password: string, firstName: string, lastName: string }): Promise<void> {
  // Implement user registration logic here
  console.log('User registered successfully.');
}

export async function getCart(): Promise<any[]> {
  // Implement cart retrieval logic here
  return [{ id: 'Health Book', quantity: 1 }];
}
```

4. Run the application using Playwright:

```bash
npx playwright run src/index.ts
```