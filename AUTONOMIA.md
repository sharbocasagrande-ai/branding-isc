# Autonomia do ISC Branding

Cópia administrada por **SHARBO CASAGRANDE**, conta GitHub **sharbocasagrande-ai**. Migração de hospedagem em 18/11/2026.

Manual: https://sharbocasagrande-ai.github.io/branding-isc/brand-book.html

Repositório: https://github.com/sharbocasagrande-ai/branding-isc

## Original preservado

Os 357 arquivos do repositório de origem foram encontrados idênticos na cópia do titular. Commit original: dfe8806f801172a59809f0204bfa9f8f7acc4094. Árvore original: 1820555c78feff9f82468ba408e5127137f40742. A tag original-rafael-2026-11-18 conserva essa versão sem alterações. O manifesto preservation/original-2026-11-18.json registra caminho, tamanho, SHA-256 e blob Git de cada arquivo.

Conteúdo do manual, marcas, fotografias, modelos, fontes e créditos de origem foram preservados. O corpo dos três HTMLs principais permanece idêntico ao original. A versão de hospedagem altera a carga de fontes e os endereços de distribuição para eliminar dependência operacional da conta de origem. Os arquivos do designer em CorelDRAW e PDF, as versões para impressão, imagens e recursos continuam na árvore.

## Controle e dependências

O titular tem permissão administrativa no repositório. Na conferência de 18/11/2026, a conta rafaelnasch tem somente leitura pública, sem permissão de escrita. O vínculo de fork conserva a procedência; a publicação usa a branch main da conta do titular e não faz sincronização automática com a origem.

O endereço antigo, sob rafaelnasch.github.io, é controlado pela conta de origem. O endereço desta cópia usa sharbocasagrande-ai.github.io. Fontes necessárias à leitura em português são servidas localmente, com os mesmos bytes latinos da versão preservada; exportações autocontidas embutem fontes, imagens e scripts. Downloads da skill usam esta mesma conta. Links de referência a normas, ferramentas e sites externos continuam como referências e não são necessários para abrir o manual.

A hospedagem continua sujeita ao funcionamento do GitHub e à segurança da conta do titular. Esta migração não altera permissões da conta, não adiciona colaboradores e não promete invulnerabilidade. Histórico e cópia local permitem reconstrução em outro servidor.

## Reconstruir

Projeto estático: não há banco, variáveis de ambiente, dependências instaláveis nem gerenciador de pacotes. HTML de entrada index.html, manual em brand-book.html, motores iviz.js e iforms.js. Os scripts de empacotamento/exportação usam Python padrão; exportar PDF exige Playwright conforme documentação original.

Executar, a partir da raiz:

    python3 autocontido.py
    python3 tools/empacotar_skill.py

Copiar dist-skill/branding-isc.zip para downloads/branding-isc.zip após atualizar o pacote. Pages usa main, pasta raiz, com .nojekyll. Preservar créditos, marca e licenças das fontes e dos ícones.

## Critérios de verificação

Conferir integridade dos 357 arquivos originais pelo manifesto/tag; corpo editorial sem alteração; fontes locais; links de imagens/scripts; pacote ZIP válido; ausência de requisições à conta de origem; publicação sob a conta do titular. O registro final de verificação registra os resultados e o commit publicado.
