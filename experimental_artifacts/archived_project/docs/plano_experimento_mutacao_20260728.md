# Plano operacional do experimento de mutação do DOM

## 1. Estado e objetivo

Este documento define a campanha confirmatória de resiliência dos testes E2E.
Os resultados exploratórios já existentes em `resilience_artifacts/results_*`
são pilotos de instrumentação e não serão incorporados aos resultados finais.
Eles foram executados antes da correção de todos os critérios descritos neste
plano e, em alguns casos, com apenas uma repetição.

O experimento verificará se os testes gerados somente com a especificação
(`baseline`) e os testes gerados com contexto estruturado reagem de maneira
diferente a alterações controladas no DOM. A geração dos testes permanece
congelada: somente a interface recebida pelo navegador será modificada.

## 2. Questões de pesquisa

- **QP1:** testes gerados com contexto estruturado apresentam sobrevivência
  diferente dos testes baseline diante de mudanças neutras do DOM?
- **QP2:** em quais estratos e operadores ocorrem resultados discordantes entre
  as duas condições?
- **QP3, exploratória:** como os testes reagem quando o nome visível ou
  acessível do elemento é alterado?

QP1 é a questão principal. QP3 não será misturada ao resultado confirmatório,
pois altera o contrato percebido pelo usuário.

## 3. Desenho pareado e trilhas de análise

A unidade experimental registrada será:

```text
(trilha, modelo, cenário, mutação, repetição)
```

O mesmo mutante será aplicado aos arquivos baseline e contexto estruturado do
mesmo modelo e cenário. Comparações entre modelos não serão tratadas como
pareadas.

### 3.1 Trilha P — testes originalmente aprovados

Esta é a trilha principal. Inclui somente pares em que os dois arquivos:

1. não foram reparados depois da geração;
2. obtiveram adequação semântica 6/6;
3. passaram na aplicação original;
4. passam novamente nas três execuções normalizadas de elegibilidade;
5. interagem com o elemento-alvo antes da mutação.

Somente esta trilha sustentará conclusões sobre a influência do contexto
estruturado na resiliência dos testes originalmente gerados.

### 3.2 Trilha R — testes após uma rodada de reparo

Esta trilha é secundária. Um par pode conter um arquivo reparado e outro
original, mas deve atender aos mesmos critérios técnicos e semânticos da trilha
P. Seus resultados serão identificados como resiliência após reparo e não serão
somados aos resultados principais.

Não será realizada nova correção em resposta aos resultados de mutação.

## 4. Amostra candidata antes da revalidação

### 4.1 Trilha principal

| Modelo | Cenário | Situação |
| --- | --- | --- |
| GPT-5.6 Sol | `suite_busca_blue_jeans` | candidato principal |
| GPT-5.6 Sol | `suite_detalhes_fiction` | candidato principal |
| GPT-5.6 Sol | `suite_limpar_carrinho` | candidato principal |
| GPT-5.6 Sol | `suite_login_invalido` | candidato principal |
| GPT-5.6 Sol | `suite_login_valido` | candidato principal |
| Gemini 3.6 Flash | `suite_cadastro_campos_obrigatorios` | candidato principal |
| Gemini 3.6 Flash | `suite_cadastro_confirmacao_senha` | candidato principal |
| Gemini 3.6 Flash | `suite_navegar_categoria_livros` | candidato principal |

A trilha principal possui, portanto, no máximo oito cenários: cinco do GPT e
três do Gemini.

Dois pares originalmente aprovados não entram na campanha ao vivo:

- `suite_logout`, do GPT, não possui alvo mutável associado no catálogo atual;
- `user_registration_book_purchase`, do Gemini, cria conta permanente no site
  público e não possui mecanismo autorizado de limpeza.

Eles serão registrados como, respectivamente, “sem alvo aplicável” e “excluído
por efeito persistente”, sem remoção silenciosa.

### 4.2 Trilha após reparo

| Modelo | Cenário | Arquivo reparado |
| --- | --- | --- |
| GPT-5.6 Sol | `suite_adicionar_carrinho` | baseline |
| Gemini 3.6 Flash | `fluxo_computadores_desktops` | baseline |
| Gemini 3.6 Flash | `suite_navegar_sobre_nos` | contexto estruturado |

O nome legado `fluxo_computadores_desktops` identifica a especificação de
navegação para a categoria *Digital downloads*. O nome será preservado para
manter a rastreabilidade, e a descrição correta será registrada no manifesto.

Os reparos `suite_persistencia_carrinho_apos_login` e `suite_login_valido` do
Qwen não formam pares, pois o arquivo da outra condição continua reprovado.
Consequentemente, o Qwen não participa da comparação pareada.

## 5. Ambiente normalizado

Todas as execuções usarão:

