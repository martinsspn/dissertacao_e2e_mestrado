# Estado de preparação da campanha de mutação

## Resultado

O executor e a fixture foram corrigidos e validados localmente. Nenhuma
execução desta etapa acessou o Demo Web Shop e nenhum resultado-piloto foi
promovido a resultado confirmatório.

## Correções implementadas

- pareamento de nomes diretos `cenario.spec.ts` e nomes legados;
- allowlist obrigatória por trilha e modelo;
- hashes da allowlist e da revisão semântica no manifesto;
- recusa de diretórios existentes no preparo e na execução;
- evento `interacted` obrigatório para considerar sobrevivência;
- distinção de falso positivo, alvo incorreto, falhas de locator, ambiguidade,
  asserção, runtime, instrumentação e ambiente;
- resultado agregado por unidade cenário-mutante, exigindo 3/3;
- JSON, stderr, trace e screenshot em diretório exclusivo por execução;
- código de saída, duração e metadados de runtime no resultado;
- execução sequencial, um worker e zero retries;
- preservação de apresentação na renomeação de ID/classe e na conversão de
  `input[type=submit]` para `button`.

## Validações realizadas

- 17 testes Python aprovados;
- fixtures locais de E1, E2 e E3 aprovadas em controle e mutação;
- operadores exercitados:
  - `insert_wrapper`;
  - `insert_noninteractive_sibling_before`;
  - `rename_id`;
  - `rename_class`;
  - `input_submit_to_button`;
  - `change_accessible_name`;
- prova ponta a ponta pelo executor:
  - status Playwright: `passed`;
  - classificação: `passed_interacted`;
  - eventos: `applied`, `interacted`;
  - código de saída: `0`;
  - JSON, stderr, screenshot e trace preservados.

## Allowlists candidatas

Foram criadas allowlists separadas para:

- trilha P / GPT-5.6 Sol;
- trilha P / Gemini 3.6 Flash;
- trilha R / GPT-5.6 Sol;
- trilha R / Gemini 3.6 Flash.

Esses arquivos ainda são candidatos. Seus hashes somente serão tratados como
congelados depois da geração e verificação do catálogo ampliado.

## Próximo marco

O código está apto para a preparação dos artefatos de congelamento. Antes da
campanha ao vivo ainda é necessário:

1. copiar para uma pasta versionada as especificações e prompts exatos da rodada
   ampliada;
2. gerar e verificar o catálogo e o plano ampliados;
3. montar diretórios independentes para cada combinação de trilha e modelo;
4. preparar os manifestos e conferir todos os hashes;
5. executar as três repetições de elegibilidade na interface original.
