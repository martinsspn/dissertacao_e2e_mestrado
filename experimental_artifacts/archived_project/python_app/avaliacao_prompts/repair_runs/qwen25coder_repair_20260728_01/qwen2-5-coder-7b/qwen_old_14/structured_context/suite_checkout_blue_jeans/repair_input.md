Condição experimental: structured_context

ESPECIFICAÇÃO ORIGINAL:
Complete purchase of the product Blue Jeans: The user is authenticated in an account with a valid billing and shipping address, using data provided by the testing environment. The user searches for Blue Jeans and opens the product page. The user adds Blue Jeans to the cart. The user accesses Shopping cart and confirms that the product is present. The user accepts the Terms of service and selects Checkout. The user confirms or provides valid Billing address data. The user confirms or provides valid Shipping address data. The user selects an available Shipping method option. The user selects an available Payment method option. The user reviews Payment information and proceeds. The user reviews the order and selects Confirm. The system informs that the order was processed successfully.


ARQUIVO GERADO QUE DEVE SER REPARADO:
```typescript
import { test, expect } from '@playwright/test';

test.describe('Suite Checkout Blue Jeans', () => {
  test('should complete the checkout process for blue jeans', async ({ page }) => {
    // Step 2: Search for Blue Jeans and open the product page
    await page.goto('https://demowebshop.tricentis.com/');
    await page.locator("[id=\"small-searchterms\"]").fill('Blue Jeans');
    await page.getByRole("button", { name: "Search", exact: true }).click();
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/blue-jeans');

    // Step 3: Add Blue Jeans to the cart
    await page.locator("[id=\"add-to-cart-button-36\"]").click();

    // Step 4: Access Shopping cart and confirm that the product is present
    await page.getByRole("link", { name: "Shopping cart", exact: true }).click();
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/cart');
    await expect(page.locator('h1').textContent()).toBe('Shopping cart');

    // Step 5: Accept the Terms of service and select Checkout
    await page.getByLabel('I agree with the terms', { exact: true }).check();
    await page.getByRole("button", { name: "Checkout", exact: true }).click();

    // Step 6: Confirm or provide valid Billing address data
    await page.locator("[id=\"BillingAddress_FirstName\"]").fill('John');
    await page.locator("[id=\"BillingAddress_LastName\"]").fill('Doe');
    await page.locator("[id=\"BillingAddress_Email\"]").fill('john.doe@example.com');
    await page.locator("[id=\"BillingAddress_CountryId\"]").selectOption({ label: 'United States' });
    await page.locator("[id=\"BillingAddress_StateProvinceId\"]").selectOption({ label: 'Alabama' });
    await page.locator("[id=\"BillingAddress_City\"]").fill('Montgomery');
    await page.locator("[id=\"BillingAddress_Address1\"]").fill('123 Main St');
    await page.locator("[id=\"BillingAddress_ZipPostalCode\"]").fill('36104');

    // Step 7: Confirm or provide valid Shipping address data
    await page.locator("[id=\"ShippingAddress_FirstName\"]").fill('John');
    await page.locator("[id=\"ShippingAddress_LastName\"]").fill('Doe');
    await page.locator("[id=\"ShippingAddress_Email\"]").fill('john.doe@example.com');
    await page.locator("[id=\"ShippingAddress_CountryId\"]").selectOption({ label: 'United States' });
    await page.locator("[id=\"ShippingAddress_StateProvinceId\"]").selectOption({ label: 'Alabama' });
    await page.locator("[id=\"ShippingAddress_City\"]").fill('Montgomery');
    await page.locator("[id=\"ShippingAddress_Address1\"]").fill('123 Main St');
    await page.locator("[id=\"ShippingAddress_ZipPostalCode\"]").fill('36104');

    // Step 8: Select an available Shipping method option
    await page.getByRole("radio", { name: "Next Day Air" }).click();

    // Step 9: Select an available Payment method option
    await page.getByLabel("Credit Card (Visa, MasterCard)").check();

    // Step 10: Review Payment information and proceed
    await page.locator("[id=\"CardholderName\"]").fill('John Doe');
    await page.locator("[id=\"CardNumber\"]").fill('4111111111111111');
    await page.locator("[id=\"ExpireMonth\"]").selectOption({ label: '01' });
    await page.locator("[id=\"ExpireYear\"]").selectOption({ label: '2025' });
    await page.locator("[id=\"CardCode\"]").fill('123');
    await page.getByRole("button", { name: "Continue" }).click();

    // Step 11: Review the order and select Confirm
    await expect(page.locator('h1').textContent()).toBe('Order review');
    await page.getByRole("button", { name: "Confirm" }).click();

    // Step 12: System informs that the order was processed successfully
    await expect(page.locator('h1').textContent()).toBe('Your order has been successfully processed!');
  });
});

```

EVIDÊNCIA DA FALHA DE EXECUÇÃO:
Error: expect(page).toHaveURL(expected) failed

Expected: "https://demowebshop.tricentis.com/blue-jeans"
Received: "https://demowebshop.tricentis.com/search?q=Blue+Jeans"
Timeout:  7000ms

Call log:
  - Expect "toHaveURL" with timeout 7000ms
    17 × unexpected value "https://demowebshop.tricentis.com/search?q=Blue+Jeans"

DIAGNÓSTICO DA REVISÃO:
Omite autenticação, espera redirecionamento direto da busca e inventa grande parte do checkout.

