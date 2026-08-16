# Testes exploratórios de mudança de `id` e `class`

## Escopo

Esta é uma rodada exploratória separada da avaliação anterior. Foi usado apenas
o cenário de busca por “Blue Jeans”, que passou na interface original tanto no
baseline quanto no contexto estruturado. Cada mutação foi executada isoladamente
e uma única vez em cada condição.

Os alvos vieram do catálogo anterior à geração dos testes. Como esse catálogo
não armazenava classes, os nomes de `class` foram lidos diretamente do DOM
público em 20/07/2026. O plano foi criado depois dos resultados iniciais e não
deve ser apresentado como plano confirmatório pré-registrado.

## Mudanças executadas

| Elemento | Antes | Depois |
| --- | --- | --- |
| Campo de busca | `id="small-searchterms"` | `id="small-searchterms--exploratory"` |
| Campo de busca | `class="search-box-text"` | `class="search-box-text--exploratory"` |
| Botão de busca | `class="search-box-button"` | `class="search-box-button--exploratory"` |

A apresentação visual calculada foi preservada durante as mudanças de classe.
As alterações ocorreram somente no DOM do navegador; o servidor não foi
modificado.

## Resultado

### Mudança do `id` do campo de busca

Essa mutação foi **funcionalmente inválida** e não entrou na comparação entre os
testes. O JavaScript da aplicação produziu o erro:

`Cannot set properties of null (setting '_renderItem')`

Isso mostra que o `id` também faz parte da implementação do autocomplete da
própria página. Se os testes falhassem depois dessa alteração, não seria possível
atribuir a falha somente ao locator. O resultado correto é “mutação inválida”, e
não vitória ou derrota de uma abordagem.

### Mudança da classe `search-box-text` do campo

- Baseline: passou.
- Contexto estruturado: passou.

Os dois testes localizam o campo pelo `id` `small-searchterms`; portanto, mudar
uma classe que não era usada pelos locators não os afetou.

### Mudança da classe `search-box-button` do botão

- Baseline: falhou por timeout ao clicar.
- Contexto estruturado: passou.

O baseline usa `input.search-box-button` e depende diretamente dessa classe. O
teste com contexto estruturado usa o papel `button` e o nome “Search”, que foram
preservados pela mutação.

## Interpretação permitida

Os resultados demonstram somente o comportamento desse componente e dessas duas
classes:

1. mudar uma classe não utilizada pelos testes não causou quebra;
2. mudar uma classe utilizada explicitamente pelo locator quebrou aquele teste;
3. o locator por papel e nome permaneceu válido porque seu contrato não mudou;
4. nem toda mudança de `id` é funcionalmente neutra — neste caso, ela quebrou o
   JavaScript da aplicação e precisou ser descartada.

Há apenas duas comparações de classe válidas e uma repetição. Esses dados são
descritivos e não sustentam uma conclusão estatística geral sobre resiliência.

## Rastreabilidade

- Plano exploratório: `../id_class_exploratory_plan.json`.
- Hash do plano: `eb8b218eb4610c65ff6e57943d2b3af64e71d11aed779640c90fc6b050fba0c8`.
- Resultado estruturado: `resilience_results.json`.
- Evidências brutas: diretórios `original`, `controls`, `exposure` e `mutations`.
