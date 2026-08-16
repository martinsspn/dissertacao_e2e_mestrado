Condição experimental: structured_context

ESPECIFICAÇÃO ORIGINAL:
Opening the institutional information page: The user accesses the Demo Web Shop home page. In the Information section of the footer, the user selects About us. The system displays the About us page and its corresponding heading.


ARQUIVO GERADO QUE DEVE SER REPARADO:
```typescript
import { test, expect } from '@playwright/test';

test.describe('Suite Navegar Sobre Nos', () => {
  test('Deve navegar para a pagina About us a partir do rodape', async ({ page }) => {
    // Etapa 1: O usuario acessa a pagina inicial do Demo Web Shop.
    await page.goto('https://demowebshop.tricentis.com/');

    // Etapa 2: Na secao Information do rodape, o usuario seleciona About us.
    await page.getByText("About us", { exact: true }).first().click();

    // Etapa 3: O sistema exibe a pagina About us e seu titulo correspondente.
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/about-us');
    await expect(page.getByRole('heading', { name: 'About us', exact: true })).toBeVisible();
  });
});

```

EVIDÊNCIA DA FALHA DE EXECUÇÃO:
Error: expect(locator).toBeVisible() failed

Locator: getByRole('heading', { name: 'About us', exact: true })
Expected: visible
Timeout: 7000ms
Error: element(s) not found

Call log:
  - Expect "toBeVisible" with timeout 7000ms
  - waiting for getByRole('heading', { name: 'About us', exact: true })

DIAGNÓSTICO DA REVISÃO:
Navega e valida URL e heading; não restringe o link ao rodapé, mas aciona o alvo correto.

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

Especificacao `Suite Navegar Sobre Nos` em etapas:
1. The user accesses the Demo Web Shop home page.
2. In the Information section of the footer, the user selects About us.
3. The system displays the About us page and its corresponding heading.

Contexto estruturado por etapa:
Etapa 1 (R1):
- pagina_evidencia=https://demowebshop.tricentis.com/
- evidencia_pagina=title:Demo Web Shop
Etapa 2 (R2):
- pagina=https://demowebshop.tricentis.com/
- controle=tag=a, text=About us, href=/about-us
- operacao=click
- destino=https://demowebshop.tricentis.com/about-us
- locator_playwright=page.getByText("About us", { exact: true }).first()
Etapas sem contexto observado: 3.

Use as informacoes observadas quando forem aplicaveis, sem limitar o teste a elas.
`pagina_evidencia` nao comprova uma transicao ate a pagina.
Sem contexto, siga a especificacao e interaja normalmente com a pagina; nao trate inferencias como fatos observados.


Faça uma única tentativa de reparo. Mantenha todas as verificações exigidas e devolva o arquivo TypeScript completo.