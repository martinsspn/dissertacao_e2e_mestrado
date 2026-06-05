# Specification Coverage

## Objetivo

`specification_coverage` e a camada do gerador de prompts que estima o quanto a especificacao em linguagem natural esta sustentada pelo grafo navegacional extraido da aplicacao.

Ela existe para evitar que o prompt apenas entregue paginas e transicoes "parecidas" com a especificacao. O objetivo e explicitar, antes da geracao do teste, quais partes do fluxo possuem evidencia no grafo e quais partes exigiriam invencao por parte da LLM.

Em termos da pesquisa, essa camada ajuda a separar tres situacoes:

- o grafo cobre o comportamento pedido;
- o grafo cobre apenas parte do comportamento;
- o grafo nao possui evidencias suficientes para aquele fluxo.

Isso transforma uma limitacao pratica do crawler em uma informacao auditavel e mensuravel.

## Onde Entra No Pipeline

O fluxo atual do gerador e:

```text
especificacao em LN
  -> normalizacao textual
  -> ranking de paginas relevantes
  -> ranking de transicoes relevantes
  -> ranking de caminhos candidatos
  -> specification_coverage
  -> montagem do prompt estruturado
```

A implementacao principal esta em:

```text
python_app/teste_prompt_e2e_semantico/teste_prompt_e2e_semantico/application/spec_coverage.py
```

Os modelos ficam em:

```text
python_app/teste_prompt_e2e_semantico/teste_prompt_e2e_semantico/domain/models.py
```

## Como Funciona

### 1. Extracao De Requisitos

A especificacao e quebrada em requisitos menores.

Exemplo:

```text
O usuario deve acessar a categoria Digital downloads, visualizar os itens digitais disponiveis e validar que a pagina de downloads digitais esta visivel.
```

Pode virar:

```text
1. acessar a categoria Digital downloads, visualizar os itens digitais disponiveis
2. validar que a pagina de downloads digitais esta visivel
```

Para especificacoes passo a passo, cada linha tende a virar um requisito.

### 2. Termos De Cobertura

Cada requisito e normalizado em termos relevantes. Termos genericos sao removidos, por exemplo:

```text
usuario, deve, pagina, validar, acessar, clicar
```

Assim, um requisito como:

```text
validar que a pagina de comparacao ficou visivel
```

fica centrado em:

```text
comparacao
```

Como as especificacoes estao frequentemente em portugues e o grafo vem da interface em ingles, existe uma pequena camada de sinonimos:

```text
comparacao -> compare, comparison, compareproducts
cartao -> card, cards
presente -> gift
carrinho -> cart, shopping
registro -> register, registration
livro -> book, books
```

Essa camada nao traduz a especificacao inteira. Ela apenas reduz falsos negativos em termos importantes do dominio.

### 3. Busca De Evidencias No Grafo

Para cada requisito, o sistema procura evidencias em tres fontes:

- paginas relevantes;
- transicoes relevantes;
- caminhos candidatos.

Uma evidencia pode ser:

```json
{
  "kind": "page",
  "label": "Digital downloads",
  "score": 0.767,
  "details": {
    "url": "https://demowebshop.tricentis.com/digital-downloads",
    "matched_terms": ["digital", "downloads"]
  }
}
```

Ou:

```json
{
  "kind": "transition",
  "label": "Contact us",
  "score": 0.95,
  "details": {
    "source_url": "https://demowebshop.tricentis.com/about-us",
    "target_url": "https://demowebshop.tricentis.com/contactus",
    "action": "click",
    "matched_terms": ["contact", "us"]
  }
}
```

### 4. Classificacao Do Requisito

Cada requisito recebe um status:

| Status | Significado |
|---|---|
| `supported` | Ha evidencia forte no grafo, geralmente pagina alvo clara e/ou transicao/caminho acionavel. |
| `partial` | Ha evidencia parcial, mas o fluxo nao esta completamente sustentado. |
| `missing` | Nao ha evidencia suficiente no grafo para gerar esse passo sem risco de invencao. |

Exemplo:

```json
{
  "text": "validar que a pagina de downloads digitais esta visivel",
  "terms": ["downloads", "digitais", "digital"],
  "status": "supported",
  "confidence": 0.767,
  "evidence": [
    {
      "kind": "page",
      "label": "Digital downloads",
      "score": 0.767
    }
  ]
}
```

### 5. Classificacao Geral Da Especificacao

