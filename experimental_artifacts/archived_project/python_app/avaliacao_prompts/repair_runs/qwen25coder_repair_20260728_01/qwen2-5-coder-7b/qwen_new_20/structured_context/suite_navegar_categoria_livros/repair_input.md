Condição experimental: structured_context

ESPECIFICAÇÃO ORIGINAL:
Browsing the Books category: The user accesses the Demo Web Shop home page. The user selects Books in the main category menu. The system displays the Books category page, its breadcrumb, and the available book products, including Computing and Internet, Fiction, and Health Book.


ARQUIVO GERADO QUE DEVE SER REPARADO:
```typescript
import { test, expect } from '@playwright/test';

test.describe('Suite Navegar Categoria Livros', () => {
  test('The user accesses the Demo Web Shop home page and navigates to the Books category', async ({ page }) => {
    // Etapa 1: Acessa a página inicial do Demo Web Shop
    await page.goto('https://demowebshop.tricentis.com/');
    expect(page).toHaveTitle('Demo Web Shop');

    // Etapa 2: Seleciona a categoria "Books" no menu principal
    const booksLink = page.getByText("Books", { exact: true }).first();
    await booksLink.click();

    // Verifica se foi redirecionado para a página de categorias de livros
    expect(page).toHaveURL('https://demowebshop.tricentis.com/books');
    expect(page.locator('h1')).toHaveText('Books');

    // Etapa 3: Confirma que os subcategorias estão disponíveis
    const subcategories = ['Computing and Internet', 'Fiction', 'Health Book'];
    for (const category of subcategories) {
      expect(page.getByText(category)).toBeVisible();
    }
  });
});

```

EVIDÊNCIA DA FALHA DE EXECUÇÃO:
Error: expect(page).toHaveURL(expected) failed

Expected: "https://demowebshop.tricentis.com/books"
Received: ""

Call log:
  - Expect "toHaveURL" with timeout 7000ms

DIAGNÓSTICO DA REVISÃO:
Fluxo e produtos corretos, porém todas as expectativas assíncronas estão sem await.

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

Especificacao `Suite Navegar Categoria Livros` em etapas:
1. The user accesses the Demo Web Shop home page.
2. The user selects Books in the main category menu.
3. The system displays the Books category page, its breadcrumb, and the available book products, including Computing and Internet, Fiction, and Health Book.

Contexto estruturado por etapa:
Etapa 1 (R1):
- pagina_evidencia=https://demowebshop.tricentis.com/
- evidencia_pagina=title:Demo Web Shop
Etapa 2 (R2):
- pagina=https://demowebshop.tricentis.com/
- controle=tag=a, text=Books, href=/books
- operacao=click
- destino=https://demowebshop.tricentis.com/books
- locator_playwright=page.getByText("Books", { exact: true }).first()
- resultado_observado=Books
Etapa 3 (R3):
- pagina_evidencia=https://demowebshop.tricentis.com/books
- evidencia_pagina=h1:Books

Use as informacoes observadas quando forem aplicaveis, sem limitar o teste a elas.
`pagina_evidencia` nao comprova uma transicao ate a pagina.
Sem contexto, siga a especificacao e interaja normalmente com a pagina; nao trate inferencias como fatos observados.


Faça uma única tentativa de reparo. Mantenha todas as verificações exigidas e devolva o arquivo TypeScript completo.