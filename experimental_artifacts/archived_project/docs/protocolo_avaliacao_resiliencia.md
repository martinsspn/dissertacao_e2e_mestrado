# Protocolo de avaliação de resiliência dos testes E2E

## 1. Objetivo e separação das etapas

Este protocolo avalia o comportamento dos testes E2E gerados quando a interface
da aplicação sofre mudanças controladas. Ele é posterior e independente da
avaliação da geração dos testes.

A etapa de geração mede propriedades dos artefatos produzidos e sua execução na
interface original. Ela não fornece evidência de resiliência. A resiliência será
medida somente pela reexecução dos mesmos testes, sem reparo ou regeneração, em
interfaces modificadas.

As modificações serão aplicadas ao DOM recebido pelo navegador. Elas não serão
apresentadas como versões oficiais do Demo Web Shop nem como mudanças realizadas
no servidor da Tricentis.

## 2. Hipóteses

- **H0:** para uma mesma classe de mudança da interface, não há diferença na
  proporção de pares cenário-mutante que permanecem corretos entre baseline e
  contexto estruturado;
- **H1:** para pelo menos uma classe previamente definida de mudança, existe
  diferença nessa proporção.

Não será formulada a hipótese de que um tipo específico de locator é
universalmente superior.

## 3. Unidade experimental e comparação pareada

A unidade experimental principal é o par:

```text
(cenário, mutante da interface)
```

O mesmo mutante deve ser aplicado ao teste baseline e ao teste com contexto
estruturado do mesmo cenário. A comparação principal inclui somente os cenários
em que ambos os testes passam na interface original. Isso impede atribuir à
mutação uma falha que já existia antes dela.

Resultados dos demais testes podem ser apresentados como análise secundária
dentro de cada abordagem, sem serem misturados à comparação pareada principal.

## 4. Prevenção de viés na escolha das mutações

Como os resultados da geração e da execução inicial já foram observados, este
procedimento não deve ser apresentado como pré-registro anterior a todo o
experimento. Ele será um **registro prospectivo da etapa de resiliência**, feito
antes de gerar ou executar qualquer mutante. O conhecimento dos resultados
iniciais será declarado como ameaça à validade e mitigado pelas regras
determinísticas abaixo.

### 4.1 Dados proibidos durante a seleção

O gerador do plano de mutações não pode ler:

- os arquivos `.spec.ts` gerados;
- os relatórios de aprovação e falha;
- as contagens de tipos de locator;
- os erros produzidos pelo baseline ou pelo contexto estruturado.

### 4.2 Origem independente dos elementos-alvo

Os elementos candidatos serão obtidos a partir de:

- especificações originais dos cenários;
- inventário da interface coletado antes da avaliação;
- associação determinística entre etapa da especificação e elemento observado.

O catálogo conterá a identidade do elemento, página, ação e contrato funcional.
Seletores técnicos usados apenas para instrumentar o elemento não entram na
comparação e não podem ser disponibilizados à LLM.

Na implementação atual, a associação congelada é lida dos prompts estruturados
produzidos antes da geração dos arquivos `.spec.ts`. O gerador do plano extrai
somente página, etapa, ação e atributos do controle; ignora os testes gerados e
seus resultados. Essa escolha é declarada porque os prompts pertencem à condição
estruturada. Para impedir que isso beneficie a condição, um mutante só é
considerado aplicável na comparação pareada quando a instrumentação confirma que
os dois testes interagiam com o mesmo elemento antes da mutação.

### 4.3 Seleção reproduzível

O plano será produzido por algoritmo determinístico, com:

- operadores definidos antes da execução;
- regras de aplicabilidade explícitas;
- quantidade fixa por estrato;
- semente pseudoaleatória publicada;
- ordenação canônica dos candidatos antes do sorteio;
- arquivo final e código do gerador identificados por SHA-256.

Depois de congelado, o plano não poderá ser alterado em resposta aos resultados.
Qualquer exclusão será registrada, nunca removida silenciosamente.

## 5. Classes de mudança

Não será usada uma única lista composta apenas por mudanças que favoreçam
locators baseados em papel, rótulo ou texto. As mudanças serão estratificadas.

### E1 — Estrutura do DOM com contrato perceptível preservado

Exemplos:

- inserir contêiner intermediário;
- inserir elemento irmão não interativo;
- alterar profundidade ou agrupamento;
- reorganizar nós mantendo a mesma ordem visual, quando tecnicamente possível.

Essa classe altera a estrutura sem alterar nome acessível, texto visível ou ação.

### E2 — Atributos de implementação com contrato perceptível preservado

Exemplos:

- renomear `id` e atualizar referências como `label[for]`;
- renomear classe exclusivamente visual e preservar as regras CSS;
- substituir marcação por elemento semanticamente equivalente;
- alterar atributo não percebido pelo usuário e não utilizado pela lógica da
  aplicação.

A aplicabilidade deve ser confirmada sem observar o resultado dos testes
comparados.

### E3 — Contrato visível ou acessível alterado

Exemplos:

- alterar texto visível;
- alterar nome acessível;
- alterar rótulo mantendo a ação funcional;
- introduzir outro controle com nome semelhante.

