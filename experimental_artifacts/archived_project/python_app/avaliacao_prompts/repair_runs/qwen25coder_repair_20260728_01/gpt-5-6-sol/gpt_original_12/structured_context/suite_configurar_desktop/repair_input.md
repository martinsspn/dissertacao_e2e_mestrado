Condição experimental: structured_context

ESPECIFICAÇÃO ORIGINAL:
Configuration of a computer before purchase: The user accesses Computers and opens the Desktops category. The user opens a desktop that allows choosing its configuration. The user selects the options for a Fast processor, 4 GB memory, 400 GB disk, and Office Suite software. The user selects Add to cart. The system informs that the product has been added to the cart. The user accesses Shopping cart. The system displays the configured desktop among the items in the cart.


ARQUIVO GERADO QUE DEVE SER REPARADO:
```typescript
import { test, expect } from '@playwright/test';

test.describe('Suite Configurar Desktop', () => {
  test('configura um desktop e o adiciona ao carrinho', async ({ page }) => {
    await page.goto('https://demowebshop.tricentis.com/');

    await page
      .locator('.top-menu')
      .getByRole('link', { name: 'Computers', exact: true })
      .click();

    await expect(page).toHaveURL(
      'https://demowebshop.tricentis.com/computers',
    );
    await expect(
      page.getByRole('heading', { name: 'Computers', exact: true }),
    ).toBeVisible();

    await page
      .locator('.category-grid')
      .getByRole('link', { name: 'Desktops', exact: true })
      .click();

    await expect(page).toHaveURL(
      'https://demowebshop.tricentis.com/desktops',
    );
    await expect(
      page.getByRole('heading', { name: 'Desktops', exact: true }),
    ).toBeVisible();

    const desktopName = 'Build your own cheap computer';

    const configurableDesktop = page
      .locator('.product-item')
      .filter({
        has: page.getByRole('link', {
          name: desktopName,
          exact: true,
        }),
      });

    await expect(configurableDesktop).toBeVisible();

    await configurableDesktop
      .getByRole('link', {
        name: desktopName,
        exact: true,
      })
      .click();

    await expect(page).toHaveURL(
      'https://demowebshop.tricentis.com/build-your-cheap-own-computer',
    );
    await expect(
      page.getByRole('heading', {
        name: desktopName,
        exact: true,
      }),
    ).toBeVisible();

    const fastProcessor = page.getByLabel('Fast [+100.00]', {
      exact: true,
    });
    const fourGbMemory = page.getByLabel('4 GB [+20.00]', {
      exact: true,
    });
    const fourHundredGbDisk = page.getByLabel('400 GB [+100.00]', {
      exact: true,
    });
    const officeSuite = page.getByLabel('Office Suite [+100.00]', {
      exact: true,
    });

    await fastProcessor.check();
    await fourGbMemory.check();
    await fourHundredGbDisk.check();
    await officeSuite.check();

    await expect(fastProcessor).toBeChecked();
    await expect(fourGbMemory).toBeChecked();
    await expect(fourHundredGbDisk).toBeChecked();
    await expect(officeSuite).toBeChecked();

    await page
      .getByRole('button', { name: 'Add to cart', exact: true })
      .click();

    const notification = page.locator('#bar-notification');

    await expect(notification).toBeVisible();
    await expect(notification).toContainText(
      'The product has been added to your shopping cart',
    );

    await page
      .getByRole('link', { name: 'Shopping cart', exact: true })
      .click();

    await expect(page).toHaveURL(
      'https://demowebshop.tricentis.com/cart',
    );
    await expect(
      page.getByRole('heading', {
        name: 'Shopping cart',
        exact: true,
      }),
    ).toBeVisible();

    const configuredDesktopCartItem = page
      .locator('tr.cart-item-row')
      .filter({
        has: page.getByRole('link', {
          name: desktopName,
          exact: true,
        }),
      });

    await expect(configuredDesktopCartItem).toBeVisible();
    await expect(
      configuredDesktopCartItem.getByRole('link', {
        name: desktopName,
        exact: true,
      }),
    ).toBeVisible();

    const configuration = configuredDesktopCartItem.locator('.attributes');

    await expect(configuration).toContainText('Fast');
    await expect(configuration).toContainText('4 GB');
    await expect(configuration).toContainText('400 GB');
    await expect(configuration).toContainText('Office Suite');
  });
});

```

EVIDÊNCIA DA FALHA DE EXECUÇÃO:
Falha registrada sem mensagem detalhada.

DIAGNÓSTICO DA REVISÃO:
Fluxo e opções completos; o escopo category-grid não correspondeu ao DOM observado.

PROMPT ESTRUTURADO ORIGINAL DESTA CONDIÇÃO:
# Geracao de teste E2E Playwright

Gere um teste TypeScript Playwright fiel a especificacao.

Regras:
- Retorne um unico bloco de codigo `typescript`, sem texto fora dele; o conteudo interno deve ser um arquivo Playwright `.spec.ts` completo e executavel por `npx playwright test`.
- Importe `test` e `expect` de `@playwright/test`.
- Inicie com `await page.goto('https://demowebshop.tricentis.com/')`; use URLs literais tambem em `toHaveURL`, sem regex ou links Markdown.
- Nao derive rotas do texto de links, produtos ou titulos. Use `toHaveURL` somente quando a URL exata estiver na base ou no contexto; sem URL observada, confirme a pagina por elementos visiveis.
- Use locators Playwright legiveis e unicos no modo estrito; evite XPath, indices e `waitForTimeout`.
- Quando o contexto fornecer `id`, `data-testid` ou um locator Playwright exato, preserve esse seletor; nao o substitua por um locator generico baseado apenas em papel e nome.
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
- seletor_1=text:Computers
- resultado_observado_1=Computers
- controle_2=tag=a, text=Desktops, href=/desktops
- operacao_2=click
- destino_2=https://demowebshop.tricentis.com/desktops
- seletor_2=text:Desktops
- pagina_evidencia=https://demowebshop.tricentis.com/desktops
- evidencia_pagina=h1:Desktops
Etapa 6 (R6):
- pagina=https://demowebshop.tricentis.com/desktops
- controle=tag=a, text=Shopping cart, href=/cart
- operacao=click
- destino=https://demowebshop.tricentis.com/cart
- seletor=page.getByRole('link', { name: 'Shopping cart', exact: true })
- pagina_evidencia=https://demowebshop.tricentis.com/cart
- evidencia_pagina=h1:Shopping cart
Etapas sem contexto observado: 2, 3, 4, 5, 7.

Use as informacoes observadas quando forem aplicaveis, sem limitar o teste a elas.
`pagina_evidencia` nao comprova uma transicao ate a pagina.
Sem contexto, siga a especificacao e interaja normalmente com a pagina; nao trate inferencias como fatos observados.


Faça uma única tentativa de reparo. Mantenha todas as verificações exigidas e devolva o arquivo TypeScript completo.