Condição experimental: baseline

ESPECIFICAÇÃO ORIGINAL:
Searching for a nonexistent product: The user enters a unique term that does not correspond to any product in the Search store field. The user submits the search. The system displays the Search page and informs that no products matched the search criteria.


ARQUIVO GERADO QUE DEVE SER REPARADO:
```typescript
import { test, expect } from '@playwright/test';

test.describe('Search for nonexistent product', () => {
  test('should display no results message when searching for a nonexistent product', async ({ page }) => {
    // Navigate to the Search page
    await page.goto('/search');

    // Enter a unique term that does not correspond to any product
    const searchInput = page.locator('#search-input');
    await searchInput.fill('nonexistent-product-term');

    // Submit the search
    const searchButton = page.locator('#search-button');
    await searchButton.click();

    // Verify that the Search page is displayed
    expect(page.url()).toContain('/search');

    // Verify that no products matched the search criteria
    const noResultsMessage = page.locator('.no-results-message');
    await expect(noResultsMessage).toBeVisible();
    await expect(noResultsMessage).toHaveText('No products matched the search criteria.');
  });
});

```

EVIDÊNCIA DA FALHA DE EXECUÇÃO:
TimeoutError: locator.fill: Timeout 10000ms exceeded.
Call log:
  - waiting for locator('#search-input')

DIAGNÓSTICO DA REVISÃO:
Fluxo e intenção do oráculo estão presentes, mas os controles e a mensagem pertencem a uma interface inventada.

Faça uma única tentativa de reparo. Mantenha todas as verificações exigidas e devolva o arquivo TypeScript completo.