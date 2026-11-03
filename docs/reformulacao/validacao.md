# Reformulação visual — validação de 02/11/2026

Preparada para apresentação em 03/11/2026. Branch local `feat/reformulacao-dashboard`, baseada em `e53232a`. Sem push ou merge. Após a reformulação, o responsável solicitou um link pela internet para testes do grupo; um túnel HTTPS temporário foi preparado separadamente, sem hospedagem permanente.

## Escopo preservado

Somente interface, composição, estilos, gráficos, testes de interface e documentação. `app/core/`, `app/adapters/`, `firmware/` e `mobile/` não foram alterados. Cálculos, contratos, cenários, histórico, eventos e proteção permanecem os mesmos.

O quarto indicador agora conta alertas não resolvidos, incluindo reconhecidos. O gráfico usa apenas a janela existente de cinco minutos. Lista de eventos vazia é apresentada honestamente, sem registros fictícios da imagem. A tabela HTML semântica permite fonte legível e vírgula decimal; o CSV usa os mesmos dados filtrados e preserva seu formato anterior.

## Execução e testes

Windows, Python 3.14.3, Streamlit 1.50.0, Plotly 6.3.1, tzdata 2025.2. Nenhuma nova dependência de execução.

```powershell
.\.venv\Scripts\python.exe -m streamlit run app/main.py --server.headless true --server.address 127.0.0.1
.\.venv\Scripts\python.exe -m unittest discover -s app/tests -v
.\.venv\Scripts\python.exe -m pip check
```

- Referência inicial: 10 testes existentes passaram antes das alterações.
- Resultado após reformulação: **13 testes passaram**, incluindo navegação, filtro, reinício, pausa, ausência de leituras sem zeros fictícios, contagem de reconhecidos e confirmação de comando distinta da leitura seguinte.
- `pip check`: nenhuma dependência quebrada.
- Edge headless + Playwright: navegação lateral, link de eventos, atualização periódica sem interação, consumo elevado, vazamento, fechamento pendente/confirmado, reconhecimento, reabertura explícita, desconexão, pausa/retomada e download CSV exercitados.
- O arquivo baixado foi conferido quanto a nome e quantidade de linhas. A igualdade numérica do CSV filtrado é coberta pelo teste unitário existente; filtro de três dias também verificado por AppTest.

## Interface e acessibilidade

Capturas abertas e inspecionadas em desktop (1672 e 1440 px) e janela estreita (390 px), com altura ampliada para registrar conteúdo completo. A navegação lateral abre/recolhe em janela estreita. A área principal não apresentou transbordamento horizontal.

| Verificação | Resultado |
| --- | --- |
| Fonte principal | 17 px; secundária de eventos aproximadamente 16 px |
| Controles principais medidos no DOM | 46 px de altura, largura superior a 44 px |
| Foco de teclado | Contorno de 3 px; Tab alcança próximo botão |
| Texto principal / branco | 15,03:1 |
| Texto secundário / branco | 6,51:1 |
| Texto secundário / fundo principal | 5,99:1 |
| Texto branco / item de navegação selecionado | 4,81:1 |
| Texto da situação / fundo do modo demonstração | 5,69:1; usa o token escuro de foco |
| Ícones | SVGs locais como imagens, decorativos com `alt=""`; controles com rótulos |

As razões usam luminância relativa das cores de texto e fundo. Não constituem certificação WCAG nem auditoria com usuários/leitores de tela. Alertas nativos receberam os tokens escuros da aplicação para evitar contraste no limiar. O detector mecânico da skill impeccable não apresentou achados nos arquivos visuais. A revisão visual independente reabriu as dez capturas finais e retornou **ship**, sem correções materiais pendentes no recorte solicitado; medições de DOM e execução foram feitas pelo implementador.

## Capturas

| Área/estado | Evidência |
| --- | --- |
| Visão geral — desktop | [1672 px](overview-desktop.png), [1440 px](overview-1440.png) |
| Visão geral — estreita | [390 px](overview-narrow.png) |
| Histórico | [Desktop](history-desktop.png), [estreita](history-narrow.png) |
| Alertas | [Desktop](alerts-desktop.png), [estreita](alerts-narrow.png) |
| Comando pendente | [Desktop](pending-desktop.png) |
| Comunicação indisponível | [Desktop](offline-desktop.png) |
| Pausa | [Desktop](paused-desktop.png) |

As capturas usam dados e horários produzidos durante a execução. São evidências do software, não de sensores reais. O script opcional `app/tests/inspect_browser.cjs` usa `playwright` e Microsoft Edge; execute com `node app/tests/inspect_browser.cjs`, servidor local iniciado. `APP_URL` e `PLAYWRIGHT_MODULE` permitem caminhos alternativos. O script mantém as evidências da versão escura original em `docs/` e salva as novas nesta subpasta.

## Correções durante a revisão

- SVG inline era removido pelo sanitizador HTML do Streamlit; substituído por imagens SVG incorporadas, sem conexão externa.
- A altura mínima genérica de botão perdia precedência para o estilo nativo; seletor localizado foi aplicado e alvos de 46 px confirmados no DOM.
- Texto turquesa sobre fundo turquesa claro media 4,25:1; passou a usar o token de texto escuro. Alertas receberam o mesmo tratamento de contraste.
- Callbacks dos controles inferiores aplicam cenário, pausa e proteção antes de renderizar o painel, evitando atualização com estado anterior.
- Imports residentes do servidor exigiram reinício durante desenvolvimento; a verificação final foi feita com a implementação atual carregada.

## Limites atuais

Aplicação demonstrativa, sem integração física ou persistência. Histórico diário continua fixo em outubro de 2026. Textos e estados maiores podem aumentar a altura da página: a referência foi adaptada para legibilidade e controles nativos. CSS complementar depende de alguns `data-testid` da versão Streamlit validada; revisar ao atualizar a dependência. Não houve teste em Linux/macOS, leitores de tela ou dispositivos móveis físicos.

## Acesso temporário para o grupo

A pedido do responsável, foi iniciado um Cloudflare Quick Tunnel para a porta local 8501, usando `cloudflared 2026.10.7`. O executável oficial foi baixado para a pasta temporária do Windows; não integra o repositório. A URL é fornecida no chat e não é um endereço permanente. Cada visitante mantém uma sessão de simulação independente.

O endpoint público de saúde retornou HTTP 200. O roteiro Playwright também passou pela URL HTTPS pública: três telas, atualização periódica, comandos, cenários, reconhecimento, reabertura, desconexão, pausa e download CSV. As capturas desta pasta foram atualizadas nessa execução pública.

O serviço local e o túnel precisam permanecer ativos, com o computador ligado e conectado. A URL muda ao recriar o túnel e não há garantia de disponibilidade. Não houve publicação de código no GitHub nem configuração de hospedagem permanente. Referência: [Cloudflare Quick Tunnels](https://developers.cloudflare.com/tunnel/get-started/quick-tunnels/).

Veja o [roteiro de três minutos](../demo_mvp_visual.md) e a [instalação](../../app/README.md).