Depois de classificar os requisitos, o sistema calcula:

```text
coverage_score = (supported + partial * 0.5) / total
```

E atribui um status geral:

| Status geral | Interpretação |
|---|---|
| `supported` | A especificacao esta majoritariamente sustentada pelo grafo. |
| `partial` | O grafo cobre partes relevantes, mas ha lacunas. |
| `low_coverage` | O grafo nao oferece base suficiente para gerar o teste completo com seguranca. |

## Formato No Prompt

O prompt gerado passa a incluir:

```json
"specification_coverage": {
  "overall_status": "partial",
  "coverage_score": 0.75,
  "summary": {
    "supported": 1,
    "partial": 1,
    "missing": 0
  },
  "requirements": [
    {
      "text": "O usuario deve navegar ate a pagina Contact Us...",
      "terms": ["contact", "us", "site"],
      "status": "supported",
      "confidence": 0.95,
      "warning": "",
      "evidence": []
    }
  ],
  "warnings": []
}
```

Tambem foram adicionadas regras para a LLM:

```text
- Use specification_coverage para decidir o escopo do teste.
- Priorize requisitos supported.
- Trate requisitos partial com cautela.
- Nao invente passos marcados como missing.
```

## Exemplos Observados

Com o grafo atual do Demo Web Shop:

| Especificacao | Status | Leitura |
|---|---|---|
| `fluxo_downloads_digitais` | `partial` | O grafo contem `Digital downloads`, mas nem todo o fluxo e plenamente evidenciado. |
| `fluxo_contato` | `partial` | Existe pagina `Contact Us` e transicao para ela, mas o caminho completo ainda tem lacunas. |
| `fluxo_computadores_desktops` | `partial` | Existe `Computers`, mas falta evidencia forte da pagina/listagem `Desktops`. |
| `fluxo_cartao_presente_comparacao` | `low_coverage` | Ha alguma evidencia de comparacao, mas falta o caminho/produto de Gift Card. |
| `user_registration_book_purchase` | `low_coverage` | Faltam registro, catalogo de livros, Health Book e carrinho no grafo atual. |

## Como Usar Na Avaliacao

`specification_coverage` deve ser usado como variavel de contexto na avaliacao dos testes gerados.

Um teste ruim para uma especificacao `supported` indica problema provavel da LLM ou do prompt.

Um teste incompleto para uma especificacao `low_coverage` pode indicar uma limitacao do grafo, nao necessariamente falha da LLM.

Isso permite classificar melhor os resultados:

| Situação | Interpretação |
|---|---|
| Alta cobertura + teste com rota inventada | Falha da geracao do teste. |
| Baixa cobertura + teste incompleto | Limitação esperada do contexto. |
| Alta cobertura + teste falha por comportamento ausente | Possivel falha da aplicacao. |
| Baixa cobertura + teste passa usando rotas nao vistas no grafo | Resultado util, mas pouco fundamentado pela proposta. |

## Relevancia Para A Dissertacao

Essa camada fortalece a contribuicao cientifica porque o sistema deixa de ser apenas um gerador de prompts e passa a produzir tambem uma estimativa de confianca.

A contribuicao passa a incluir:

- grounding da LLM no grafo;
- selecao de contexto relevante;
- avaliacao previa da cobertura semantica;
- explicacao de lacunas antes da geracao do teste.

Isso e importante porque um prompt grande e aparentemente rico pode ainda nao conter o fluxo correto. `specification_coverage` explicita essa diferenca.

## Limitacoes

A cobertura e heuristica. Ela nao prova formalmente que o fluxo existe.

Principais limitacoes:

- depende da qualidade da exploracao feita pelo Crawljax;
- pode sofrer com sinonimos nao mapeados;
- pode marcar evidencia textual como parcial mesmo quando o clique real nao existe;
- nao interpreta profundamente regras de negocio;
- nao substitui a avaliacao humana da aderencia semantica.

Mesmo assim, ela melhora a auditabilidade do prompt e cria uma metrica util para comparar especificacoes, grafos e testes gerados.

## Evolucoes Possiveis

Possiveis melhorias:

- extrair requisitos com LLM ou parser semantico;
- expandir sinonimos automaticamente a partir do proprio grafo;
- diferenciar requisitos de acao, navegacao, formulario e assercao;
- exigir transicao acionavel para requisitos de acao;
- usar embeddings para comparar requisito e elementos do grafo;
- exibir a cobertura visualmente no modulo web.
