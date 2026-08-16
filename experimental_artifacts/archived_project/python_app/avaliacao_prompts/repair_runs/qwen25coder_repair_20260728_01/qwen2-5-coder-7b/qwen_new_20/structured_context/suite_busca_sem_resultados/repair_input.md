Condição experimental: structured_context

ESPECIFICAÇÃO ORIGINAL:
Searching for a nonexistent product: The user enters a unique term that does not correspond to any product in the Search store field. The user submits the search. The system displays the Search page and informs that no products matched the search criteria.


ARQUIVO GERADO QUE DEVE SER REPARADO:
```typescript
import { test, expect } from '@playwright/test';

test.describe('Suite Busca Sem Resultados', () => {
  test('should display no products matched message when searching for a non-existent term', async ({ page }) => {
    await page.goto('https://demowebshop.tricentis.com/');

    // Etapa 1
    const searchInputLocator = page.locator("[id=\"small-searchterms\"]");
    await searchInputLocator.fill('NonExistentTerm');
    
    const searchButtonLocator = page.getByRole("button", { name: "Search", exact: true });
    await searchButtonLocator.click();

    // Verificação de que a página de busca foi carregada
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/search?q=NonExistentTerm');

    // Verificação de que não há produtos correspondentes
    const noResultsMessage = page.getByText('No products were found that matched your criteria!');
    await expect(noResultsMessage).toBeVisible();
  });
});

```

EVIDÊNCIA DA FALHA DE EXECUÇÃO:
Error: expect(locator).toBeVisible() failed

Locator: getByText('No products were found that matched your criteria!')
Expected: visible
Timeout: 7000ms
Error: element(s) not found

Call log:
  - Expect "toBeVisible" with timeout 7000ms
  - waiting for getByText('No products were found that matched your criteria!')

DIAGNÓSTICO DA REVISÃO:
Busca corretamente um termo inexistente; a mensagem esperada não coincide com a resposta observada.

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

Especificacao `Suite Busca Sem Resultados` em etapas:
1. The user enters a unique term that does not correspond to any product in the Search store field.
2. The user submits the search.
3. The system displays the Search page and informs that no products matched the search criteria.

Contexto estruturado por etapa:
Etapa 1 (R1):
- pagina=https://demowebshop.tricentis.com/
- controle_1=tag=input, id=small-searchterms, name=q, input_type=text, value=Search store, form_action=/search, form_method=GET
- operacao_1=fill
- locator_playwright_1=page.locator("[id=\"small-searchterms\"]")
- controle_2=tag=input, input_type=submit, value=Search, form_action=/search, form_method=GET
- operacao_2=click
- locator_playwright_2=page.getByRole("button", { name: "Search", exact: true })
Etapas sem contexto observado: 2, 3.

Use as informacoes observadas quando forem aplicaveis, sem limitar o teste a elas.
`pagina_evidencia` nao comprova uma transicao ate a pagina.
Sem contexto, siga a especificacao e interaja normalmente com a pagina; nao trate inferencias como fatos observados.


Faça uma única tentativa de reparo. Mantenha todas as verificações exigidas e devolva o arquivo TypeScript completo.