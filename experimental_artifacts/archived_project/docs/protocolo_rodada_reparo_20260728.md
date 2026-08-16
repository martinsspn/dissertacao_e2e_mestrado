# Protocolo da rodada única de reparo dos testes reprovados

## Objetivo

Medir quanto esforço automatizado é necessário para tentar tornar executáveis e
semanticamente corretos os arquivos que falharam na interface original. Os
resultados reparados formam uma análise separada e não substituem os testes
produzidos originalmente.

## Escopo

- 94 arquivos reprovados entre GPT-5.6 Sol, Qwen 2.5 Coder 7B e Gemini 3.6
  Flash;
- rodada corrigida anterior do Qwen e rodada ampliada atual;
- exclusão apenas da rodada do Qwen já substituída;
- preservação integral dos arquivos originais.

## Reparador e isolamento

Todos os arquivos serão submetidos ao mesmo reparador,
`qwen2.5-coder:7b` Q4_K_M, com temperatura zero e uma chamada sem estado por
arquivo.

Cada entrada conterá:

- especificação original;
- apenas o próprio arquivo gerado;
- erro da execução e diagnóstico da revisão;
- prompt estruturado somente quando o arquivo pertencer à condição estruturada.

O reparador não poderá ler outro teste gerado ou outro resultado de reparo.
Baseline e contexto estruturado permanecerão em diretórios diferentes. Nenhuma
resposta será reutilizada como contexto.

## Limite da rodada

Cada arquivo recebe exatamente uma chamada de reparo e uma avaliação posterior.
Não haverá segundo pedido ao modelo com base no novo erro. Correções humanas
posteriores, se realizadas, constituirão outra etapa.

## Métricas de esforço

- tempo de cliente e tempos informados pelo Ollama;
- tokens de entrada e saída;
- linhas originais e reparadas;
- linhas adicionadas e removidas;
- similaridade textual;
- reparo localizado versus reescrita ampla;
- coleta sintática pelo Playwright;
- aprovação na aplicação após uma tentativa;
- adequação semântica após o reparo;
- nova elegibilidade pareada para o experimento de mutação.

## Ambiente de reexecução

- um worker e contexto novo por teste;
- `PROMPT_E2E_BASE_URL` e `BASE_URL` apontando para o Demo Web Shop;
- mesmos valores de credenciais expostos sob todos os aliases exigidos;
- processos separados por modelo, rodada e condição;
- nenhum arquivo reparado usado como entrada para reparar outro.

## Interpretação

As medidas representam esforço de reparo automatizado pelo Qwen, não esforço
manual de um engenheiro. Um arquivo aprovado somente será considerado
recuperado para a etapa de mutação se também atender semanticamente à
especificação.