PROMPT ESTRUTURADO ORIGINAL DESTA CONDIÇÃO:
# Geracao de teste E2E Playwright

Gere um teste TypeScript Playwright fiel a especificacao.

Regras:
- Retorne um unico bloco de codigo `typescript`, sem texto fora dele; o conteudo interno deve ser um arquivo Playwright `.spec.ts` completo e executavel por `npx playwright test`.
- Importe `test` e `expect` de `@playwright/test`.
- Inicie com `await page.goto('https://demowebshop.tricentis.com/')`; use URLs literais tambem em `toHaveURL`, sem regex ou links Markdown.
- Nao derive rotas do texto de links, produtos ou titulos. Use `toHaveURL` somente quando a URL exata estiver na base ou no contexto; sem URL observada, confirme a pagina por elementos visiveis.
- Use locators Playwright legiveis e unicos no modo estrito; evite XPath, indices e `waitForTimeout`.
- Cada valor `locator_playwright=...` e uma expressao TypeScript Playwright completa e executavel. Copie a expressao sem aspas adicionais e aplique a acao nela, por exemplo `await page.getByRole('button', { name: 'Search', exact: true }).click()` ou `await page.getByLabel('Email:', { exact: true }).fill(valor)`.
- Nunca passe uma expressao `page.getBy*` ou `page.locator` como argumento de `page.click`, `page.fill` ou `page.selectOption`; chame `.click()`, `.fill()` ou `.selectOption()` diretamente no locator.
- Nao use no codigo a notacao descritiva de `controle=...` nem invente engines como `role_name:`, `label:`, `id:`, `tag=` ou `text:`. Somente os valores de `locator_playwright=...` sao locators copiaveis.
- Quando o contexto fornecer `locator_playwright`, preserve esse locator; nao o substitua por um locator generico baseado apenas em papel e nome.
- Quando varios itens ou variantes compartilharem a mesma acao, relacione o controle escolhido ao nome visivel do item antes do clique e reutilize esse nome nas verificacoes posteriores; nao trate o titulo da pagina agrupadora como nome do item sem confirmar essa igualdade. Se o nome exato nao puder ser observado, verifique apenas a propriedade explicitada pela especificacao, sem inventar um rotulo.
- Inclua assercoes observaveis que comprovem o resultado esperado.
- O contexto é apenas um guia: combine-o com a especificacao e sua experiencia para navegar, localizar elementos e executar as acoes.
- Caso seja possível acessar a aplicação, entre nela e interaja validando o fluxo e os resultados e utilizando as informações obtidas nessa interação em conjunto do contexto e a especificacao e seu conhecimento de playwright para fazer o teste ts; caso contrario, use a especificacao, o contexto observado e seu conhecimento de Playwright sem afirmar que executou acoes.

Especificacao `Suite Checkout Blue Jeans` em etapas:
1. The user is authenticated in an account with a valid billing and shipping address, using data provided by the testing environment.
2. The user searches for Blue Jeans and opens the product page.
3. The user adds Blue Jeans to the cart.
4. The user accesses Shopping cart and confirms that the product is present.
5. The user accepts the Terms of service and selects Checkout.
6. The user confirms or provides valid Billing address data.
7. The user confirms or provides valid Shipping address data.
8. The user selects an available Shipping method option.
9. The user selects an available Payment method option.
10. The user reviews Payment information and proceeds.
11. The user reviews the order and selects Confirm.
12. The system informs that the order was processed successfully.

Contexto estruturado por etapa:
Etapa 2 (R2):
- pagina=https://demowebshop.tricentis.com/
- controle_1=tag=input, id=small-searchterms, name=q, input_type=text, value=Search store, form_action=/search, form_method=GET
- operacao_1=fill
- locator_playwright_1=page.locator("[id=\"small-searchterms\"]")
- controle_2=tag=input, input_type=submit, value=Search, form_action=/search, form_method=GET
- operacao_2=click
- locator_playwright_2=page.getByRole("button", { name: "Search", exact: true })
- pagina_evidencia=https://demowebshop.tricentis.com/blue-jeans
- evidencia_pagina=h1:Blue Jeans
Etapa 3 (R3):
- pagina=https://demowebshop.tricentis.com/blue-jeans
- controle=tag=input, id=add-to-cart-button-36, input_type=button, value=Add to cart, form_action=/blue-jeans, form_method=POST
- operacao=click
- locator_playwright=page.locator("[id=\"add-to-cart-button-36\"]")
Etapa 4 (R4):
- pagina=https://demowebshop.tricentis.com/blue-jeans
- controle=tag=a, text=Shopping cart, href=/cart
- operacao=click
- destino=https://demowebshop.tricentis.com/cart
- locator_playwright=page.getByRole("link", { name: "Shopping cart", exact: true })
- pagina_evidencia=https://demowebshop.tricentis.com/cart
- evidencia_pagina=h1:Shopping cart
Etapas sem contexto observado: 1, 5, 6, 7, 8, 9, 10, 11, 12.

Use as informacoes observadas quando forem aplicaveis, sem limitar o teste a elas.
`pagina_evidencia` nao comprova uma transicao ate a pagina.
Sem contexto, siga a especificacao e interaja normalmente com a pagina; nao trate inferencias como fatos observados.


Faça uma única tentativa de reparo. Mantenha todas as verificações exigidas e devolva o arquivo TypeScript completo.