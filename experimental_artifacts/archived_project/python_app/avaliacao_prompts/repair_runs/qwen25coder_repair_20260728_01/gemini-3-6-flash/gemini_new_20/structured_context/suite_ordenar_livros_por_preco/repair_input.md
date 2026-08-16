Condição experimental: structured_context

ESPECIFICAÇÃO ORIGINAL:
Sorting books by ascending price: The user accesses the Books category. The user selects Price: Low to High in the Sort by control. The system keeps the Books category visible and displays the products in nondecreasing order according to their current sale prices.


ARQUIVO GERADO QUE DEVE SER REPARADO:
```typescript
import { test, expect } from '@playwright/test';

test.describe('Suite Ordenar Livros Por Preco', () => {
  test('Deve ordenar livros por preco do menor para o maior', async ({ page }) => {
    // Etapa 1: Navegar para a categoria Books
    await page.goto('https://demowebshop.tricentis.com/');
    await page.getByText("Books", { exact: true }).first().click();
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/books');
    await expect(page.getByRole('heading', { name: 'Books', exact: true })).toBeVisible();

    // Etapa 2: Selecionar "Price: Low to High" no controle de ordenacao
    await page.getByLabel('Sort by').selectOption({ label: 'Price: Low to High' });

    // Etapa 3: Verificar que a categoria Books continua visivel e os produtos estao ordenados por preco crescente
    await expect(page.getByRole('heading', { name: 'Books', exact: true })).toBeVisible();

    const priceElements = page.locator('.actual-price');
    await expect(priceElements.first()).toBeVisible();

    const priceTexts = await priceElements.allInnerTexts();
    const prices = priceTexts.map(text => parseFloat(text.replace(/[^0-9.]/g, '')));

    expect(prices.length).toBeGreaterThan(0);
    for (let i = 0; i < prices.length - 1; i++) {
      expect(prices[i]).toBeLessThanOrEqual(prices[i + 1]);
    }
  });
});

```

EVIDÊNCIA DA FALHA DE EXECUÇÃO:
TimeoutError: locator.selectOption: Timeout 10000ms exceeded.
Call log:
  - waiting for getByLabel('Sort by')

DIAGNÓSTICO DA REVISÃO:
Seleciona o combobox e verifica numericamente ordem não decrescente.

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

Especificacao `Suite Ordenar Livros Por Preco` em etapas:
1. The user accesses the Books category.
2. The user selects Price: Low to High in the Sort by control.
3. The system keeps the Books category visible and displays the products in nondecreasing order according to their current sale prices.

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