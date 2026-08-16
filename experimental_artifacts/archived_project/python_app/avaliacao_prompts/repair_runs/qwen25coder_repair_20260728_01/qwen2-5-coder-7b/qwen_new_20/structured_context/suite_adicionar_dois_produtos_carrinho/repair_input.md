Condição experimental: structured_context

ESPECIFICAÇÃO ORIGINAL:
Adding two different products to the cart: The user adds Computing and Internet to the cart. The user then adds Fiction to the cart. The user accesses Shopping cart. The system displays both Computing and Internet and Fiction as separate cart items, each with its quantity and price.


ARQUIVO GERADO QUE DEVE SER REPARADO:
```typescript
import { test, expect } from '@playwright/test';

test.describe('Suite Adicionar Dois Produtos Carrinho', () => {
  test('Adicionar Computing and Internet ao carrinho', async ({ page }) => {
    await page.goto('https://demowebshop.tricentis.com/computing-and-internet');
    await page.locator("[id=\"add-to-cart-button-13\"]").click();
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/computing-and-internet');
  });

  test('Adicionar Fiction ao carrinho', async ({ page }) => {
    await page.goto('https://demowebshop.tricentis.com/computing-and-internet');
    await page.getByText("Fiction", { exact: true }).first().click();
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/fiction');
  });

  test('Acessar carrinho', async ({ page }) => {
    await page.goto('https://demowebshop.tricentis.com/fiction');
    await page.getByRole("link", { name: "Shopping cart", exact: true }).click();
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/cart');
  });

  test('Verificar itens no carrinho', async ({ page }) => {
    await page.goto('https://demowebshop.tricentis.com/cart');
    await expect(page.getByText("Computing and Internet")).toBeVisible();
    await expect(page.getByText("Fiction")).toBeVisible();
  });
});

```

EVIDÊNCIA DA FALHA DE EXECUÇÃO:
Error: expect(locator).toBeVisible() failed

Locator: getByText('Computing and Internet')
Expected: visible
Timeout: 7000ms
Error: element(s) not found

Call log:
  - Expect "toBeVisible" with timeout 7000ms
  - waiting for getByText('Computing and Internet')

DIAGNÓSTICO DA REVISÃO:
Divide um único fluxo em quatro testes isolados e não adiciona Fiction ao carrinho; o estado não é compartilhado.

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

Especificacao `Suite Adicionar Dois Produtos Carrinho` em etapas:
1. The user adds Computing and Internet to the cart.
2. The user then adds Fiction to the cart.
3. The user accesses Shopping cart.
4. The system displays both Computing and Internet and Fiction as separate cart items, each with its quantity and price.

Contexto estruturado por etapa:
Etapa 1 (R1):
- pagina=https://demowebshop.tricentis.com/computing-and-internet
- controle=tag=input, id=add-to-cart-button-13, input_type=button, value=Add to cart, form_action=/computing-and-internet, form_method=POST
- operacao=click
- locator_playwright=page.locator("[id=\"add-to-cart-button-13\"]")
Etapa 2 (R2):
- pagina=https://demowebshop.tricentis.com/computing-and-internet
- controle=tag=a, text=Fiction, href=/fiction, form_action=/computing-and-internet, form_method=POST
- operacao=click
- destino=https://demowebshop.tricentis.com/fiction
- locator_playwright=page.getByText("Fiction", { exact: true }).first()
- resultado_observado=Fiction
Etapa 3 (R3):
- pagina=https://demowebshop.tricentis.com/fiction
- controle=tag=a, text=Shopping cart, href=/cart
- operacao=click
- destino=https://demowebshop.tricentis.com/cart
- locator_playwright=page.getByRole("link", { name: "Shopping cart", exact: true })
- pagina_evidencia=https://demowebshop.tricentis.com/cart
- evidencia_pagina=h1:Shopping cart
Etapas sem contexto observado: 4.

Use as informacoes observadas quando forem aplicaveis, sem limitar o teste a elas.
`pagina_evidencia` nao comprova uma transicao ate a pagina.
Sem contexto, siga a especificacao e interaja normalmente com a pagina; nao trate inferencias como fatos observados.


Faça uma única tentativa de reparo. Mantenha todas as verificações exigidas e devolva o arquivo TypeScript completo.