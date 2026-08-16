Condição experimental: structured_context

ESPECIFICAÇÃO ORIGINAL:
Updating a product quantity in the cart: The user adds Computing and Internet to the cart to prepare the scenario. The user accesses Shopping cart and changes the quantity of Computing and Internet from one to two. The user selects Update shopping cart. The system keeps the product in the cart with quantity two and updates its subtotal consistently with the displayed unit price.


ARQUIVO GERADO QUE DEVE SER REPARADO:
```typescript
import { test, expect } from '@playwright/test';

test.describe('Suite Atualizar Quantidade Carrinho', () => {
  test('should update quantity in cart and keep product with updated subtotal', async ({ page }) => {
    // Etapa 1: Adicionar produto ao carrinho
    await page.goto('https://demowebshop.tricentis.com/computing-and-internet');
    await page.locator("[id=\"add-to-cart-button-13\"]").click();
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/cart');

    // Etapa 2: Acessar carrinho e alterar quantidade
    await page.getByRole("link", { name: "Shopping cart", exact: true }).click();
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/cart');
    await page.locator("[name=\"cart_quantity_13\"]").fill('2');
    await page.locator("[id=\"update_cart_button\"]").click();

    // Verificar se a quantidade foi atualizada e o subtotal está correto
    await expect(page.locator("[name=\"cart_quantity_13\"]")).toHaveValue('2');
    const unitPrice = await page.locator("[class=\"product-unit-price\"]").textContent();
    const expectedSubtotal = parseFloat(unitPrice) * 2;
    const displayedSubtotal = await page.locator("[class=\"order-total-value\"]").textContent();
    expect(parseFloat(displayedSubtotal)).toBe(expectedSubtotal);
  });
});

```

EVIDÊNCIA DA FALHA DE EXECUÇÃO:
Error: expect(page).toHaveURL(expected) failed

Expected: "https://demowebshop.tricentis.com/cart"
Received: "https://demowebshop.tricentis.com/computing-and-internet"
Timeout:  7000ms

Call log:
  - Expect "toHaveURL" with timeout 7000ms
    17 × unexpected value "https://demowebshop.tricentis.com/computing-and-internet"

DIAGNÓSTICO DA REVISÃO:
Usa o produto real, mas espera redirecionamento inexistente e compara o preço unitário ao total do pedido.

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

Especificacao `Suite Atualizar Quantidade Carrinho` em etapas:
1. The user adds Computing and Internet to the cart to prepare the scenario.
2. The user accesses Shopping cart and changes the quantity of Computing and Internet from one to two.
3. The user selects Update shopping cart.
4. The system keeps the product in the cart with quantity two and updates its subtotal consistently with the displayed unit price.

Contexto estruturado por etapa:
Etapa 1 (R1):
- pagina=https://demowebshop.tricentis.com/computing-and-internet
- controle=tag=input, id=add-to-cart-button-13, input_type=button, value=Add to cart, form_action=/computing-and-internet, form_method=POST
- operacao=click
- locator_playwright=page.locator("[id=\"add-to-cart-button-13\"]")
Etapa 2 (R2):
- pagina=https://demowebshop.tricentis.com/computing-and-internet
- controle=tag=a, text=Shopping cart, href=/cart
- operacao=click
- destino=https://demowebshop.tricentis.com/cart
- locator_playwright=page.getByRole("link", { name: "Shopping cart", exact: true })
- pagina_evidencia=https://demowebshop.tricentis.com/cart
- evidencia_pagina=h1:Shopping cart
Etapas sem contexto observado: 3, 4.

Use as informacoes observadas quando forem aplicaveis, sem limitar o teste a elas.
`pagina_evidencia` nao comprova uma transicao ate a pagina.
Sem contexto, siga a especificacao e interaja normalmente com a pagina; nao trate inferencias como fatos observados.


Faça uma única tentativa de reparo. Mantenha todas as verificações exigidas e devolva o arquivo TypeScript completo.