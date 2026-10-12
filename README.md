# Guardião Hídrico Inteligente

Projeto acadêmico A3 de Sistemas Automatizados — Universidade São Judas Tadeu.

Sistema proposto de monitoramento e controle do consumo de água com ESP32, sensores e uma aplicação de supervisão.

## Objetivos

- Medir vazão e volume de água.
- Detectar possíveis vazamentos e consumo anômalo.
- Exibir dados, histórico e alertas na aplicação.
- Controlar uma válvula remotamente e demonstrar atuação em uma bancada.

## Estado atual

O MVP visual em Python, Streamlit e Plotly está implementado em `app/`: visão geral, histórico de exemplo, alertas e controle simulado. Firmware e integração física ainda precisam ser implementados e validados.

ESP32 e Arduino/C++ fazem parte da proposta. Sensores, válvula, comunicação e armazenamento permanecem a definir.

## Executar o MVP

Na raiz, Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r app/requirements.txt
python -m streamlit run app/main.py
```

Se o atalho `python` estiver indisponível, use `py -3.14 -m venv .venv` no primeiro passo. O endereço local abre no navegador; compartilhar pela internet exige hospedagem posterior.

Veja [instalação Windows e Linux/macOS](app/README.md), [roteiro de demonstração](docs/demo_mvp_visual.md), [contrato proposto](docs/contrato_telemetria.md) e [validação](docs/validacao_mvp.md). Dados e comandos são simulados; não comprovam comportamento físico.

## Organização

| Pasta | Finalidade |
| --- | --- |
| `firmware/` | Firmware do ESP32: leitura, controle e telemetria |
| `app/` | Aplicação de supervisão e serviços necessários |
| `docs/` | Diagramas e documentação técnica vinculados ao código |

## Começar a contribuir

Após a criação do repositório no GitHub:

```bash
git clone https://github.com/Ceistutis/Guardi-o-H-drico.git
cd Guardi-o-H-drico
git switch -c feat/nome-da-implementacao
```

Leia [CONTRIBUTING.md](CONTRIBUTING.md). Ao escolher as ferramentas de uma frente, documente sua instalação, execução e validação no README da pasta correspondente.

## Documentação e acompanhamento

- [Wiki do projeto no Notion](https://app.notion.com/p/3f7bcc86442281189691c3e6aad3bfdc): escopo, decisões, compras, atualizações, fotos e evidências.
- [Backlog no ClickUp](https://app.clickup.com/90171594670/v/l/li/901717763972): execução, responsáveis e sprints.

O acesso a essas páginas depende das permissões concedidas pela equipe.

## Equipe

Guilherme Ceistutis: gestão de projeto e desenvolvimento de software/aplicação.

As funções dos demais integrantes serão definidas pelo grupo e registradas na wiki.

## Próximas decisões

1. Definir componentes, alimentação e alternativa de válvula.
2. Definir protocolo e contrato de telemetria/comandos.
3. Revisar o contrato proposto e decidir o armazenamento futuro.
4. Implementar e validar leitura de sensores, painel e acionamento na bancada.

## Licença

Este projeto é distribuído sob a [licença MIT](LICENSE), preservada do repositório original.
