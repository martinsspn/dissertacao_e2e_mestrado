Condição experimental: structured_context

ESPECIFICAÇÃO ORIGINAL:
Adding a product to the cart: The user searches for the product Blue Jeans in the Search store field. The user opens the product Blue Jeans in the search results. The user selects Add to cart on the product page. The system informs that the product has been added to the cart. The user accesses Shopping cart. The system displays Blue Jeans among the items in the cart.


ARQUIVO GERADO QUE DEVE SER REPARADO:
```typescript
import { test, expect } from '@playwright/test';

test.describe('Suite Adicionar Carrinho', () => {
  test('Adicionar Blue Jeans ao carrinho', async ({ page }) => {
    // Etapa 1: Pesquisa por Blue Jeans
    await page.goto('https://demowebshop.tricentis.com/');
    await page.locator("[id=\"small-searchterms\"]").fill('Blue Jeans');
    await page.getByRole("button", { name: "Search", exact: true }).click();

    // Etapa 2: Abre a página do produto Blue Jeans
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/blue-jeans');

    // Etapa 3: Adiciona o produto ao carrinho
    await page.locator("[id=\"add-to-cart-button-36\"]").click();

    // Verifica a mensagem de sucesso
    await expect(page.getByText('The product has been added to your shopping cart')).toBeVisible();

    // Etapa 5: Acessa o carrinho
    await page.getByRole("link", { name: "Shopping cart", exact: true }).click();
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/cart');

    // Verifica que Blue Jeans está no carrinho
    await expect(page.getByText('Blue Jeans')).toBeVisible();
  });
});

```

EVIDÊNCIA DA FALHA DE EXECUÇÃO:
Error: expect(page).toHaveURL(expected) failed

Expected: "https://demowebshop.tricentis.com/blue-jeans"
Received: "https://demowebshop.tricentis.com/search?q=Blue+Jeans"
Timeout:  7000ms

Call log:
  - Expect "toHaveURL" with timeout 7000ms
    17 × unexpected value "https://demowebshop.tricentis.com/search?q=Blue+Jeans"

DIAGNÓSTICO DA REVISÃO:
Busca com controles corretos, mas espera redirecionamento direto ao produto e não clica no resultado.

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

Especificacao `Suite Adicionar Carrinho` em etapas:
1. The user searches for the product Blue Jeans in the Search store field.
2. The user opens the product Blue Jeans in the search results.
3. The user selects Add to cart on the product page.
4. The system informs that the product has been added to the cart.
5. The user accesses Shopping cart.
6. The system displays Blue Jeans among the items in the cart.

Contexto estruturado por etapa:
Etapa 1 (R1):
- pagina=https://demowebshop.tricentis.com/
- controle_1=tag=input, id=small-searchterms, name=q, input_type=text, value=Search store, form_action=/search, form_method=GET
- operacao_1=fill
- locator_playwright_1=page.locator("[id=\"small-searchterms\"]")
- controle_2=tag=input, input_type=submit, value=Search, form_action=/search, form_method=GET
- operacao_2=click
- locator_playwright_2=page.getByRole("button", { name: "Search", exact: true })
Etapa 2 (R2):
- pagina_evidencia=https://demowebshop.tricentis.com/blue-jeans
- evidencia_pagina=h1:Blue Jeans
Etapa 3 (R3):
- pagina=https://demowebshop.tricentis.com/blue-jeans
- controle=tag=input, id=add-to-cart-button-36, input_type=button, value=Add to cart, form_action=/blue-jeans, form_method=POST
- operacao=click
- locator_playwright=page.locator("[id=\"add-to-cart-button-36\"]")
Etapa 5 (R5):
- pagina=https://demowebshop.tricentis.com/blue-jeans
- controle=tag=a, text=Shopping cart, href=/cart
- operacao=click
- destino=https://demowebshop.tricentis.com/cart
- locator_playwright=page.getByRole("link", { name: "Shopping cart", exact: true })
- pagina_evidencia=https://demowebshop.tricentis.com/cart
- evidencia_pagina=h1:Shopping cart
Etapas sem contexto observado: 4, 6.

Use as informacoes observadas quando forem aplicaveis, sem limitar o teste a elas.
`pagina_evidencia` nao comprova uma transicao ate a pagina.
Sem contexto, siga a especificacao e interaja normalmente com a pagina; nao trate inferencias como fatos observados.


Faça uma única tentativa de reparo. Mantenha todas as verificações exigidas e devolva o arquivo TypeScript completo.