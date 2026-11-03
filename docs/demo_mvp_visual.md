# Demonstração ao grupo — cerca de três minutos

Inicie pela raiz com `python -m streamlit run app/main.py`, ambiente ativo. Abra o endereço local e diga: **“Demonstração — dados simulados; não há hardware conectado.”**

1. **0:00–0:30:** Pela lateral, abra Visão geral. Mostre L/min, volume da sessão, estado informado da válvula e alertas ativos. O gráfico começa com poucas amostras reais da simulação e se forma a cada 2 s; não há curva pré-preenchida.
2. **0:30–0:50:** Abra “Configurações da demonstração”, no fim da tela. Selecione “Consumo elevado”: vazão aumenta e aparece atenção, sem fechamento automático.
3. **0:50–1:20:** Escolha “Vazamento simulado”, proteção ligada. Observe pendente, confirmação do comando e leitura fechada; vazão zero. “Abrir válvula” permanece bloqueado.
4. **1:20–1:50:** Use “Ver todos os eventos”. Reconheça o alerta: a condição continua presente. Encerre o cenário de vazamento selecionando operação normal: registro resolvido, válvula ainda fechada. Abra explicitamente e aguarde a leitura.
5. **1:50–2:20:** Selecione “Comunicação indisponível”: comandos bloqueados e válvula desconhecida; após 10 s surge leitura desatualizada. Retorne à operação normal. Pause e retome: o tempo pausado não é somado ao volume.
6. **2:20–3:00:** Abra Histórico pela lateral, selecione três dias e baixe o CSV. Explique que o histórico é ilustrativo e separado da sessão. Volte à visão geral. Reinicie apenas ao finalizar: isso limpa os dados da demonstração.

Exploração adicional: desligue proteção antes do vazamento, observe alerta sem fechamento e ligue proteção. No consumo elevado com válvula fechada, abrir exige confirmação. Pausa longa envelhece leitura; retomar não soma intervalo pausado.

Regra didática, sem detector validado, economia calculada ou testes físicos.