- `PROMPT_E2E_BASE_URL=https://demowebshop.tricentis.com/`;
- `BASE_URL=https://demowebshop.tricentis.com`;
- os mesmos aliases de credenciais para os dois testes do par;
- uma conta sintética exclusiva da campanha;
- um worker;
- zero *retries* internos do Playwright;
- novo contexto de navegador para cada teste;
- Chromium e versão do Playwright registrados no manifesto;
- execução sequencial, evitando concorrência sobre conta, carrinho e wishlist.

Segredos não serão gravados. O manifesto registrará apenas os nomes das
variáveis configuradas. Cenários que deixam carrinho ou sessão alterados devem
restaurar seu estado ou usar preparação e limpeza independentes da condição.

## 6. Estratos e operadores

### E1 — mudança estrutural neutra

- `insert_wrapper`: envolve o alvo com contêiner intermediário usando
  `display: contents`;
- `insert_noninteractive_sibling_before`: insere antes do alvo um irmão oculto,
  não interativo e com `aria-hidden`.

### E2 — mudança de implementação neutra

- `rename_id`: altera o `id` e atualiza `for`, `aria-controls`,
  `aria-describedby` e `aria-labelledby`;
- `rename_class`: altera uma classe apenas quando a apresentação computada
  puder ser preservada;
- `input_submit_to_button`: converte `input[type=submit]` em `button` com ação,
  texto e semântica equivalentes.

### E3 — mudança de contrato perceptível

- `change_accessible_name`.

E3 será executado somente depois da campanha principal e reportado como análise
exploratória independente.

### E4 — contrato explícito de teste

Não há `data-testid` no catálogo observado. E4 será registrado como não
aplicável; atributos artificiais não serão adicionados para criar esse estrato.

## 7. Seleção das mutações

Para cada cenário elegível serão selecionadas, sem consultar os testes ou seus
resultados:

1. uma mutação E1;
2. uma mutação E2, quando houver operador aplicável;
3. na ausência de E2, uma segunda mutação E1.

Os candidatos serão ordenados por SHA-256 calculado a partir do hash do plano,
do cenário e da identidade da mutação. Essa regra torna a seleção determinística
e impede a escolha posterior de mutações que favoreçam uma condição.

Cada mutação será repetida três vezes. A seleção confirmatória contém, no
máximo:

- trilha P: 8 cenários, 16 unidades cenário-mutante e 48 medições pareadas ao
  longo das três repetições;
- trilha R: 3 cenários, 6 unidades cenário-mutante e 18 medições pareadas ao
  longo das três repetições.

Uma observação pareada robusta corresponde ao resultado consolidado das três
repetições de baseline e contexto estruturado sobre o mesmo mutante.

## 8. Elegibilidade, validade e exposição

### 8.1 Elegibilidade na interface original

Antes de selecionar os mutantes executáveis, cada arquivo será executado três
vezes sem mutação. O cenário somente permanece se os dois arquivos passarem em
3/3. Resultado 1/3 ou 2/3 será classificado como instável e excluído da
comparação confirmatória.

### 8.2 Controle funcional do mutante

Para cada mutação e repetição:

1. executar o controle na página original com o alvo marcado;
2. executar o mesmo controle com a mutação aplicada;
3. comparar rota, parâmetros, headings, notificações, erros de página,
   respostas HTTP 5xx e efeito observável da ação;
4. invalidar o mutante se a observação funcional for diferente.

Mutante inválido não entra no denominador de sobrevivência.

### 8.3 Exposição do par

Na interface não mutada, cada teste deve:

- passar;
- produzir o evento `marked`;
- produzir o evento `interacted` para o alvo correto.

Se apenas uma condição interagir com o alvo, a unidade será “não aplicável ao
par”, em vez de ser contada como quebra da outra condição.

### 8.4 Execução mutada

Para sobreviver, o teste deve:

- passar no Playwright;
- registrar `applied`;
- registrar `interacted` para o alvo mutado;
- manter suas asserções semanticamente relevantes.

Um teste aprovado sem `interacted` será classificado como falso positivo.

## 9. Classificação dos resultados

Por repetição, cada execução será classificada como:

- `passed_interacted`;
- `false_positive_no_interaction`;
- `locator_not_found`;
- `strict_mode_ambiguity`;
- `wrong_target`;
- `assertion_failure`;
- `unrelated_timeout`;
- `runtime_code_error`;
- `instrumentation_failure`;
- `environment_failure`.

Por par cenário-mutante:

- **sobrevive:** passa e interage em 3/3;
- **quebra reproduzível:** falha em 3/3;
- **instável:** passa em 1/3 ou 2/3;
- **inválido:** controle funcional não preservado;
- **não aplicável:** uma das condições não exercita o alvo original.

## 10. Desfechos e análise

