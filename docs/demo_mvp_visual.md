# Demonstração ao grupo — cerca de dois minutos

Inicie pela raiz com `python -m streamlit run app/main.py`, ambiente ativo. Abra o endereço local e diga: **“Demonstração — dados simulados; não há hardware conectado.”**

1. **0:00–0:20:** Visão geral: L/min, volume da sessão, válvula e gráfico. Abra “Demonstração”. O resumo diário é exemplo separado.
2. **0:20–0:35:** “Consumo elevado”: vazão aumenta, surge atenção e válvula permanece aberta.
3. **0:35–0:55:** “Vazamento simulado”, proteção ligada: observe comando pendente, resposta, leitura fechada e vazão zero. Reabertura bloqueada.
4. **0:55–1:15:** Em “Alertas e controle”, reconheça o vazamento ativo: condição permanece. Volte ao cenário normal: evento resolvido, válvula ainda fechada. Clique “Abrir válvula” e aguarde leitura.
5. **1:15–1:35:** “Comunicação indisponível”: comandos bloqueados, válvula desconhecida. Após 10 s, “Sem comunicação”, horário antigo e valores desatualizados.
6. **1:35–2:00:** “Histórico”: filtre datas e baixe CSV. Retorne à operação normal. Se houver tempo, pause/retome e reinicie; reinício limpa apenas esta sessão.

Exploração adicional: desligue proteção antes do vazamento, observe alerta sem fechamento e ligue proteção. No consumo elevado com válvula fechada, abrir exige confirmação. Pausa longa envelhece leitura; retomar não soma intervalo pausado.

Regra didática, sem detector validado, economia calculada ou testes físicos.
