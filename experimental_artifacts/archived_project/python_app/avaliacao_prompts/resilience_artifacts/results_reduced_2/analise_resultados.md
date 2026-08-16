# Análise da rodada reduzida de mutações

## O que foi executado

- Data da execução: 20/07/2026.
- Site: Demo Web Shop público.
- Condição A: testes gerados pelo prompt **baseline**.
- Condição B: testes gerados pelo prompt com **contexto estruturado**.
- Uma repetição por execução.
- No máximo duas mutações neutras por cenário elegível: uma estrutural (E1) e uma de implementação (E2), quando disponível.
- Seleção determinística pelo hash do plano congelado, sem consultar o resultado das condições.
- Mudanças de contrato visível/acessível (E3) não foram usadas nesta rodada reduzida.

As mutações foram aplicadas no DOM carregado pelo navegador. O servidor público e
os arquivos originais dos testes não foram modificados.

## Elegibilidade antes das mutações

Foram executados 12 cenários nas duas condições sobre a interface original.
Somente quatro passaram nas duas condições e puderam entrar na comparação
pareada:

1. adicionar produto ao carrinho;
2. buscar Blue Jeans;
3. consultar detalhes de Fiction;
4. limpar o carrinho.

Os oito cenários restantes foram excluídos antes das mutações. Sete dependiam de
credenciais ou dados de ambiente ausentes em pelo menos uma condição. O cenário
de configuração de desktop falhou nas duas condições por timeout de interação.
Essa exclusão não representa vitória de nenhuma abordagem.

## Resultado das mutações

Oito mutações foram selecionadas. Todas passaram pelo controle diferencial, isto
é, a instrumentação confirmou a aplicação e o comportamento funcional observado
pelo controle permaneceu equivalente. Três foram classificadas como não
aplicáveis ao par porque os dois testes não interagiam com o alvo na página
original. Restaram cinco pares válidos.

| Classe | Pares válidos | Ambos passaram | Só baseline passou | Só contexto estruturado passou | Ambos falharam |
| --- | ---: | ---: | ---: | ---: | ---: |
| E1 — alteração estrutural neutra | 2 | 2 | 0 | 0 | 0 |
| E2 — alteração de implementação neutra | 3 | 0 | 0 | 3 | 0 |

Nas duas mutações E1 válidas, inserir um elemento irmão antes do campo de busca
ou envolver o campo em um novo contêiner não quebrou nenhum dos testes.

Nas três mutações E2 válidas, o controle de busca foi transformado de
`input[type="submit"]` em `button`, preservando o nome acessível “Search” e a
ação do formulário. Os testes baseline falharam por timeout ao procurar
`input.search-box-button`. Os testes com contexto estruturado passaram porque
usaram o papel e o nome do controle (`getByRole('button', { name: 'Search' })`).

## Interpretação permitida

Esta rodada fornece evidência de que, **nesta alteração específica do botão de
busca**, o locator por papel e nome continuou funcionando enquanto o locator
acoplado à tag `input` deixou de encontrar o controle. Ela não demonstra que o
contexto estruturado é universalmente mais resiliente.

As três observações favoráveis de E2 correspondem ao mesmo componente de busca
reutilizado em três cenários. Portanto, não são três mudanças independentes de
interface. Além disso, houve uma única repetição, apenas cinco pares válidos e o
teste exato de McNemar para E2 resultou em `p = 0,25`, acima de `0,05`. O resultado
é exploratório e descritivo; não permite rejeitar a hipótese nula nem sustentar
uma generalização estatística.

Para uma etapa confirmatória, ainda será necessário fornecer os dados de ambiente
dos cenários autenticados, corrigir ou justificar os testes que falham na página
original, executar mais componentes e operadores do plano congelado e tratar
componentes compartilhados como agrupamentos na análise.

## Rastreabilidade

- Hash do plano congelado: `44fe459525f513719dc46a9bb394fa77d00c8fe1679bc77d4fbedb16b5da4e7b`.
- Resultado estruturado: `resilience_results.json`.
- Relatório gerado: `resilience_results.md`.
- Evidências brutas: diretórios `original`, `controls`, `exposure` e `mutations`.