O desfecho primário será a sobrevivência robusta em E1 e E2. Para cada modelo,
estrato e operador será construída a tabela:

| Resultado pareado | Contagem |
| --- | ---: |
| ambos sobrevivem |  |
| somente baseline sobrevive |  |
| somente contexto estruturado sobrevive |  |
| ambos quebram |  |

Também serão reportados:

- diferença pareada de sobrevivência;
- taxa por repetição;
- instabilidade;
- falsos positivos;
- mutantes inválidos e não aplicáveis;
- distribuição das falhas;
- duração por condição e operador;
- associação descritiva entre perfil de locator e sobrevivência.

O teste exato de McNemar será exploratório e só será interpretado quando houver
quantidade razoável de pares discordantes. Como mutações do mesmo cenário não
são independentes, as conclusões priorizarão contagens por cenário e intervalos
agrupados por cenário. GPT e Gemini serão apresentados separadamente.

## 11. Volume máximo previsto

Com dois mutantes por cenário e três repetições, cada cenário pode produzir:

- 6 execuções de elegibilidade: 2 condições × 3;
- 12 controles funcionais: 2 estados × 2 mutantes × 3;
- 12 execuções de exposição: 2 condições × 2 mutantes × 3;
- 12 execuções mutadas: 2 condições × 2 mutantes × 3.

O teto é de 42 execuções Playwright por cenário:

- trilha P: até 336 execuções;
- trilha R: até 126 execuções;
- total: até 462 execuções.

O número real será menor quando um cenário for inelegível ou um mutante for
inválido ou não aplicável, pois as etapas posteriores não serão executadas.

## 12. Correções obrigatórias antes do congelamento

O executor atual ainda não está apto para a campanha confirmatória. Antes de
qualquer execução final, será necessário:

1. aceitar nomes diretos `cenario.spec.ts` e nomes legados
   `teste_*_baseline/estruturado.spec.ts`;
2. receber allowlists distintas para as trilhas P e R e registrar o hash do
   arquivo de revisão semântica;
3. exigir `interacted` também na execução mutada;
4. recusar diretório de saída existente, sem apagá-lo ou sobrescrevê-lo;
5. preservar JSON, stderr, trace, screenshot e eventos por execução;
6. registrar código de saída, duração, navegador, Playwright e hashes;
7. classificar automaticamente as falhas conforme a Seção 9;
8. mascarar as condições como A/B e balancear sua ordem por hash;
9. criar um plano ampliado que contemple os cenários da rodada Gemini;
10. validar todas as mudanças em fixtures locais sintéticas.

O comportamento atual que remove o diretório de saída deve ser eliminado. Os
resultados-piloto existentes serão preservados, mas nunca reutilizados como
resultado confirmatório.

## 13. Congelamento e rastreabilidade

Depois dos testes locais e antes da primeira requisição ao site público, serão
registrados:

- hashes das especificações e prompts estruturados;
- hash agregado das entradas;
- catálogo completo e plano de mutações;
- allowlists das trilhas P e R;
- testes originais, reparados e cópias instrumentadas;
- fixture, controle, executor e configuração do Playwright;
- semente e regra de seleção;
- versões de Node.js, Playwright e Chromium;
- manifesto da conta por identificador não secreto.

Cada modelo e trilha terá diretório e manifesto próprios. Uma campanha congelada
será imutável; qualquer repetição corretiva criará uma nova campanha.

## 14. Ordem operacional

1. implementar as correções obrigatórias do executor;
2. adicionar testes locais para cada operador e cada estado de resultado;
3. copiar para o repositório as entradas da rodada ampliada usadas na geração;
4. gerar o catálogo ampliado sem ler `.spec.ts` ou resultados;
5. preparar separadamente as trilhas P e R;
6. verificar manualmente os pares e hashes dos manifestos;
7. executar três repetições originais de elegibilidade;
8. congelar o conjunto elegível automaticamente;
9. selecionar duas mutações neutras por cenário pela regra hash;
10. executar controles e exposição;
11. executar os mutantes válidos e aplicáveis;
12. auditar falsos positivos, ambiguidades e uma amostra dos casos concordantes;
13. consolidar tabelas separadas por trilha, modelo, estrato e operador;
14. somente depois decidir sobre a campanha exploratória E3.

## 15. Critérios para iniciar a execução final

A campanha somente poderá começar quando todos os itens forem verdadeiros:

- testes unitários Python e testes Playwright das fixtures aprovados;
- nenhum diretório de resultado puder ser sobrescrito;
- evento `interacted` obrigatório no mutante;
- plano ampliado íntegro e identificado por SHA-256;
- pares das trilhas P e R revisados e separados;
- três execuções originais previstas no comando;
- cenário com criação permanente de conta excluído;
- comando de execução e estimativa de requisições revisados.
