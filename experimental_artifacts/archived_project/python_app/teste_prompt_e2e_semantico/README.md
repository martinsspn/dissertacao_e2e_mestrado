# Gerador De Prompts E2E Com Contexto Estruturado

O modulo gera um prompt com contexto estruturado para cada especificacao:

- `*.structured_context.prompt.md`, com um contexto compacto extraido do grafo.

O baseline nao e gerado pelo modulo: a especificacao original e enviada diretamente a LLM. O arquivo `generated_prompts/prompt_generation_summary.json` registra a quantidade de etapas, itens de contexto e caracteres do prompt estruturado.

## Fluxo

1. Carrega a especificacao, as paginas e transicoes observadas e o inventario estruturado da interface.
2. Segmenta a especificacao em etapas textuais, sem LLM ou classificacao semantica.
3. Compara cada etapa primeiro com os controles da interface ativa; rotas sao usadas somente como evidencia auxiliar.
4. Associa ate quatro interacoes explicitamente mencionadas ou estruturalmente relacionadas, seus resultados observados e uma evidencia curta de pagina.
5. Deduplica controles equivalentes e escolhe um seletor por prioridade fixa.
6. Produz somente o prompt com contexto estruturado por etapa, sem repetir a especificacao original.

Na segmentacao, titulos em uma linha propria e prefixos descritivos antes da
primeira acao de um paragrafo, como `Cenario: The user searches...`, nao viram
etapas. O texto das acoes permanece inalterado.

Uma etapa pode, por exemplo, receber o campo de busca e o botao `Search` do mesmo
formulario sem que isso implique uma troca de rota. Preenchimentos, marcacoes e
cliques locais mantem a pagina ativa. O cursor so avanca por um link com `href`,
por uma transicao realmente observada ou por uma pagina identificada de forma
literal e univoca por `h1` ou `title`.

Resultados observados iguais a evidencia literal da pagina sao deduplicados. O
campo `destino` e reservado a links com `href`; `form_action` descreve o
formulario extraido e pode relacionar seus controles, mas nao e tratado como
navegacao observada. A selecao nao calcula scores, pesos nem cobertura da
especificacao.

Para controles `radio`, mencionar apenas o grupo, como `Gender option`, nao
autoriza escolher arbitrariamente uma opcao. O contexto so inclui o `radio`
quando seu rotulo ou valor, como `Female`, aparece explicitamente na etapa.

O prompt apresenta o contexto como apoio parcial, nao como roteiro completo. A
LLM deve combina-lo com a especificacao e com seu conhecimento de navegacao web
para localizar os elementos visiveis e implementar inclusive as etapas sem
contexto, sem transformar seletores ou rotas nao observados em evidencias do
grafo. A resposta deve usar um unico bloco de codigo `typescript`, pois a
renderizacao como texto Markdown pode transformar URLs e remover barras
invertidas. O conteudo interno desse bloco e um arquivo Playwright `.spec.ts`
completo, executavel por `npx playwright test` sem edicao manual. `page.goto` e
`toHaveURL` usam URLs literais, sem regex ou links Markdown. Locators usados em
acoes devem resolver um unico elemento no modo estrito do Playwright.

Seletores recomendados aparecem somente como `locator_playwright=...`, contendo
uma expressao TypeScript completa, por exemplo
`page.getByRole("button", { name: "Search", exact: true })`. A LLM deve chamar a
acao diretamente nessa expressao (`.click()`, `.fill()`, `.check()` etc.).
Notacoes internas como `role_name:`, `label:`, `id:`, `tag=` e `text:` nao sao
locators Playwright e nao sao publicadas como seletores copiaveis.

O perfil de origem usa `SHALLOW_FIRST`, ordem nao aleatoria e executa somente
links navegacionais. Controles nao acionados tambem podem aparecer no prompt
porque sao extraidos do HTML; resultados observados, por outro lado, existem
somente para transicoes realmente executadas. As regioes dinamicas
`slider-wrapper` e `block-recently-viewed-products` sao normalizadas na
comparacao de estados. Campos de senha sao disponibilizados sem valor.

O exportador consolida por URL os DOMs reconhecidos como estados distintos.
Consequentemente, controles de estados AJAX diferentes na mesma URL podem ser
unidos no inventario, sem preservar a ordem em que ficaram disponiveis. Essa
limitacao deve ser considerada ao interpretar o contexto produzido.

## Execucao

```bash
python3 -m teste_prompt_e2e_semantico --specs-dir ./specs --output-dir ./generated_prompts
```

Na raiz do repositorio:

```bash
docker compose run --rm prompt_e2e
```

## Configuracao

- `PROMPT_E2E_BASE_URL`
- `PROMPT_E2E_SPECS_DIR`
- `PROMPT_E2E_OUTPUT_DIR`
- `NEO4J_URI`, `NEO4J_USER`, `NEO4J_PASSWORD`

As especificacoes do experimento devem usar o idioma predominante da interface, pois o modulo nao traduz termos nem possui dicionario especifico de dominio.

## Suite de referencia

Os arquivos `specs/suite_*.txt` formam uma suite curada de 12 cenarios do Demo Web Shop, reescritos em linguagem natural a partir de comportamentos encontrados em projetos publicos. A origem, os criterios de selecao e as dependencias de execucao estao documentados em [`docs/suite_referencia_demowebshop.md`](../../docs/suite_referencia_demowebshop.md).

O gerador pode processar todos os arquivos em uma execucao, mas produz um prompt separado para cada cenario. Na etapa experimental, use exatamente o mesmo arquivo de especificacao no baseline e na geracao com contexto estruturado.

## Testes Unitarios

```bash
python3 -m unittest discover -s tests -v
```
