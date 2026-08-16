Condição experimental: structured_context

ESPECIFICAÇÃO ORIGINAL:
Viewing the product history: In a new browser context, the user opens the Fiction product page and then opens the Blue Jeans product page. The user selects Recently viewed products in the Customer service section. The system displays the Recently viewed products page containing both Blue Jeans and Fiction, with Blue Jeans presented before Fiction because it was viewed most recently.


ARQUIVO GERADO QUE DEVE SER REPARADO:
```typescript
import { test, expect } from '@playwright/test';

test.describe('Suite Produtos Visualizados Recentemente', () => {
  test('Viewing the product history and verifying recently viewed products', async ({ page }) => {
    // Etapa 1: Viewing the product history
    await page.goto('https://demowebshop.tricentis.com/blue-jeans');
    expect(page).toHaveURL('https://demowebshop.tricentis.com/blue-jeans');

    // Etapa 2: The user selects Recently viewed products in the Customer service section
    await page.getByText("Recently viewed products", { exact: true }).first().click();
    expect(page).toHaveURL('https://demowebshop.tricentis.com/recentlyviewedproducts');

    // Verifying that Blue Jeans is presented before Fiction because it was viewed most recently
    const productItems = await page.locator('.product-item').allInnerTexts();
    expect(productItems[0]).toContain('Blue Jeans');
    expect(productItems[1]).toContain('Fiction');
  });
});

```

EVIDÊNCIA DA FALHA DE EXECUÇÃO:
Error: expect(received).toContain(expected) // indexOf

Matcher error: received value must not be null nor undefined

Received has value: undefined

DIAGNÓSTICO DA REVISÃO:
Abre apenas Blue Jeans; Fiction depende indevidamente de histórico anterior em contexto novo.

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

Especificacao `Suite Produtos Visualizados Recentemente` em etapas:
1. Viewing the product history: In a new browser context, the user opens the Fiction product page and then opens the Blue Jeans product page.
2. The user selects Recently viewed products in the Customer service section.
3. The system displays the Recently viewed products page containing both Blue Jeans and Fiction, with Blue Jeans presented before Fiction because it was viewed most recently.

Contexto estruturado por etapa:
Etapa 1 (R1):
- pagina_evidencia=https://demowebshop.tricentis.com/blue-jeans
- evidencia_pagina=h1:Blue Jeans
Etapa 2 (R2):
- pagina=https://demowebshop.tricentis.com/blue-jeans
- controle=tag=a, text=Recently viewed products, href=/recentlyviewedproducts
- operacao=click
- destino=https://demowebshop.tricentis.com/recentlyviewedproducts
- locator_playwright=page.getByText("Recently viewed products", { exact: true }).first()
Etapas sem contexto observado: 3.

Use as informacoes observadas quando forem aplicaveis, sem limitar o teste a elas.
`pagina_evidencia` nao comprova uma transicao ate a pagina.
Sem contexto, siga a especificacao e interaja normalmente com a pagina; nao trate inferencias como fatos observados.


Faça uma única tentativa de reparo. Mantenha todas as verificações exigidas e devolva o arquivo TypeScript completo.