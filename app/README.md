# MVP visual — Guardião Hídrico

Aplicação local demonstrativa com um dispositivo (“Bancada principal”). Sem hardware, persistência, autenticação ou nuvem.

## Instalar e executar

Ambiente validado: Windows, Python 3.14.3, Streamlit 1.50.0, Plotly 6.3.1, tzdata 2025.2. Dependências diretas fixadas em `app/requirements.txt`.

Windows PowerShell, na raiz:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r app/requirements.txt
python -m streamlit run app/main.py
```

Nesta máquina o atalho `python` estava indisponível; a criação executada foi `py -3.14 -m venv .venv`. Alternativa sem ativar o ambiente ou alterar políticas do PowerShell:

```powershell
.\.venv\Scripts\python.exe -m pip install -r app/requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app/main.py
```

Linux/macOS (instruções fornecidas, execução não validada nessas plataformas):

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r app/requirements.txt
python -m streamlit run app/main.py
```

Abra o endereço exibido, normalmente http://localhost:8501. Compartilhar pela internet exige hospedagem posterior.

## Organização e decisões

- `main.py`: composição, sessão, navegação e controles de demonstração.
- `core/models.py`, `contracts.py`: modelos imutáveis e interface `TelemetrySource`.
- `core/demo_controller.py`: relógio monotônico, pausa e escolha de cenário.
- `adapters/mock_source.py`: integração de volume, leituras, eventos e respostas.
- `core/presentation.py`: estados derivados do contrato para apresentação.
- `core/example_history.py`: sete dias fixos de exemplo (05–11/10/2026), filtro e CSV.
- `ui/`: telas e Plotly. CSS usa classes próprias; tema em `.streamlit/config.toml`.

A interface operacional conhece somente o contrato. Os controles específicos de demonstração usam o controlador. Fonte e controlador ficam em `st.session_state`, sem cache mutável global. Navegar preserva estado; recarregar a conexão do navegador pode criar uma sessão nova.

## Regras demonstrativas

Vazão constante por trecho: incremento = L/min × segundos / 60. Atualizações usam tempo monotônico; renderizações sem avanço não duplicam volume ou leituras. Ruído determinístico por sessão, semente 42. Pausar exclui o intervalo pausado inclusive das respostas de comandos. A idade da leitura usa UTC real; uma pausa longa mostra desatualização explicada pela pausa.

Parâmetros em `core/config.py`: amostra 2 s, leitura antiga 10 s, resposta 3 s, timeout 8 s, histórico recente 5 minutos/151 amostras, até 200 eventos. Vazões: normal perto de 4 L/min, elevado 15 L/min, vazamento 9 L/min antes de fechar; ruído ±0,25 L/min. São parâmetros visuais sem calibração física.

Na indisponibilidade, não há leituras nem estimativa de volume perdido. Volume da sessão abrange intervalos simulados com comunicação, excluindo pausa. O contador real deverá ser revisado com firmware. A válvula passa a desconhecida imediatamente; após 10 s aparece “Sem comunicação”. Ausência não vira zero.

Consumo elevado não fecha. Vazamento bloqueia reabertura e, com proteção ligada, solicita fechamento uma vez. Desligar proteção não cancela um fechamento enviado. Sair do cenário resolve o alerta sem reabrir; reabertura exige ação explícita. Reconhecer preserva a condição. Outros alertas exigem confirmação antes de abrir. Vazamento cancela uma abertura pendente.

Pedido, confirmação e leitura são separados. Eventos pontuais de ação/resultado usam situação resolvido; o alerta de vazamento segue ativo/reconhecido até encerrar a condição. O CSV usa o mesmo conjunto filtrado do gráfico, tabela e totais.

## Verificar

Ambiente ativo, na raiz:

```powershell
python -m unittest discover -s app/tests -v
python -m pip check
```

Veja [resultados e limitações](../docs/validacao_mvp.md) e [roteiro de dois minutos](../docs/demo_mvp_visual.md).

## Extensão futura

Implementar outro `TelemetrySource` e revisar o [contrato](../docs/contrato_telemetria.md) com firmware. MQTT, persistência e múltiplos usuários podem exigir serviço intermediário. A proteção final deve residir no controlador/serviço apropriado, nunca depender de uma página aberta. Essas ideias não são requisitos desta entrega.
