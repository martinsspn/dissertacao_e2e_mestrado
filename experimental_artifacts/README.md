# Arquivos experimentais da dissertação

Esta pasta preserva os documentos, relatórios, resultados de execução,
campanhas experimentais e artefatos auxiliares produzidos durante a pesquisa.
Ela integra o repositório público da implementação:
<https://github.com/martinsspn/dissertacao_e2e_mestrado>.

Os arquivos originados no projeto `dissertacao_e2e_semantico` mantêm seus
caminhos relativos dentro de `archived_project/`. O arquivo
`archive_manifest.csv` registra o caminho original, o caminho arquivado, o
tamanho e o SHA-256 de cada item publicado. A integridade pode ser verificada
com:

```bash
python3 experimental_artifacts/scripts/verify_archive_manifest.py
```

As especificações em linguagem natural e os testes Playwright gerados também
permanecem nas pastas da implementação final. O acervo conserva as cópias e os
caminhos usados nas campanhas para permitir a auditoria dos resultados.

O arquivo local `archived_project/.env` não foi incorporado ao acervo público,
pois pode conter configuração específica do ambiente. Nenhum segredo ou
credencial é necessário para verificar o manifesto e consultar os resultados
já produzidos.
