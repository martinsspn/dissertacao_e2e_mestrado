Condição experimental: structured_context

ESPECIFICAÇÃO ORIGINAL:
Configuration of a computer before purchase: The user accesses Computers and opens the Desktops category. The user opens a desktop that allows choosing its configuration. The user selects the options for a Fast processor, 4 GB memory, 400 GB disk, and Office Suite software. The user selects Add to cart. The system informs that the product has been added to the cart. The user accesses Shopping cart. The system displays the configured desktop among the items in the cart.


ARQUIVO GERADO QUE DEVE SER REPARADO:
```typescript
import { test, expect } from '@playwright/test';

test.describe('Suite Configurar Desktop', () => {
  test('should configure and add desktop to cart', async ({ page }) => {
    // Step 1: Access Computers and open the Desktops category
    await page.goto('https://demowebshop.tricentis.com/');
    await page.getByText("Computers", { exact: true }).first().click();
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/computers');
    
    // Step 2: Open a desktop that allows choosing its configuration
    await page.getByText("Desktops", { exact: true }).first().click();
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/desktops');

    // Step 3: Select options for Fast processor, 4 GB memory, 400 GB disk, and Office Suite software
    await page.getByText("Fast", { exact: true }).click();
    await page.getByText("4GB [+$25.00]", { exact: true }).click();
    await page.getByText("400GB [+$10.00]", { exact: true }).click();
    await page.getByText("Microsoft Office Suite [+$79.00]", { exact: true }).click();

    // Step 4: Select Add to cart
    await page.getByRole('button', { name: 'Add to cart', exact: true }).click();

    // Step 5: System informs that the product has been added to the cart
    await expect(page.locator('.content')).toContainText('The product has been added to your shopping cart');

    // Step 6: Access Shopping cart
    await page.getByRole("link", { name: "Shopping cart", exact: true }).click();
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/cart');

    // Step 7: System displays the configured desktop among the items in the cart
    await expect(page.locator('.cart-item-name')).toContainText('Desktop');
  });
});

```

EVIDÊNCIA DA FALHA DE EXECUÇÃO:
TimeoutError: locator.click: Timeout 10000ms exceeded.
Call log:
  - waiting for getByText('Fast', { exact: true })

DIAGNÓSTICO DA REVISÃO:
Navega às categorias, mas não abre um produto antes de procurar as opções de configuração.

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

Especificacao `Suite Configurar Desktop` em etapas:
1. The user accesses Computers and opens the Desktops category.
2. The user opens a desktop that allows choosing its configuration.
3. The user selects the options for a Fast processor, 4 GB memory, 400 GB disk, and Office Suite software.
4. The user selects Add to cart.
5. The system informs that the product has been added to the cart.
6. The user accesses Shopping cart.
7. The system displays the configured desktop among the items in the cart.

Contexto estruturado por etapa:
Etapa 1 (R1):
- pagina=https://demowebshop.tricentis.com/
- controle_1=tag=a, text=Computers, href=/computers
- operacao_1=click
- destino_1=https://demowebshop.tricentis.com/computers
- locator_playwright_1=page.getByText("Computers", { exact: true }).first()
- resultado_observado_1=Computers
- controle_2=tag=a, text=Desktops, href=/desktops
- operacao_2=click
- destino_2=https://demowebshop.tricentis.com/desktops
- locator_playwright_2=page.getByText("Desktops", { exact: true }).first()
- pagina_evidencia=https://demowebshop.tricentis.com/desktops
- evidencia_pagina=h1:Desktops
Etapa 6 (R6):
- pagina=https://demowebshop.tricentis.com/desktops
- controle=tag=a, text=Shopping cart, href=/cart
- operacao=click
- destino=https://demowebshop.tricentis.com/cart
- locator_playwright=page.getByRole("link", { name: "Shopping cart", exact: true })
- pagina_evidencia=https://demowebshop.tricentis.com/cart
- evidencia_pagina=h1:Shopping cart
Etapas sem contexto observado: 2, 3, 4, 5, 7.

Use as informacoes observadas quando forem aplicaveis, sem limitar o teste a elas.
`pagina_evidencia` nao comprova uma transicao ate a pagina.
Sem contexto, siga a especificacao e interaja normalmente com a pagina; nao trate inferencias como fatos observados.


Faça uma única tentativa de reparo. Mantenha todas as verificações exigidas e devolva o arquivo TypeScript completo.