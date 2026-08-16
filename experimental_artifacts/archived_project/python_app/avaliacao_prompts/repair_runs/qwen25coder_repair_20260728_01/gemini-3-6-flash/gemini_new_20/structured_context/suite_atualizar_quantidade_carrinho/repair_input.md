Condição experimental: structured_context

ESPECIFICAÇÃO ORIGINAL:
Updating a product quantity in the cart: The user adds Computing and Internet to the cart to prepare the scenario. The user accesses Shopping cart and changes the quantity of Computing and Internet from one to two. The user selects Update shopping cart. The system keeps the product in the cart with quantity two and updates its subtotal consistently with the displayed unit price.


ARQUIVO GERADO QUE DEVE SER REPARADO:
```typescript
import { test, expect } from '@playwright/test';

test.describe('Suite Atualizar Quantidade Carrinho', () => {
  test('Atualizar quantidade do produto Computing and Internet no carrinho', async ({ page }) => {
    // Inicia na pagina principal
    await page.goto('https://demowebshop.tricentis.com/');

    // Etapa 1: Navegar ate o produto Computing and Internet e adicionar ao carrinho
    await page.goto('https://demowebshop.tricentis.com/computing-and-internet');
    await page.locator("[id=\"add-to-cart-button-13\"]").click();

    // Etapa 2: Acessar o carrinho de compras
    await page.getByRole("link", { name: "Shopping cart", exact: true }).click();
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/cart');

    // Alterar a quantidade do produto de 1 para 2
    const qtyInput = page.locator('input.qty-input').first();
    await qtyInput.fill('2');

    // Etapa 3: Selecionar Atualizar carrinho de compras
    await page.getByRole('button', { name: 'Update shopping cart' }).click();

    // Etapa 4: Validar a permanencia do produto, quantidade e consistencia do subtotal
    await expect(qtyInput).toHaveValue('2');
    await expect(page.locator('.shopping-cart-page')).toContainText('Computing and Internet');

    const unitPriceText = await page.locator('.product-unit-price').first().innerText();
    const subtotalText = await page.locator('.product-subtotal').first().innerText();

    const unitPrice = parseFloat(unitPriceText.replace(/[^0-9.]/g, ''));
    const subtotal = parseFloat(subtotalText.replace(/[^0-9.]/g, ''));

    expect(subtotal).toBeCloseTo(unitPrice * 2, 2);
  });
});

```

EVIDÊNCIA DA FALHA DE EXECUÇÃO:
TimeoutError: locator.fill: Timeout 10000ms exceeded.
Call log:
  - waiting for locator('input.qty-input').first()

DIAGNÓSTICO DA REVISÃO:
Atualiza quantidade e compara subtotal da linha com duas vezes o preço unitário.

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