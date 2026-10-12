# Validação do MVP visual

Realizada em 12/10/2026. Durante a implementação, a cópia local ainda não tinha metadados `.git` nem `LICENSE`. Na preparação posterior para envio, autorizada pelo responsável, a pasta foi vinculada ao histórico de `Ceistutis/Guardi-o-H-drico`, na branch `feat/mvp-visual`, e a licença MIT original foi restaurada. Documentação e firmware existentes foram preservados. Não houve merge ou deploy.

## Executado

- Ambiente virtual local: Python 3.14.3, Streamlit 1.50.0, Plotly 6.3.1 e tzdata 2025.2.
- `python -m streamlit run app/main.py --server.headless true --server.address 127.0.0.1`: servidor iniciou em 127.0.0.1:8501.
- `python -m unittest discover -s app/tests -v`: 10 testes passaram (9 de regras e 1 fluxo AppTest).
- `python -m pip check`: nenhuma dependência quebrada.
- Navegador Microsoft Edge headless via Playwright: navegação das três áreas, consumo elevado, vazamento, comando pendente e confirmado, reconhecimento, reabertura, indisponibilidade e download CSV.
- Filtro de três dias e pausa/retomada/reinício exercitados pelo AppTest. CSV filtrado comparado com os dados de origem por teste unitário.
- Layout em larguras de 1440 e 390 px, sem transbordamento horizontal da área principal. Capturas completas inspecionadas visualmente; a altura foi ampliada para registrar também o conteúdo abaixo da dobra.

## Evidências visuais

| Área | Desktop | Janela estreita |
| --- | --- | --- |
| Visão geral | [Captura](overview-desktop.png) | [Captura](overview-narrow.png) |
| Histórico | [Captura](history-desktop.png) | [Captura](history-narrow.png) |
| Alertas e controle | [Captura](alerts-desktop.png) | [Captura](alerts-narrow.png) |

[Indisponibilidade de comunicação](offline-desktop.png).

O script opcional `app/tests/inspect_browser.cjs` usa Node, Playwright e Edge instalados, com servidor local já iniciado. Executar `node app/tests/inspect_browser.cjs` após disponibilizar o pacote `playwright`; `PLAYWRIGHT_MODULE` aceita caminho alternativo do pacote. Essas ferramentas não são dependências da aplicação.

## Correções verificadas

O seletor inicialmente derivava seu valor inicial do cenário atual, alterando a identidade do widget em reruns e perdendo seleções subsequentes. Corrigido com chave estável e valor inicial constante; AppTest confirmou transições consecutivas e reinício. O teste inicialmente passava texto onde o seletor usa Enum; corrigido o teste para usar o modelo tipado. Avisos de largura de botões/tabela foram removidos usando a API suportada pela versão instalada.

O navegador integrado não iniciou devido a erro do sandbox; a revisão foi realizada no Edge headless alternativo. O sandbox também falhou ao lançar comandos, executados após aprovação da ferramenta. O alias `python` e o registro de Python 3.12 estavam obsoletos; usado launcher `py -3.14` para criar o ambiente.

## Limites

Sem validação física, firmware, sensores, calibração ou atuação real. Sem persistência; uma nova conexão pode reiniciar a sessão. Dados diários fixos, explicitamente ilustrativos. Ausência de telemetria não estima volume perdido. Resposta e timeout usam o relógio da simulação, congelado na pausa. A operação autônoma final não pode depender da página aberta.

Execução em Linux/macOS não foi testada. Nenhum transporte real ou ingestão de pacotes foi implementado; o contrato exige revisão com firmware. Não foram feitos ensaios de carga, segurança de produção ou publicação externa, fora deste escopo demonstrativo.
