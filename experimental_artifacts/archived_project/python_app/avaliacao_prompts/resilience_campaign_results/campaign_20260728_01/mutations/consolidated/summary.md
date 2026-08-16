# Consolidação da campanha de mutações

- Manifesto verificado: `37406d85410bafb5cef3418e92c25b2e17a4d2d35d37a718eba2444165717c61`
- Unidades selecionadas: 20
- Controles válidos: 16
- Unidades pareadas aplicáveis: 14
- Execuções Playwright de resiliência (elegibilidade + mutação): 366

## Resultado por coorte

| Trilha | Modelo | Aplicáveis | Baseline | Estruturado | Só estruturado | p McNemar |
|---|---|---:|---:|---:|---:|---:|
| P | gemini-3.6-flash | 2 | 2/2 | 2/2 | 0 | 1.000 |
| P | gpt-5.6-sol | 8 | 4/8 | 8/8 | 4 | 0.125 |
| R | gemini-3.6-flash | 2 | 2/2 | 2/2 | 0 | 1.000 |
| R | gpt-5.6-sol | 2 | 1/2 | 2/2 | 1 | 1.000 |

A condição A corresponde ao baseline e a condição B ao contexto estruturado. A sobrevivência exige aprovação com interação comprovada no alvo em três de três repetições. Unidades sem controle válido ou sem exposição pareada foram excluídas do denominador.