Essa classe será reportada separadamente. Uma falha após mudança do contrato
percebido pelo usuário não será automaticamente classificada como fragilidade
indevida. O estrato mede sensibilidade a mudanças do contrato, não o mesmo
conceito medido por E1 e E2.

### E4 — Contrato explícito de teste alterado

Mudanças em `data-testid` ou em outro atributo declarado como contrato de teste
formam um estrato próprio. Elas não serão misturadas a mudanças estruturais.

## 6. Validade funcional do mutante

Cada mutante terá um teste de controle independente dos testes gerados. Antes da
mutação, o elemento-alvo receberá um identificador apenas instrumental, por
exemplo `data-resilience-target`. O teste de controle usará essa identidade para
verificar que:

- o elemento correto continua presente;
- a ação ainda pode ser executada;
- o resultado funcional esperado continua ocorrendo;
- a página não apresenta erro provocado pela instrumentação.

O atributo instrumental será injetado somente depois da geração dos testes e os
arquivos gerados permanecerão congelados. Assim, ele não influencia os locators
produzidos pela LLM.

Um mutante cujo controle falhar será marcado como **inválido**. O motivo e todas
as contagens de mutantes inválidos serão publicados. A decisão de invalidade não
poderá consultar qual abordagem passou ou falhou.

## 7. Execução

1. Calcular e registrar SHA-256 dos testes gerados, especificações, catálogo de
   elementos, plano de mutações e código do executor.
2. Executar os testes sem mutação em ordem aleatorizada.
3. Formar o conjunto pareado com os cenários aprovados nas duas abordagens.
4. Para cada mutante, executar primeiro o controle funcional.
5. Sem aplicar a mudança, marcar o elemento e confirmar que os dois testes do
   par realmente interagem com ele; caso contrário, registrar “não aplicável”.
6. Se o controle for válido e o par aplicável, executar as duas abordagens sobre
   o mesmo mutante.
7. Usar novo contexto do navegador e estado de sessão isolado em cada execução.
8. Alternar ou randomizar, com semente registrada, a ordem das abordagens.
9. Repetir cada condição para separar quebra reproduzível de flakiness.
10. Armazenar JSON do Playwright, trace, screenshot, log de mutação e identidade
   do elemento efetivamente acionado.

Contas, carrinho e wishlist devem ser reinicializados ou isolados. Quando o
estado remoto não puder ser controlado, a execução será marcada como ameaça à
validade ou inconclusiva.

## 8. Desfechos

### 8.1 Desfecho primário

Para cada estrato, será medida a sobrevivência pareada:

```text
testes que permanecem corretos / pares cenário-mutante válidos
```

“Permanece correto” exige que o teste conclua e que os eventos instrumentados
confirmem interação com o elemento esperado. Apenas `passed` não é suficiente,
pois um locator pode selecionar outro elemento e produzir um falso positivo.

### 8.2 Desfechos secundários

- locator não encontrado;
- violação de modo estrito por ambiguidade;
- elemento incorreto acionado;
- falha de asserção;
- timeout não atribuído ao locator;
- flakiness entre repetições;
- tempo e alteração necessários para reparar o teste, em etapa posterior.

## 9. Análise

Os resultados serão apresentados separadamente para E1, E2, E3 e E4. Não será
produzida uma conclusão universal a partir de um único percentual agregado.

Para os pares válidos podem ser usados:

- tabela pareada: ambos passam, apenas baseline passa, apenas estruturado passa,
  ambos falham;
- teste exato de McNemar para resultados binários pareados;
- diferença de proporções pareadas com intervalo de confiança;
- distribuição por operador e por cenário.

Uma média global, caso apresentada, será secundária, terá pesos definidos antes
da execução e será acompanhada dos resultados de cada estrato.

## 10. Ameaças à validade

- mutações sintéticas não representam toda a evolução real de uma aplicação;
- o site público e seu estado podem mudar durante o experimento;
- controles funcionais podem não detectar toda alteração comportamental;
- a amostra de cenários pareados pode ser pequena;
- a seleção a partir do inventário observado limita o universo às páginas
  exploradas;
- conhecimento prévio dos resultados exige reduzir graus de liberdade por meio
  de geração determinística, hashes e congelamento do plano.

## 11. Fundamentação

- Hammoudi, M.; Rothermel, G.; Tonella, P. *Why Do Record/Replay Tests of Web
  Applications Break?* ICST, 2016.
  [DOI 10.1109/ICST.2016.16](https://doi.org/10.1109/ICST.2016.16).
- Leotta, M.; Stocco, A.; Ricca, F.; Tonella, P. *Using Multi-Locators to
  Increase the Robustness of Web Test Cases.* ICST, 2015.
  [DOI 10.1109/ICST.2015.7102611](https://doi.org/10.1109/ICST.2015.7102611).
- Leotta, M.; Stocco, A.; Ricca, F.; Tonella, P. *Robula+: an algorithm for
  generating robust XPath locators for web testing.* Journal of Software:
  Evolution and Process, 2016.
  [DOI 10.1002/smr.1771](https://doi.org/10.1002/smr.1771).
- De Luca, M.; Fasolino, A. R.; Tramontana, P. *Investigating the robustness of
  locators in template-based Web application testing using a GUI change
  classification model.* Journal of Systems and Software, 2024.
  [DOI 10.1016/j.jss.2023.111932](https://doi.org/10.1016/j.jss.2023.111932).
