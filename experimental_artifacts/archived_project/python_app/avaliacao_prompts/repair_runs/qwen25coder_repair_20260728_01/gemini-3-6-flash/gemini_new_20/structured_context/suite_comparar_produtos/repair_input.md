Condição experimental: structured_context

ESPECIFICAÇÃO ORIGINAL:
Comparing two products: The user opens the Computing and Internet product page and selects Add to compare list. The user opens the Fiction product page and selects Add to compare list. The system displays the Compare products page containing both Computing and Internet and Fiction, with their product information arranged for comparison. At the end, the user clears the comparison list.


ARQUIVO GERADO QUE DEVE SER REPARADO:
```typescript
import { test, expect } from '@playwright/test';

test.describe('Suite Comparar Produtos', () => {
  test('Deve adicionar produtos a lista de comparacao e depois limpar a lista', async ({ page }) => {
    // Inicia na pagina principal
    await page.goto('https://demowebshop.tricentis.com/');

    // Etapa 1: Acessa a pagina do produto Computing and Internet e adiciona a lista de comparacao
    await page.goto('https://demowebshop.tricentis.com/computing-and-internet');
    await expect(page.getByRole('heading', { name: 'Computing and Internet' })).toBeVisible();
    await page.getByRole('button', { name: 'Add to compare list' }).click();

    // Etapa 2: Acessa a pagina do produto Fiction e adiciona a lista de comparacao
    await page.getByText("Fiction", { exact: true }).first().click();
    await expect(page.getByRole('heading', { name: 'Fiction' })).toBeVisible();
    await page.getByRole('button', { name: 'Add to compare list' }).click();

    // Etapa 3: Exibe a pagina de comparacao contendo Computing and Internet e Fiction
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/compareproducts');
    await expect(page.getByRole('heading', { name: 'Compare products' })).toBeVisible();
    await expect(page.getByRole('link', { name: 'Computing and Internet' }).last()).toBeVisible();
    await expect(page.getByRole('link', { name: 'Fiction' }).last()).toBeVisible();

    // Etapa 4: Limpa a lista de comparacao
    await page.getByRole('button', { name: 'Clear list' }).click();
    await expect(page.getByText('You have no items to compare.')).toBeVisible();
  });
});

```

EVIDÊNCIA DA FALHA DE EXECUÇÃO:
TimeoutError: locator.click: Timeout 10000ms exceeded.
Call log:
  - waiting for getByText('Fiction', { exact: true }).first()

DIAGNÓSTICO DA REVISÃO:
Adiciona os dois produtos no mesmo fluxo, valida-os e limpa a lista.

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

Especificacao `Suite Comparar Produtos` em etapas:
1. The user opens the Computing and Internet product page and selects Add to compare list.
2. The user opens the Fiction product page and selects Add to compare list.
3. The system displays the Compare products page containing both Computing and Internet and Fiction, with their product information arranged for comparison.
4. At the end, the user clears the comparison list.

Contexto estruturado por etapa:
Etapa 1 (R1):
- pagina_evidencia=https://demowebshop.tricentis.com/computing-and-internet
- evidencia_pagina=h1:Computing and Internet
Etapa 2 (R2):
- pagina=https://demowebshop.tricentis.com/computing-and-internet
- controle=tag=a, text=Fiction, href=/fiction, form_action=/computing-and-internet, form_method=POST
- operacao=click
- destino=https://demowebshop.tricentis.com/fiction
- locator_playwright=page.getByText("Fiction", { exact: true }).first()
- pagina_evidencia=https://demowebshop.tricentis.com/fiction
- evidencia_pagina=h1:Fiction
Etapa 3 (R3):
- pagina_evidencia=https://demowebshop.tricentis.com/fiction
- evidencia_pagina=h1:Fiction
Etapas sem contexto observado: 4.

Use as informacoes observadas quando forem aplicaveis, sem limitar o teste a elas.
`pagina_evidencia` nao comprova uma transicao ate a pagina.
Sem contexto, siga a especificacao e interaja normalmente com a pagina; nao trate inferencias como fatos observados.


Faça uma única tentativa de reparo. Mantenha todas as verificações exigidas e devolva o arquivo TypeScript completo.