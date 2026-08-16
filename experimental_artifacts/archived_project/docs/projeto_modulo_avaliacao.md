# Ferramenta Auxiliar De Avaliação

## Status

Esta ferramenta é um módulo **não oficial**, criado apenas para auxiliar a execução do experimento e a leitura dos resultados. Ela não integra o gerador de prompts proposto como artefato principal. A aplicação web também é uma ferramenta auxiliar não oficial e apenas orquestra a execução local.

O código está fisicamente separado em:

```text
python_app/avaliacao_prompts/
  avaliacao_prompts/
    domain/
    application/
    infrastructure/
    presentation/
  relatorios/
  tests/
```

O pacote oficial `teste_prompt_e2e_semantico` não expõe comando de avaliação e não é importado pela ferramenta auxiliar.

## Objetivo

A ferramenta coleta evidências automáticas sobre testes Playwright gerados por LLM e organiza essas evidências para inspeção humana. Ela não decide sozinha se o teste representa corretamente a especificação.

São coletados:

- presença da importação do Playwright, bloco de teste e asserções;
- quantidade de ações e locators;
- uso de locators semânticos, XPath e espera fixa;
- URLs e textos encontrados no código;
- tamanho do prompt, quando o arquivo correspondente é localizado;
- conformidade de URLs e textos com o grafo, quando o Neo4j é consultado;
- campos reservados para resultado de execução e rubrica humana.

## Relatório Legível

A saída padrão é Markdown, em vez de uma lista JSON de campos técnicos. O arquivo contém:

1. visão geral consolidada;
2. instruções para interpretar as métricas;
3. leitura rápida por teste;
4. tabelas com estrutura e seletores;
5. evidências encontradas no código;
6. pontos não encontrados no grafo;
7. dados de prompt e execução;
8. rubrica humana com perguntas orientadoras.

As ausências no grafo são apresentadas como pontos para revisão, não como prova automática de erro.

## Execução

```bash
cd python_app/avaliacao_prompts
PYTHONPATH=. python3 -m avaliacao_prompts \
  --tests-dir ../teste_prompt_e2e_semantico/generated_tests/structured_context \
  --approach structured_context \
  --prompt-dir ../teste_prompt_e2e_semantico/generated_prompts \
  --base-url https://demowebshop.tricentis.com/ \
  --skip-graph \
  --output ./relatorios/structured_context.md
```

Para comparar com o grafo, remova `--skip-graph`. A conexão usa `NEO4J_URI`, `NEO4J_USER` e `NEO4J_PASSWORD`, que também podem ser informados por argumentos da CLI.

## Decisão Metodológica

A análise estática usa padrões textuais simples e explicáveis. Por isso, seus resultados devem ser combinados com a leitura da especificação, do teste gerado e, quando disponível, dos logs de execução. A correção semântica permanece uma decisão humana.
