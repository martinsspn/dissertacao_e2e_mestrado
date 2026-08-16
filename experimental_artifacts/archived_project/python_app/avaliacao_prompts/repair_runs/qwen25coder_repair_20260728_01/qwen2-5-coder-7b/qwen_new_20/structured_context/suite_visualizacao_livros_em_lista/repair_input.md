Condição experimental: structured_context

ESPECIFICAÇÃO ORIGINAL:
Changing the book catalog view: The user accesses the Books category, which initially presents the Grid view. The user selects List in the View as control. The system keeps the Books category visible and presents its products using the list view.


ARQUIVO GERADO QUE DEVE SER REPARADO:
```typescript
import { test, expect } from '@playwright/test';

test.describe('Suite Visualizacao Livros Em Lista', () => {
  test('The user accesses the Books category and selects List view', async ({ page }) => {
    // Etapa 1: Acessa a categoria de Livros
    await page.goto('https://demowebshop.tricentis.com/');
    await page.getByText("Books", { exact: true }).first().click();
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/books');

    // Etapa 3: Seleciona a visualização em Lista
    const listViewButton = page.locator('button', { hasText: 'List' });
    if (await listViewButton.isVisible()) {
      await listViewButton.click();
    }

    // Verifica se a página ainda é a de Livros e se está em modo de lista
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/books');
    const productItems = page.locator('.product-item');
    await expect(productItems).toBeVisible();
  });
});

```

EVIDÊNCIA DA FALHA DE EXECUÇÃO:
Error: expect(locator).toBeVisible() failed

Locator: locator('.product-item')
Expected: visible
Error: strict mode violation: locator('.product-item') resolved to 6 elements:
    1) <div data-productid="13" class="product-item">…</div> aka locator('.product-item').first()
    2) <div data-productid="79" class="product-item">…</div> aka locator('div:nth-child(2) > .product-item')
    3) <div data-productid="45" class="product-item">…</div> aka locator('div:nth-child(3) > .product-item')
    4) <div data-productid="78" class="product-item">…</div> aka locator('div:nth-child(4) > .product-item')
    5) <div data-productid="22" class="product-item">…</div> aka locator('div:nth-child(5) > .product-item')
    6) <div data-productid="27" class="product-item">…</div> aka locator('div:nth-child(6) > .product-item')

Call log:
  - Expect "toBeVisible" with timeout 7000ms
  - waiting for locator('.product-item')

DIAGNÓSTICO DA REVISÃO:
Procura um botão opcional em vez do controle View as e nunca comprova a visualização em lista.

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

Especificacao `Suite Visualizacao Livros Em Lista` em etapas:
1. The user accesses the Books category, which initially presents the Grid view.
2. The user selects List in the View as control.
3. The system keeps the Books category visible and presents its products using the list view.

Contexto estruturado por etapa:
Etapa 1 (R1):
- pagina=https://demowebshop.tricentis.com/
- controle=tag=a, text=Books, href=/books
- operacao=click
- destino=https://demowebshop.tricentis.com/books
- locator_playwright=page.getByText("Books", { exact: true }).first()
- pagina_evidencia=https://demowebshop.tricentis.com/books
- evidencia_pagina=h1:Books
Etapa 3 (R3):
- pagina_evidencia=https://demowebshop.tricentis.com/books
- evidencia_pagina=h1:Books
Etapas sem contexto observado: 2.

Use as informacoes observadas quando forem aplicaveis, sem limitar o teste a elas.
`pagina_evidencia` nao comprova uma transicao ate a pagina.
Sem contexto, siga a especificacao e interaja normalmente com a pagina; nao trate inferencias como fatos observados.


Faça uma única tentativa de reparo. Mantenha todas as verificações exigidas e devolva o arquivo TypeScript completo.